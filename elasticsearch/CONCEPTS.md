# Elasticsearch 常规用法与生产实践（Python）

本页面向日常开发与生产环境的常见场景，按“概念 + 用法 + 参数意义”的方式整理。

## 1) 索引与映射（Index & Mapping）

核心概念：
- 索引是逻辑库，文档是记录。
- Mapping 定义字段类型，避免动态映射带来的类型错误。

生产习惯：
- 先建映射再写入。
- 结合索引模板（Index Template）统一规范。

示例（创建索引 + 映射）：

```python
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

es.indices.create(
    index="orders",
    mappings={
        "properties": {
            "order_id": {"type": "keyword"},
            "user_id": {"type": "keyword"},
            "amount": {"type": "float"},
            "created_at": {"type": "date"},
            "title": {"type": "text"},
        }
    },
)
```

## 2) 索引模板（Index Template）

用于统一命名、映射、ILM、别名。

示例（模板）：

```python
es.indices.put_index_template(
    name="orders-template",
    index_patterns=["orders-*"],
    template={
        "settings": {"number_of_shards": 3, "number_of_replicas": 1},
        "mappings": {"properties": {"order_id": {"type": "keyword"}}},
        "aliases": {"orders-read": {}, "orders-write": {}},
    },
)
```

## 3) 分片与副本（Shards & Replicas）

- 分片数影响吞吐与扩展性。
- 副本数影响可用性与读性能。

生产建议：
- 单分片控制在 10-50GB。
- 小索引不要过多分片。

## 4) 写入文档（Index API）

常用参数与含义：
- `index`：目标索引名。
- `id`：文档 ID，固定 ID 可避免重复写入。
- `document`：文档内容。
- `refresh`：`true/false/wait_for`，是否立即可见。
- `pipeline`：摄取管道（Ingest Pipeline）。
- `routing`：路由键，控制文档落到哪个分片。
- `op_type`：`index`（覆盖）或 `create`（已存在则失败）。
- `timeout`：写入超时时间。
- `if_seq_no`/`if_primary_term`：乐观锁，防并发覆盖。

示例：

```python
es.index(
    index="orders-2025.12",
    id="order-1001",
    document={"order_id": "order-1001", "amount": 99.0},
    refresh="wait_for",
    op_type="index",
)
```

## 5) 批量写入（Bulk）

批量提升吞吐，生产里是默认方式。

参数含义：
- `_index`：目标索引。
- `_id`：可选文档 ID。
- `_source`：文档内容。

示例：

```python
from elasticsearch import helpers

actions = [
    {"_index": "orders-2025.12", "_id": "1", "_source": {"order_id": "1", "amount": 10}},
    {"_index": "orders-2025.12", "_id": "2", "_source": {"order_id": "2", "amount": 20}},
]
helpers.bulk(es, actions, refresh=False)
```

## 6) 查询（Search）

常用参数与含义：
- `index`：索引或通配符。
- `query`：查询 DSL。
- `from_`/`size`：分页（小分页）。
- `sort`：排序规则。
- `track_total_hits`：是否精确统计总数。
- `_source`：返回字段过滤。
- `aggs`：聚合统计。
- `highlight`：高亮返回。
- `timeout`：查询超时。
- `terminate_after`：命中数量上限后提前结束。
- `min_score`：低于该分数的结果丢弃。
- `preference`：路由到同一 shard，保证缓存命中。
- `routing`：按路由键查询。
- `search_after`：深分页（配合 sort）。

示例（全文 + 过滤）：

```python
resp = es.search(
    index="orders-*",
    query={
        "bool": {
            "must": {"match": {"title": "refund"}},
            "filter": {"term": {"user_id": "u-1"}},
        }
    },
    sort=[{"created_at": "desc"}],
    size=10,
    track_total_hits=False,
)
```

## 7) 深分页（search_after）

生产里避免用大 `from`，用 `search_after`。

```python
resp = es.search(
    index="orders-*",
    query={"match_all": {}},
    sort=[{"created_at": "desc"}, {"_id": "asc"}],
    size=10,
    search_after=["2025-12-01T00:00:00Z", "order-1001"],
)
```

## 8) 聚合（Aggregations）

常见参数：
- `aggs`：聚合定义。
- `size=0`：只返回聚合结果，不返回文档。

```python
resp = es.search(
    index="orders-*",
    size=0,
    aggs={"amount_stats": {"stats": {"field": "amount"}}},
)
```

## 9) 更新（Update API）

参数含义：
- `id`：文档 ID。
- `doc`：部分更新内容。
- `doc_as_upsert`：不存在时插入。
- `retry_on_conflict`：冲突重试次数。

```python
es.update(
    index="orders-2025.12",
    id="order-1001",
    doc={"amount": 109.0},
    doc_as_upsert=True,
)
```

## 10) 删除（Delete API）

```python
es.delete(index="orders-2025.12", id="order-1001")
```

## 11) 多文档读取（mget / msearch）

```python
resp = es.mget(index="orders-2025.12", ids=["1", "2", "3"])

resp = es.msearch(
    index="orders-*",
    searches=[
        {"query": {"match": {"title": "refund"}}},
        {"query": {"term": {"user_id": "u-1"}}},
    ],
)
```

## 12) 别名（Alias）与无损切换

生产用别名做读写解耦与热切换。

```python
es.indices.update_aliases(
    actions=[
        {"add": {"index": "orders-2025.12", "alias": "orders-read"}},
        {"add": {"index": "orders-2025.12", "alias": "orders-write"}},
    ]
)
```

## 13) 数据流（Data Stream）

适合时间序列数据（日志、指标）。

- 写入数据流名，ES 自动管理 backing indices。
- 配合 ILM 实现冷热分层。

## 14) ILM（生命周期管理）

生产常配：hot -> warm -> cold -> delete。

```python
es.ilm.put_lifecycle(
    name="orders-ilm",
    policy={
        "phases": {
            "hot": {"actions": {"rollover": {"max_size": "30gb", "max_age": "7d"}}},
            "delete": {"min_age": "90d", "actions": {"delete": {}}},
        }
    },
)
```

## 15) Ingest Pipeline（摄取管道）

做字段清洗、解析、补充。

```python
es.ingest.put_pipeline(
    id="orders-pipeline",
    processors=[
        {"set": {"field": "ingested_at", "value": "{{_ingest.timestamp}}"}},
    ],
)
```

## 16) 生产实践要点

- **索引策略**：按业务/时间切分，避免单索引过大。
- **别名切换**：用读写别名做无损升级。
- **分片规划**：单分片 10-50GB，避免过多小分片。
- **refresh**：高吞吐写入可延迟刷新；实时性要求高再 `refresh=wait_for`。
- **监控**：关注 JVM、GC、磁盘、分片数、查询耗时。
- **安全**：生产启用 xpack.security + TLS。
- **查询性能**：尽量用 filter（不计分，可缓存）。

## 17) 常见错误与排查

- `401`：安全开启但未配置账号。
- `403`：权限不足。
- `429`：线程池拒绝，说明压力过大或分片过多。
- 查询慢：查看 slowlog，检查是否使用了深分页或非必要的评分排序。

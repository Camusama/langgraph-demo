# Elasticsearch 入门方案（Python）

面向初学者的最小可用流程：启动 ES → 安装 Python 客户端 → 创建索引 → 写入/检索 → 聚合。

## 1) 启动 Elasticsearch

方式 A：Docker（推荐）

```bash
docker run -d --name es \
  -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  docker.elastic.co/elasticsearch/elasticsearch:8.12.2
```

验证：

```bash
curl http://localhost:9200
```

方式 B：本机安装

下载并解压后运行 `bin/elasticsearch`，默认端口 `9200`。

## 2) 安装 Python 客户端

```bash
uv add elasticsearch
```

## 3) 最小可运行示例

保存为 `practice1/elasticsearch_quickstart.py`：

```python
from datetime import datetime
from elasticsearch import Elasticsearch


es = Elasticsearch("http://localhost:9200")

index_name = "books"

if not es.indices.exists(index=index_name):
    es.indices.create(
        index=index_name,
        mappings={
            "properties": {
                "title": {"type": "text"},
                "author": {"type": "keyword"},
                "price": {"type": "float"},
                "published_at": {"type": "date"},
                "tags": {"type": "keyword"},
            }
        },
    )

es.index(
    index=index_name,
    document={
        "title": "Elasticsearch in Action",
        "author": "Radu Gheorghe",
        "price": 59.9,
        "published_at": datetime.utcnow(),
        "tags": ["search", "es", "backend"],
    },
)

es.indices.refresh(index=index_name)

resp = es.search(
    index=index_name,
    query={"match": {"title": "elasticsearch"}},
)

for hit in resp["hits"]["hits"]:
    print(hit["_source"]["title"], hit["_source"]["author"])
```

运行：

```bash
uv run python practice1/elasticsearch_quickstart.py
```

## 4) 常见操作模板

### 4.1 批量写入（Bulk）

```python
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch("http://localhost:9200")

actions = [
    {"_index": "books", "_source": {"title": "Book A", "price": 10}},
    {"_index": "books", "_source": {"title": "Book B", "price": 20}},
]

helpers.bulk(es, actions)
```

### 4.2 精确过滤 + 分页

```python
resp = es.search(
    index="books",
    query={"term": {"author": "Radu Gheorghe"}},
    from_=0,
    size=10,
)
```

### 4.3 聚合统计

```python
resp = es.search(
    index="books",
    size=0,
    aggs={"price_stats": {"stats": {"field": "price"}}},
)

print(resp["aggregations"]["price_stats"])
```

## 5) 常见坑

- **索引映射**：建索引时先定义 mappings，避免字段被动态映射成错误类型。
- **刷新机制**：写入后默认有刷新间隔，测试时可手动 `refresh`。
- **keyword vs text**：`text` 适合全文搜索，`keyword` 适合精确过滤/聚合。
- **版本兼容**：客户端版本应与 ES 主版本一致（比如 ES 8.x 对应客户端 8.x）。

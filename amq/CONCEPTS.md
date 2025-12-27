# ActiveMQ 入门概念速览

这份小抄面向初学者，帮助快速理解 ActiveMQ 中常见的概念和术语。

## 1) Queue（队列）

- 点对点（P2P）模型。
- 一条消息只会被一个消费者处理。
- 适合订单处理、异步任务、流水线作业等。

示例（发送到队列并消费）：

```python
import stomp

conn = stomp.Connection([("localhost", 61613)])
conn.connect("admin", "admin", wait=True)
conn.send(destination="/queue/orders", body="create order #1001")
conn.subscribe(destination="/queue/orders", id=1, ack="auto")
```

## 2) Topic（主题）

- 发布订阅（Pub/Sub）模型。
- 一条消息会广播给所有订阅者。
- 适合事件通知、日志分发、跨服务数据同步等。

示例（发布到主题）：

```python
import stomp

conn = stomp.Connection([("localhost", 61613)])
conn.connect("admin", "admin", wait=True)
conn.send(destination="/topic/events.order", body="ORDER_CREATED")
```

## 3) Subscriber / Consumer（订阅者/消费者）

- 订阅者用于 Topic，消费者用于 Queue。
- 常见模式：
  - **持久订阅**：订阅者离线时消息会保留，上线后补收。
  - **非持久订阅**：订阅者离线时消息不保留。

示例（持久订阅）：

```python
import stomp

conn = stomp.Connection12([("localhost", 61613)])
conn.connect("admin", "admin", wait=True, headers={"client-id": "risk-service"})
conn.subscribe(
    destination="/topic/events.order",
    id="risk-sub",
    ack="auto",
    headers={"activemq.subscriptionName": "risk-service"},
)
```

## 4) Connection（连接）

- 客户端与 Broker 之间的 TCP 连接。
- 一个连接内可创建多个 Session / Subscription。
- 心跳和重连策略通常在 Connection 层配置。

示例（连接与心跳）：

```python
import stomp

conn = stomp.Connection12([("localhost", 61613)], heartbeats=(10000, 10000))
conn.connect("admin", "admin", wait=True)
```

## 5) Scheduled Destination（延迟投递/定时投递）

- 让消息延迟一段时间后再投递，或按计划重复投递。
- 常用于：
  - 延迟任务
  - 订单超时关单
  - 重试退避
- 常见头部（OpenWire/STOMP 通常可用）：
  - `AMQ_SCHEDULED_DELAY`：延迟毫秒
  - `AMQ_SCHEDULED_PERIOD`：重复间隔毫秒
  - `AMQ_SCHEDULED_REPEAT`：重复次数

示例（延迟 5 秒投递）：

```python
import stomp

conn = stomp.Connection([("localhost", 61613)])
conn.connect("admin", "admin", wait=True)
conn.send(
    destination="/queue/delayed",
    body="pay timeout",
    headers={"AMQ_SCHEDULED_DELAY": "5000"},
)
```

## 6) Message Group（消息分组）

- 让具有相同 Group ID 的消息被同一个消费者按顺序处理。
- 适合：
  - 按用户/订单维度顺序消费
  - 提高并发同时保持局部有序
- 常见头部：`JMSXGroupID`

示例（分组发送）：

```python
import stomp

conn = stomp.Connection([("localhost", 61613)])
conn.connect("admin", "admin", wait=True)
conn.send(
    destination="/queue/order-events",
    body="order step 1",
    headers={"JMSXGroupID": "ORDER-1001"},
)
```

## 7) ACK（消息确认）

- **自动 ACK**：客户端收到即确认，简单但不利于失败重试。
- **手动 ACK**：业务处理成功后再确认，便于失败重试和幂等处理。

示例（手动 ACK）：

```python
import stomp

class Listener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_message(self, frame):
        print("handle", frame.body)
        msg_id = frame.headers.get("ack") or frame.headers.get("message-id")
        self.conn.ack(msg_id, frame.headers.get("subscription"))


conn = stomp.Connection([("localhost", 61613)])
conn.set_listener("", Listener(conn))
conn.connect("admin", "admin", wait=True)
conn.subscribe(destination="/queue/tasks", id=1, ack="client-individual")
```

## 8) Selector（消息选择器）

- 类 SQL 条件表达式，用于过滤消息。
- 常用于 Topic 中按事件类型路由。
- 例子：`eventType = 'ORDER_CREATED'`

示例（Selector 订阅）：

```python
import stomp

conn = stomp.Connection([("localhost", 61613)])
conn.connect("admin", "admin", wait=True)
conn.subscribe(
    destination="/topic/events.order",
    id=1,
    ack="auto",
    headers={"selector": "eventType = 'ORDER_CREATED'"},
)
```

## 9) Dead Letter Queue（死信队列）

- 消息多次投递失败后进入 DLQ（默认 `ActiveMQ.DLQ`）。
- 常用于补偿处理或人工排查。

示例（订阅 DLQ）：

```python
import stomp

conn = stomp.Connection([("localhost", 61613)])
conn.connect("admin", "admin", wait=True)
conn.subscribe(destination="/queue/ActiveMQ.DLQ", id=1, ack="auto")
```

## 10) Producer（生产者）

- 负责发送消息。
- 关键注意：
  - 设置唯一消息 ID、追踪 ID 便于排障
  - 需要时开启持久化投递（persistent）

示例（带追踪与持久化头）：

```python
import stomp
import uuid

conn = stomp.Connection([("localhost", 61613)])
conn.connect("admin", "admin", wait=True)
conn.send(
    destination="/queue/orders",
    body="create order",
    headers={
        "trace_id": str(uuid.uuid4()),
        "correlation_id": str(uuid.uuid4()),
        "persistent": "true",
    },
)
```

## 11) Broker（消息代理）

- ActiveMQ 本体，负责存储、路由、投递消息。
- 可集群部署以提升可用性和吞吐。

示例（连接到指定 Broker）：

```python
import stomp

broker_host = "broker.company.net"
conn = stomp.Connection([(broker_host, 61613)])
conn.connect("admin", "admin", wait=True)
```

## 12) send 参数与示例（stomp.py）

参数详解：

- `destination`：队列或主题地址，ActiveMQ 用 `/queue/...` 或 `/topic/...` 前缀区分；
  其后的字符串仅是名称，可包含多个 `/`。
- `body`：消息体（字符串或 bytes）。JSON 建议先 `json.dumps`，并配合 `content-type`。
- `headers`：自定义头部（字典，键和值建议为字符串）。ActiveMQ 会把部分头部映射为 JMS
  属性或扩展能力，常见如下：
  - `content-type`：内容类型，如 `application/json`。
  - `content-length`：消息长度（通常由库自动填充，手动设置需与 bytes 长度一致）。
  - `persistent`：`true/false`，是否持久化到磁盘（Broker 重启后可保留）。
  - `priority`：`0-9`，优先级越高越优先投递（默认 4）。
  - `expires`：过期时间（毫秒时间戳），过期后 Broker 丢弃。
  - `correlation-id`：请求/响应关联 ID。
  - `reply-to`：响应地址（如 `/queue/reply`）。
  - `type`：消息类型/事件类型（字符串）。
  - `AMQ_SCHEDULED_DELAY` / `AMQ_SCHEDULED_PERIOD` / `AMQ_SCHEDULED_REPEAT`：
    延迟/周期投递参数。
  - `JMSXGroupID`：消息分组 ID（同组消息保持顺序）。
  - 说明：头部是否生效与 Broker/协议插件有关，生产使用前建议对照 ActiveMQ 版本文档验证。
- `content_type`：快捷设置 `content-type`（等价于 headers）。
- `transaction`：事务发送时的事务 id（需先 `begin`，再 `commit/abort`；异常可 `abort` 回滚）。
- `receipt`：要求 Broker 回执（可在 `on_receipt` 回调中确认投递）。

示例（带延迟投递与回执）：

```python
import json
import stomp
import uuid

conn = stomp.Connection([("localhost", 61613)])
conn.connect("admin", "admin", wait=True)

payload = {"eventType": "ORDER_CREATED", "orderId": "ORD-1"}
conn.send(
    destination="/topic/events.order",
    body=json.dumps(payload),
    headers={
        "content-type": "application/json",
        "persistent": "true",
        "trace_id": str(uuid.uuid4()),
        "AMQ_SCHEDULED_DELAY": "5000",
    },
    receipt="msg-1",
)
```

## 13) subscribe 参数与示例（stomp.py）

参数详解：

- `destination`：订阅目标（`/queue/...` 或 `/topic/...`），与生产者发送的地址匹配。
- `id`：订阅 id（必须唯一），用于 ACK/UNSUBSCRIBE 的定位，建议用字符串；
  同一连接复用 id 会覆盖旧订阅。
- `ack`：确认模式（`auto`、`client`、`client-individual`）。
- `headers`：订阅头部，常用：
  - `selector`：消息选择器（JMS Selector 语法），如 `eventType = 'ORDER_CREATED'`；
    字符串用单引号，字段名区分大小写。
  - `activemq.subscriptionName`：持久订阅名（Topic 常用），需配合 `connect` 的
    `client-id` 使用。
  - `prefetchSize` / `activemq.prefetchSize`：预取数量；值越大吞吐越高，但会导致
    单消费者积压、ACK 延迟；值越小越公平、延迟更可控。
  - `no-local`：`true/false`，不接收本连接发送的消息（部分 Broker 支持）。
  - `receipt`：订阅回执，用于确认订阅成功。

`ack` 语义说明：

- `auto`：Broker 一旦投递给客户端就视为确认；客户端崩溃时可能丢消息。
- `client`：客户端显式 ACK；一次 ACK 会确认当前消息及其之前未确认的消息（批量确认）。
- `client-individual`：客户端逐条 ACK；只确认当前消息，失败时可重投单条（更安全但更慢）。

示例（Selector + 持久订阅 + 手动 ACK）：

```python
import stomp

conn = stomp.Connection12([("localhost", 61613)])
conn.connect(
    "admin",
    "admin",
    wait=True,
    headers={"client-id": "risk-service"},
)

conn.subscribe(
    destination="/topic/events.order",
    id="risk-sub",
    ack="client-individual",
    headers={
        "selector": "eventType = 'ORDER_CANCELLED'",
        "activemq.subscriptionName": "risk-service",
    },
)
```

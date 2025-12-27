# ActiveMQ Pub/Sub Demo (Cross-Service)

一个更贴近生产使用方式的 ActiveMQ 主题（Topic）发布订阅示例：
- 多服务订阅同一主题（跨服务事件分发）
- 消息选择器（Selector）按事件类型路由
- 手动 ACK，便于失败重试
- 统一 Trace/Correlation 头部，便于链路追踪

## 1) 启动 ActiveMQ

本地安装或 Docker 均可，需开启 STOMP 端口 `61613`。

## 2) 安装依赖

```bash
uv add stomp.py
```

## 3) 环境变量

```bash
export AMQ_HOST=localhost
export AMQ_PORT=61613
export AMQ_USER=admin
export AMQ_PASSWORD=admin
```

## 4) 启动订阅者（跨服务）

终端 A（订单服务）

```bash
python practice2/amq_pubsub_demo/subscriber_order.py
```

终端 B（风控服务）

```bash
python practice2/amq_pubsub_demo/subscriber_risk.py
```

## 5) 发送事件

```bash
python practice2/amq_pubsub_demo/publisher.py --count 5
```

## 6) 说明

- 主题：`/topic/events.order`
- 事件类型：`ORDER_CREATED`、`ORDER_CANCELLED`
- Selector：`eventType = 'ORDER_CREATED'` 等
- 手动 ACK：处理失败可不 ACK，触发消息重投
- 追踪头：`trace_id`、`correlation_id`、`producer_service`

ActiveMQ 默认会将多次失败的消息投递到 `ActiveMQ.DLQ`（死信队列）。

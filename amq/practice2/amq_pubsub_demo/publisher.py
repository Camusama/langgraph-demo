import argparse
import json
import time
import uuid

from common import create_connection


TOPIC = "/topic/events.order"
EVENT_TYPES = ["ORDER_CREATED", "ORDER_CANCELLED"]


def build_event(event_type, order_id):
    return {
        "eventType": event_type,
        "eventId": str(uuid.uuid4()),
        "orderId": order_id,
        "occurredAt": int(time.time() * 1000),
        "payload": {
            "amount": 199.0,
            "currency": "CNY",
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=3)
    args = parser.parse_args()

    conn, cfg = create_connection()
    conn.connect(cfg["user"], cfg["password"], wait=True)

    for i in range(args.count):
        event_type = EVENT_TYPES[i % len(EVENT_TYPES)]
        order_id = f"ORD-{int(time.time())}-{i}"
        body = json.dumps(build_event(event_type, order_id))

        headers = {
            "trace_id": str(uuid.uuid4()),
            "correlation_id": str(uuid.uuid4()),
            "producer_service": "order-api",
            "eventType": event_type,
            "content-type": "application/json",
            "persistent": "true",
        }

        conn.send(destination=TOPIC, body=body, headers=headers)
        print("sent", event_type, order_id)
        time.sleep(0.2)

    conn.disconnect()


if __name__ == "__main__":
    main()

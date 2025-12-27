import json
import time

import stomp

from common import create_connection


TOPIC = "/topic/events.order"
SUBSCRIPTION = "risk-service"
SELECTOR = "eventType = 'ORDER_CANCELLED'"


class Listener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_message(self, frame):
        try:
            payload = json.loads(frame.body)
            print("risk-service received:", payload["eventType"], payload["orderId"])
            # stomp.py 1.2 uses positional args for ack
            self.conn.ack(frame.headers["message-id"], frame.headers.get("subscription"))
        except Exception as exc:
            print("risk-service error:", exc)


def main():
    conn, cfg = create_connection()
    conn.set_listener("", Listener(conn))
    conn.connect(cfg["user"], cfg["password"], wait=True)

    conn.subscribe(
        destination=TOPIC,
        id=1,
        ack="client-individual",
        headers={
            "activemq.subscriptionName": SUBSCRIPTION,
            "selector": SELECTOR,
        },
    )

    print("risk-service listening...", SELECTOR)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        conn.disconnect()


if __name__ == "__main__":
    main()

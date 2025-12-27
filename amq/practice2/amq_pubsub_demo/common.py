import os
import stomp


def load_config():
    return {
        "host": os.getenv("AMQ_HOST", "localhost"),
        "port": int(os.getenv("AMQ_PORT", "61613")),
        "user": os.getenv("AMQ_USER", "admin"),
        "password": os.getenv("AMQ_PASSWORD", "admin"),
    }


def create_connection():
    cfg = load_config()
    conn = stomp.Connection12(
        [(cfg["host"], cfg["port"])],
        heartbeats=(10000, 10000),
    )
    return conn, cfg

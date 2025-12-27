import time
import stomp


class Listener(stomp.ConnectionListener):
    def on_message(self, frame):
        print("received:", frame.body)


conn = stomp.Connection([("localhost", 61613)])
conn.set_listener("", Listener())
conn.connect("admin", "admin", wait=True)
conn.subscribe(destination="/queue/demo", id=1, ack="auto")

print("listening... Ctrl+C to exit")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    conn.disconnect()

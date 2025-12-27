import stomp

conn = stomp.Connection([("localhost", 61613)])
conn.connect("admin", "admin", wait=True)

conn.send(destination="/queue/demo", body="hello activemq1")
conn.disconnect()

# run

`dapr run  --app-id test --log-level debug python3 app.py --app-port 8002 -- uvicorn --host 0.0.0.0 --port 8002`

logs

```shell
✅  You're up and running! Both Dapr and your app logs will appear here.
....
== APP == TRACE:    127.0.0.1:60080 - ASGI [4] Started scope={'type': 'http', 'asgi': {'version': '3.0', 'spec_version': '2.3'}, 'http_version': '1.1', 'server': ('127.0.0.1', 8002), 'client': ('127.0.0.1', 60080), 'scheme': 'http', 'method': 'POST', 'root_path': '', 'path': '/state-outbox-transaction', 'raw_path': b'/state-outbox-transaction', 'query_string': b'', 'headers': '<...>', 'state': {}}
DEBU[0004] mDNS response for app id test received.       app_id=test component="nr (mdns/v1)" instance=DESKTOP-VDQACTQ scope=dapr.contrib type=log ver=1.14.4
DEBU[0004] Adding IPv4 address 172.19.34.189:43979 for app id test cache entry.  app_id=test component="nr (mdns/v1)" instance=DESKTOP-VDQACTQ scope=dapr.contrib type=log ver=1.14.4
== APP == /home/jse/dapr-outbox-python/app.py:50: DeprecationWarning: metadata argument is deprecated. Dapr already intercepts API token headers and this is not needed.
== APP ==   c.execute_state_transaction(
WARN[0004] Redis does not support transaction rollbacks and should not be used in production as an actor state store.  app_id=test component="outbox-statestore (state.redis/v1)" instance=DESKTOP-VDQACTQ scope=dapr.contrib type=log ver=1.14.4
DEBU[0004] Processing Redis message 1738263971272-0      app_id=test component="pubsub (pubsub.redis/v1)" instance=DESKTOP-VDQACTQ scope=dapr.contrib type=log ver=1.14.4

== APP == TRACE:    127.0.0.1:60080 - ASGI [4] Send {'type': 'http.response.start', 'status': 200, 'headers': '<...>'}
```

# state transaction

` dapr invoke --app-id test --method state-outbox-transaction --data '{}' `

invoke logs

```shell
== APP == /state-outbox-transaction: Execute the state transaction
== APP == /state-outbox-transaction: Transaction executed

== APP == INFO:     127.0.0.1:60080 - "POST /state-outbox-transaction HTTP/1.1" 200 OK
== APP == TRACE:    127.0.0.1:60080 - ASGI [4] Send {'type': 'http.response.body', 'body': '<18 bytes>'}
== APP == TRACE:    127.0.0.1:60080 - ASGI [4] Completed

DEBU[0005] Processing Redis message 1738263972273-0      app_id=test component="pubsub (pubsub.redis/v1)" instance=DESKTOP-VDQACTQ scope=dapr.contrib type=log ver=1.14.4
== APP == TRACE:    127.0.0.1:60080 - ASGI [5] Started scope={'type': 'http', 'asgi': {'version': '3.0', 'spec_version': '2.3'}, 'http_version': '1.1', 'server': ('127.0.0.1', 8002), 'client': ('127.0.0.1', 60080), 'scheme': 'http', 'method': 'POST', 'root_path': '', 'path': '/events/pubsub/outbox', 'raw_path': b'/events/pubsub/outbox', 'query_string': b'', 'headers': '<...>', 'state': {}}
== APP == TRACE:    127.0.0.1:60080 - ASGI [5] Receive {'type': 'http.request', 'body': '<394 bytes>', 'more_body': False}
== APP == TRACE:    127.0.0.1:60080 - ASGI [5] Send {'type': 'http.response.start', 'status': 200, 'headers': '<...>'}
```

outbox event is received OK
```shell
== APP == /events/pubsub/outbox: Received a new event
== APP == {'data': '{ "say": "hello world from outbox transaction" }', 'datacontenttype': 'text/plain', 'id': 'outbox-c8194fb2-f970-4896-8b37-5aa87ae22f7f', 'pubsubname': 'pubsub', 'source': 'test', 'specversion': '1.0', 'time': '2025-01-30T20:06:11+01:00', 'topic': 'my-outbox-topic', 'traceid': '00-b3b3dc11f4640ea00f32639e60794ebd-1b56fc10e1e74f82-01', 'traceparent': '', 'tracestate': '', 'type': 'com.dapr.event.sent'}
== APP == /events/pubsub/outbox: Event processed

== APP == INFO:     127.0.0.1:60080 - "POST /events/pubsub/outbox HTTP/1.1" 200 OK
== APP == TRACE:    127.0.0.1:60080 - ASGI [5] Send {'type': 'http.response.body', 'body': '<4 bytes>'}
== APP == TRACE:    127.0.0.1:60080 - ASGI [5] Completed
```

invoke with metadata

` dapr invoke --app-id test --method state-outbox-metadata --data '{}' `

no outbox event received

```shell
== APP == TRACE:    127.0.0.1:50336 - ASGI [6] Started scope={'type': 'http', 'asgi': {'version': '3.0', 'spec_version': '2.3'}, 'http_version': '1.1', 'server': ('127.0.0.1', 8002), 'client': ('127.0.0.1', 50336), 'scheme': 'http', 'method': 'POST', 'root_path': '', 'path': '/state-outbox-metadata', 'raw_path': b'/state-outbox-metadata', 'query_string': b'', 'headers': '<...>', 'state': {}}
== APP == /home/jse/dapr-outbox-python/app.py:63: DeprecationWarning: metadata argument is deprecated. Dapr already intercepts API token headers and this is not needed.
== APP ==   c.save_state(
== APP == TRACE:    127.0.0.1:50336 - ASGI [6] Send {'type': 'http.response.start', 'status': 200, 'headers': '<...>'}
== APP == INFO:     127.0.0.1:50336 - "POST /state-outbox-metadata HTTP/1.1" 200 OK
== APP == TRACE:    127.0.0.1:50336 - ASGI [6] Send {'type': 'http.response.body', 'body': '<4 bytes>'}
== APP == TRACE:    127.0.0.1:50336 - ASGI [6] Completed

```
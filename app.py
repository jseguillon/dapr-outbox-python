import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dapr.clients import DaprClient

class CloudEventModel(BaseModel):
    data: str
    datacontenttype: str
    id: str
    pubsubname: str
    source: str
    specversion: str
    topic: str
    traceid: str
    traceparent: str
    tracestate: str
    type: str    
    
app = FastAPI()
c = DaprClient()

DAPR_STORE_NAME = "outbox-statestore"

@app.get('/dapr/subscribe')
def subscribe():
    subscriptions = [
        {
          'pubsubname': 'pubsub',
          'topic': 'my-outbox-topic',
          'routes': {
            'default' : '/events/pubsub/outbox'
        }
      }
    ]

    return JSONResponse(content=subscriptions)

@app.post('/state-outbox-transaction')
def outbox_transaction():
    from dapr.clients.grpc._request import TransactionalStateOperation, TransactionOperationType, DaprRequest

    transaction_operation = TransactionalStateOperation(
        operation_type=TransactionOperationType.upsert,
        key="1",
        data='{ "say": "hello world from outbox transaction" }',
    )

    print("/state-outbox-transaction: Execute the state transaction")
    c.execute_state_transaction(
        store_name=DAPR_STORE_NAME,
        operations=[transaction_operation],
        transactional_metadata={ 'datacontenttype': 'application/json'},
        metadata= (('datacontenttype', 'application/json'),)
    )
    
    print("/state-outbox-transaction: Transaction executed")
    return JSONResponse(content={"success": "true"})


@app.post('/state-outbox-metadata')
def outbox_metadata():
    c.save_state(
        store_name=DAPR_STORE_NAME,
        key="test",
        value='{ "say": "hello world from outbox-metadata" }',
        state_metadata={  "outbox.projection": "true" },
        metadata=(("outbox.projection", "true"),)
    )

@app.post('/events/pubsub/outbox')
async def get_body(request: Request):
   print("/events/pubsub/outbox: Received a new event")
   print(await request.json())
   print("/events/pubsub/outbox: Event processed")

import argparse 
parser = argparse.ArgumentParser(description="Run the FastAPI app with Uvicorn.")
parser.add_argument("--port", type=int, default=8000, help="Port to run the Uvicorn server on.")
parser.add_argument("--log_level, -l", type=str, default="trace", help="Log level for Uvicorn.")
args, unknown = parser.parse_known_args()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=args.port, log_level="trace")
    app.run()
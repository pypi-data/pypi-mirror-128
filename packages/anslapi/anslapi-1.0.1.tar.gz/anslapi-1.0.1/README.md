# anslapi

A python3 module for creating a simple API with AWS Lambda and API Gateway.

## Install

```shell
python3 -m pip install anslapi
```

## Configuration

Create an api gateway with the methods that are needed, and set up authentication, schemas, etc. as wished. Create a Lambda function and configure our function as the target for each method. Use Lambda proxy mode.

## Usage example

```python
from anslapi import APIHandler

def get_user(userid):
  return "user.name@example.com"

def add(event):
  import json
  result = { 
    "status": "FAIL"
  }

  j = json.loads(event["body"])

  if "userid" in j:
    result["response"] = cls.get_user(j["userid"])
    result["status"] = "SUCCESS"
    return (200, result)

  else:
    result["reason"] = "Invalid request"
    return (400, result)  


def lambda_handler(event, context):
  ah = APIHandler()

  ah.add_handler('/add', 'POST',  Actions.add)
  
  response = ah.handle(event)
    
  return response

```

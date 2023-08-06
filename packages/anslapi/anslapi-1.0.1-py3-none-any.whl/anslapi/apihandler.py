import json
from json.decoder import JSONDecodeError

class APIHandler(object):

  def __init__(self):
    self.methods = {}


  def add_handler(self, resource, method, func):
    if method not in self.methods:
      self.methods[method] = {}

    self.methods[method][resource] = func


  def _get_allowed_methods(self, resource):
    a = ["OPTIONS"]
    for method in self.methods:
      for x in self.methods[method].keys():
        if x == resource:
          a.append(method)

    return ','.join(a)

  @staticmethod
  def build_response(
        status_code,
        body,
        allowed_methods=None,
        allowed_origin='*',
        allowed_headers='*'
  ):

    result = {
      'statusCode': status_code,
      'body': json.dumps(body),
      'headers': {
        'Content-Type': 'application/json'
      }
    }

    if allowed_methods is not None:
      cors = {
        'headers': {
          'Access-Control-Allow-Origin':  allowed_origin,
          'Access-Control-Allow-Methods': allowed_methods,
          'Access-Control-Allow-Headers': allowed_headers
        }
      }
      return { **result, **cors }

    else:
      return result


  def handle(self, event):
    if 'body' in event:
      if event['httpMethod'] in ['PUT', 'POST', 'PATCH']:
        try:
          json.loads(event['body'])
        except JSONDecodeError as e:
          return self.build_response(400, { "message": "Invalid JSON in request body" })
        except Exception as e: # pylint: disable=broad-except
          print("Exception: " + str(e))
          return self.build_response(400, { "message": "Unknown error with request" })

    else:
      # If you get this error, check that you are running API Gateway in Lambda Proxy mode
      return self.build_response(400, { "message": "Invalid request, check config" })

    if event['httpMethod'] not in self.methods:
      return self.build_response(405, { "message": "Method not allowed" }, None)

    if event['resource'] not in self.methods[event['httpMethod']]:
      return self.build_response(404, { "message": "Not found" }, None)

    func = self.methods[event['httpMethod']][event['resource']]
    allowed_methods = self._get_allowed_methods(event['resource'])

    sc, response = func(event)
    return self.build_response(sc, response, allowed_methods)

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher

from object_detection import predict

@dispatcher.add_method
def run(path, save=False):
    return predict(path, save)

@Request.application
def application(request):
    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return Response(response.json, mimetype='application/json')

if __name__ == '__main__':
    run_simple('localhost', 4000, application, use_reloader=True)

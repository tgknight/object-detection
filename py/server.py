from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher

from object_detection import model_init, predict, remove_summary_train

model = None
@dispatcher.add_method
def run(path, save=False):
    return predict(model, path, save)

@Request.application
def application(request):
    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return Response(response.json, mimetype='application/json')

if __name__ == '__main__':
    model = model_init()
    remove_summary_train()
    run_simple('localhost', 9000, application)

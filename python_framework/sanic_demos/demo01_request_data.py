from sanic import Sanic
from sanic.response import json
from sanic.response import text
from sanic import Blueprint


bp = Blueprint('my_blueprint', url_prefix="/bp")
@bp.route('/')
async def bp_root(request):
    # http "http://localhost:8000/bp"
    if request.app.config.get('DEBUG'):
        return json({'status': 'debug'})
    else:
        return json({'status': 'production'})

blueprint = Blueprint('foo', url_prefix="/foo")

@blueprint.get('/')
async def bar(request):
    # http "http://localhost:8000/foo"
    return text(request.endpoint)


app = Sanic()
app.blueprint(bp)
app.blueprint(blueprint)

@app.get("/")
def hello(request):
    # http "http://localhost:8000/"
    return text(request.endpoint)

@app.route("/json")
async def post_json(request):
    # curl -X GET http://localhost:8000/json -d '{"name": "呆瓜"}'
    # http get http://localhost:8000/json name=呆瓜
    return json({"hello": "world", "message": request.json})


@app.route("/query_string")
def query_string(request):
    # curl "http://localhost:8000/query_string?key1=value1&key2=value2"
    # http "http://localhost:8000/query_string?key1=value1&key2=value2"
    return json({ "parsed": True, "args": request.args, "url": request.url, "query_string": request.query_string })

@app.route("/query_string_with_blank")
def query_string(request):
    # http "http://localhost:8000/query_string_with_blank?key1&key2=value2"
    args_with_blank_values = request.get_args(keep_blank_values=True)
    return json({
        "parsed": True,
        "url": request.url,
        "args_with_blank_values": args_with_blank_values,
        "query_string": request.query_string
    })

@app.route("/test_request_args")
async def test_request_args(request):
    # http "http://localhost:8000/test_request_args?key1=value1&key2=value2&key1=value3"
    return json({
        "parsed": True,
        "url": request.url,
        "query_string": request.query_string,
        "args": request.args,
        "raw_args": request.raw_args,
        "query_args": request.query_args,
    })


@app.route("/files", methods=["POST",])
def post_json(request):
    # http -f "http://localhost:8000/files" test@test.txt
    test_file = request.files.get('test')
    file_parameters = {
        'body': test_file.body.decode(),
        'name': test_file.name,
        'type': test_file.type,
    }
    return json({ "received": True, "file_names": list(request.files.keys()), "test_file_parameters": file_parameters })


@app.route("/form", methods=["POST",])
def post_json(request):
    # http -f "http://localhost:8000/form" hello=world
    return json({ "received": True, "form_data": request.form, "test": request.form.get('test') })


@app.route("/users", methods=["POST",])
def create_user(request):
    # http -d "http://localhost:8000/users" a=10
    return text("You are trying to create a user with the following POST: %s" % request.body)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)

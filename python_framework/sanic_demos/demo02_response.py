from sanic import Sanic
from sanic import response

app = Sanic()


# Plain Text
@app.route('/text')
def handle_request(request):
    return response.text('Hello world!')

# HTML
@app.route('/html')
def handle_request(request):
    return response.html('<p>Hello world!</p>')

# JSON
@app.route('/json')
def handle_request(request):
    return response.json({'message': 'Hello world!'})

# FILE
@app.route('/file')
async def handle_request(request):
    return await response.file('c.png')

# Streaming
@app.route("/streaming")
async def index(request):
    async def streaming_fn(response):
        await response.write('foo')
        await response.write('bar')
    return response.stream(streaming_fn, content_type='text/plain')

# File Streaming
@app.route('/big_file.png')
async def handle_request(request):
    return await response.file_stream('c.png')

# Redirect
@app.route('/redirect')
def handle_request(request):
    return response.redirect('/json')

# Raw
@app.route('/raw')
def handle_request(request):
    return response.raw(b'raw data')

# Empty
@app.route('/empty')
async def handle_request(request):
    return response.empty()

# Modify headers or status
@app.route('/json_status')
def handle_request(request):
    return response.json(
        {'message': 'Hello world!'},
        headers={'X-Served-By': 'sanic'},
        status=200
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
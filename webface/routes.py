from webface import app


@app.route("/")
@app.route("/index")
def index() -> str:
    return "Hello, World!"

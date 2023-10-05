from flask import Flask

app = Flask(__name__)


@app.route("/app")
def members():
    return {"members": ["1", "2", "3"]}


if __name__ == "__main__":
    app.run(debug=True)

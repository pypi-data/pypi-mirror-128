from flask import (
    Flask,
    jsonify,
)

app = Flask('light controller')


@app.get('/')
def Index():
    return jsonify('hello from index')


if __name__ == '__main__':
    app.run()

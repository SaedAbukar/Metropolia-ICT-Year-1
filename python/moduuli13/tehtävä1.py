from flask import Flask, Response
import json

app = Flask(__name__)


def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


@app.route('/primetest/<int:num>')
def primetest(num):

    try:
        if is_prime(num):
            status_code = 200
            response = {
                "Number": num,
                "isPrime": True
            }
        else:
            status_code = 200
            response = {
                "Number": num,
                "isPrime": False
            }
    except ValueError:
        status_code = 400
        response = {
            "status": status_code,
            "text": "Invalid input"
        }
    json_response = json.dumps(response)
    return Response(response=json_response, status=status_code, mimetype="application/json")


@app.errorhandler(404)
def page_not_found(errorcode):
    response = {
        "status": "404",
        "text": "Invalid endpoint"
    }

    json_response = json.dumps(response)
    return Response(response=json_response, status=404, mimetype="application/json")


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)

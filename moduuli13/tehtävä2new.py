from flask import Flask, Response, render_template
import json
import airport_db_search


app = Flask(__name__)
app.debug = True

@app.route('/airport/<icao>')
def airport_response(icao):

    try:
        airport, city = airport_db_search.airport_search(icao)
        status_code = 200
        response_data = {
            "ICAO": icao,
            "Name": airport,
            "Municipality": city
        }

    except ValueError:
        status_code = 400
        response_data = {
            "msg": "Invalid ICAO-code."
        }

    # convert python dict to json format "manually"
    response_data = json.dumps(response_data)
    # setting up a status code for response needs Response object to be created
    response = Response(response=response_data, status=status_code, mimetype="application/json")
    return response


@app.errorhandler(404)
def page_not_found():
    response = {
        "status": "404",
        "text": "Invalid endpoint"
    }
    json_response = json.dumps(response)
    return Response(response=json_response, status=404, mimetype="application/json")


# @app.errorhandler(500)
# def page_not_found():
#     response = {
#         "status": "500",
#         "text": "ICAO-code not found"
#     }
#     json_response = json.dumps(response)
#     return Response(response=json_response, status=404, mimetype="application/json")
#

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=5000)

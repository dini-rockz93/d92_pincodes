from flask import Flask, request, render_template, make_response
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config_main import host_config, d92A_store, d92B_store, templates
from flask_restful import Api


app = Flask(__name__, template_folder = templates)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100000 per day"]
)


def main():
    CORS(app)
    app.run(**host_config)


@app.route('/')
def home():
    return "Hello world"


@app.errorhandler(429)
def ratelimit_handler(error):
    """
    Default error handler by flask_limiter if there is a multiple request
    type error:basestring
    """

    return make_response("A request is already in process please try after 1 minute"), 429


@app.route('/output_data', methods=['POST'])
@limiter.limit("10/1minute")
def result():

    if request.method == 'POST':

        request_data = request.data
        request_data = request_data.decode("utf-8")

        if len(request_data) == 0:
            return "Please enter the valid pincode", 415

        if request_data in d92A_store.keys():
            return d92A_store[request_data], 200

        elif request_data in d92B_store.keys():
            return d92B_store[request_data], 200

        else:
            return "Pin-code not found", 404

    return "The Configuration filename has been received and it's processing has been initiated"


@app.route('/home')
def home1():
    return render_template('home.html')



if __name__ == '__main__':
    main()

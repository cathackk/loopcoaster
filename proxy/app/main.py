from flask import Flask
from flask import request

from queueing import receive_from_queue
from queueing import send_to_queue


app = Flask(__name__)


@app.route('/send', methods=['POST'])
def send():
    # TODO: enforce json
    # TODO: size limit
    # TODO: auth
    routed = send_to_queue(request.get_data())
    return {'ack': routed}


@app.route('/receive', methods=['POST'])
def receive():
    # TODO: return metadata (author, received, ...?)
    messages = receive_from_queue()
    return {'messages': messages}, 200 if messages else 204

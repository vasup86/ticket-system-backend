
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
from user import createTicket, getUserAllTickets
from agent import getAgentAllTickets, getTicketMessages, insertMessage


app = Flask(__name__)

CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/createTicket', methods=['POST'], strict_slashes=False)
@cross_origin()
def createTickets():
    # get the userID and message from payload
    userID = request.json['userID']
    message = request.json['message']

    result = createTicket(userID, message)
    
    # throw error 406if error
    if result  == 'error':
        return jsonify({"errorType": 406, "result": "Error when creating the ticket"}), 406

    return jsonify({"result": "Created ticket successfully"})


@app.route('/getUserAllTickets', methods=['POST'])
@cross_origin()
def getUserAllTicketss():
    # get the userID and message from payload
    userID = request.json['userID']

    result = getUserAllTickets(userID)
    
    # throw error 406 if error
    if result  == 'error':
        return jsonify({"errorType": 406, "result": "Error in getting tickets"}), 406

    return jsonify({"result": result})


@app.route('/getAgentAllTickets', methods=['POST'])
@cross_origin()
def getAgentAllTicketss():
    # get the userID and message from payload
    agentID = str(request.json['agentID']).strip()

    result = getAgentAllTickets(agentID)
    
    # throw error 406if error
    if result  == 'error':
        return jsonify({"errorType": 406, "result": "Error in getting tickets"}), 406

    return jsonify({"result": result})


@app.route('/getTicketMessage', methods=['POST'])
@cross_origin()
def getTicketMessage():
    ticketID = int(request.json['ticketID'])

    result = getTicketMessages(ticketID)

    # throw error 406 if error
    if result  == 'error':
        return jsonify({"errorType": 406, "result": "Error in getting tickets"}), 406

    return jsonify({"result": result})


@socketio.on('send_message')
def handle_send_message(data):
    ticketID = int(data['ticketID'])
    userID = str(data['userID']).strip()
    agentID = str(data['agentID']).strip()
    creator = str(data['creator']).strip()
    message = str(data['message']).strip()

    insertMessage(ticketID, userID, agentID, creator, message)
    emit('receive_message', data, broadcast=True)


@app.route('/')
def homepage():
    return jsonify({"result":"connected"})

if __name__ == '__main__':
    socketio.run(app, port=5000,  debug=True)

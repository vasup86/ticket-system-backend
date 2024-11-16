
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from user import createTicket, getUserAllTickets
from agent import getAgentAllTickets

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/ticketsystem'
app.config['DEBUG']= True

db = SQLAlchemy(app)

CORS(app)

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
    
    # throw error 406if error
    if result  == 'error':
        return jsonify({"errorType": 406, "result": "Error in getting tickets"}), 406

    return jsonify({"result": result})


@app.route('/getAgentAllTickets', methods=['POST'])
@cross_origin()
def getAgentAllTicketss():
    # get the userID and message from payload
    userID = str(request.json['agentID']).strip()

    result = getAgentAllTickets(userID)
    
    # throw error 406if error
    if result  == 'error':
        return jsonify({"errorType": 406, "result": "Error in getting tickets"}), 406

    return jsonify({"result": result})


@app.route('/')
def homepage():
    return jsonify({"result":"connected"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

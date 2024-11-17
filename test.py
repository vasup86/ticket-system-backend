
import requests
import json

data = {
  "ticketID": 5435,
  "userID": "asas.b@example.com",
  "agentID":"admin3@example.com", 
  "creator": "agent", 
  "message":"testing new connection"
}



headers = {'Content-type': 'application/json', 'Accept': '*/*'}
r = requests.post('http://127.0.0.1:5000/', headers=headers, data=json.dumps(data))

print(r.json())
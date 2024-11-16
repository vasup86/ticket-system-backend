
import requests
import json

data = {
  "userID":  "john.doe@example.com",
  "message": "cannot asa"
}



headers = {'Content-type': 'application/json', 'Accept': '*/*'}
r = requests.post('http://127.0.0.1:5000/createTicket', headers=headers, data=json.dumps(data))

print(r.json())
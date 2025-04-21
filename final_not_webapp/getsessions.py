import requests
import json
import uuid

# Janus server endpoint
JANUS_SERVER_URL = "http://localhost:8088/janus"
# API headers
headers = {
    'Content-Type': 'application/json'
}

# Your Janus access token if needed, else leave as empty
ACCESS_TOKEN = ""

def create_session():
    """Creates a session with Janus and returns the session_id."""
    data = {
        "janus": "create",
        "transaction": str(uuid.uuid4())  # Unique transaction ID
    }

    response = requests.post(JANUS_SERVER_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_data = response.json()
        if response_data['janus'] == 'success':
            return response_data['data']['id']  # session_id
        else:
            print(f"Error creating session: {response_data['error']}")
    else:
        print(f"Failed to create session. Status code: {response.status_code}")
        print(response.text)
    return None

def attach_plugin(session_id):
    """Attaches the text room plugin and returns the handle_id."""
    data = {
        "janus": "attach",
        "plugin": "janus.plugin.textroom",
        "transaction": str(uuid.uuid4())  # Unique transaction ID
    }

    url = f"{JANUS_SERVER_URL}/{session_id}"
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_data = response.json()
        if response_data['janus'] == 'success':
            return response_data['data']['id']  # handle_id
        else:
            print(f"Error attaching plugin: {response_data['error']}")
    else:
        print(f"Failed to attach plugin. Status code: {response.status_code}")
        print(response.text)
    return None

def list_text_rooms(session_id, handle_id):
    """Lists available text rooms."""
    data = {
        "janus": "message",
        "transaction": str(uuid.uuid4()),  # Unique transaction ID
        "body": {
            "request": "list"
        }
    }

    url = f"{JANUS_SERVER_URL}/{session_id}/{handle_id}"
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_data = response.json()
        if response_data['janus'] == 'success':
            return response_data['plugindata']['data']  # Room list
        else:
            print(f"Error listing text rooms: {response_data['error']}")
    else:
        print(f"Failed to list text rooms. Status code: {response.status_code}")
        print(response.text)
    return None

# Send a message through the data channel
def join_message(session_id, handle_id, room):
    url = f"{JANUS_SERVER_URL}/{session_id}/{handle_id}"
    response = requests.post(url, json={
        "janus": "message",
        "transaction": str(uuid.uuid4()),
        "body" : {
            "request": "destroy",
            "transaction": str(uuid.uuid4()),
            "textroom": "join",
            "room": room,
            "pin": "",
            "username": "console",
            "display": "console",
            "token": "",
            "history": False
        }
    }
    )
    response_data = response.json()
    print("Send Message Response:", response_data)

# Send a message through the data channel
def send_message(session_id, handle_id, room, message):
    url = f"{JANUS_SERVER_URL}/{session_id}/{handle_id}"
    response = requests.post(url, json={
        "janus": "message",
        "transaction": str(uuid.uuid4()),
        "body" : {
            "request": "destroy",
            "transaction": str(uuid.uuid4()),
            "textroom" : "message",
            "room" : room,
            "text" : message
        }
    }
    )
    response_data = response.json()
    #print("Send Message Response:", response_data)

# Send a message through the data channel
def leave_message(session_id, handle_id, room):
    url = f"{JANUS_SERVER_URL}/{session_id}/{handle_id}"
    response = requests.post(url, json={
        "janus": "message",
        "transaction": str(uuid.uuid4()),
        "body" : {
            "request": "destroy",
            "transaction": str(uuid.uuid4()),
            "textroom" : "leave",
            "room" : room,
        }
    }
    )
    response_data = response.json()
    #print("Send Message Response:", response_data)

# Main logic
#returns the session id and handle id
def init_console():
    session_id = create_session()
    if session_id:
        print(f"Session created: {session_id}")
        handle_id = attach_plugin(session_id)
        if handle_id:
            print(f"Plugin attached: {handle_id}")
            text_rooms = list_text_rooms(session_id, handle_id)
            if text_rooms:
                room = json.loads(json.dumps(text_rooms))['list'][0]['room']
                print("Available text rooms:")
                print(json.dumps(text_rooms, indent=2))
                join_message(session_id, handle_id,room)
                return [session_id, handle_id]
            else:
                print("No text rooms available.")
        else:
            print("Failed to attach text room plugin.")
    else:
        print("Failed to create session.")

def msg(session_id, handle_id,message):
    send_message(session_id, handle_id, 1234, message)

def destroy(session_id, handle_id):
    leave_message(session_id, handle_id,1234)

vals = init_console()
msg(vals[0], vals[1], "Hello World!")
destroy(vals[0], vals[1])

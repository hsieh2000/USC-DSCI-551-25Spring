import requests
import json
import sys
from datetime import datetime

# # Firebase Database configuration file
CONFIG_FILE = "config.json"

def config_load(config_file):
    f = open(f"./{config_file}") 
    return json.load(f)

# 1. Send a chat message
def send_chat_message(sender, receiver, message):
    # INPUT : Sender, Receiver, Message Body
    # RETURN : Status code of the Firebase REST API call [response.status_code]
    # EXPECTED RETURN : 200
    config_file = config_load(CONFIG_FILE)

    URL = f"{config_file["dburl"]}{config_file["node"]}"
    timestamp = int(round(datetime.now().timestamp()))
    payload = {"sender": sender, "receiver": receiver, "body": message, "timestamp": timestamp}

    url_lst = [f"{URL}/recent/{receiver}.json",
    f"{URL}/recent/{sender}.json",
    f"{URL}/{sender}/all/{receiver}/{timestamp}.json",
    f"{URL}/{receiver}/all/{sender}/{timestamp}.json"]

    for u in url_lst:
        if f"{URL}/recent/" in u:
            res = requests.put(u, json = payload)
        else:
            res = requests.patch(u, json = payload)
        
        if res.status_code != 200:
            return res.status_code
    
    return res.status_code

# 2. Retrieve the most recent message for a person
def get_recent_message(person):
    # INPUT : Person (as sender or receiver)
    # RETURN : JSON object with details of the most recent message or None if no message exists
    # EXPECTED RETURN : {"sender": "john", "receiver": "david", "body": "hello", "timestamp": 1674539458} or None
    config_file = config_load(CONFIG_FILE)
    URL = f'{config_file["dburl"]}{config_file["node"]}/recent/{person}/.json'
    res = requests.get(f'{URL}')
    _dict = json.loads(res.text)

    if _dict:
        return _dict
    return None

# 3. Retrieve the last k messages between two people
def get_last_k_messages(person1, person2, k):
    # INPUT : Person1, Person2, Number of messages (k)
    # RETURN : List of JSON objects with the k most recent messages or an Empty list if no messages exist
    # EXPECTED RETURN : [{"sender": "john", "receiver": "david", "body": "nothing much, how about we go out?", "timestamp": 1737676770}, ...] or []
    chat_dict = {}
    config_file = config_load(CONFIG_FILE)
    URL = f'{config_file["dburl"]}{config_file["node"]}/{person1}/all/{person2}/.json?orderBy="$key"&limitToLast={k}'
    res = requests.get(f'{URL}')
    _dict = json.loads(res.text)

    if _dict:
        for key, value in _dict.items():
            chat_dict.update({int(key): value})

    if chat_dict:
        ans = [value for value in chat_dict.values()][::-1]
    else:
        ans = []
    return ans

# Main execution logic
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python John_Smith_hw1.py [operation] [arguments]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "send_message":
        sender = sys.argv[2]
        receiver = sys.argv[3]
        message = sys.argv[4]
        result = send_chat_message(sender, receiver, message)
        print(result)
    
    elif command == "get_recent":
        person = sys.argv[2]
        result = get_recent_message(person)
        print(result)
    
    elif command == "get_last_k":
        person1 = sys.argv[2]
        person2 = sys.argv[3]
        k = int(sys.argv[4])
        result = get_last_k_messages(person1, person2, k)
        print(result)
    
    else:
        print("Invalid command. Use 'send_message', 'get_recent', or 'get_last_k'.")

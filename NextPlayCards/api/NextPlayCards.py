import requests
from flask import Flask, request, jsonify, Response
import subprocess
import sys
import os
#sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import time
from dotenv import load_dotenv
load_dotenv()
from GetDatabase import playerDataGet, playerDataUpdate # type: ignore
print('Getting or installing necessary modules')   
try:
    import requests
    print('module requests is installed')
except ModuleNotFoundError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'requests'])

try:
    import werkzeug
    print('module werkzeug is installed')
except ModuleNotFoundError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'werkzeug'])

    
key = os.getenv('key')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def raid_webhook():
    if request.method == "GET":
        name = request.args.get('name')
        password = request.args.get('password')
        type = request.args.get('type')
        amount = request.args.get('amount', default=0, type=int)

        if not name:
            return 'Empty name', 400
        if not password:
            return 'Empty key', 400
        if not type:
            return 'Empty type', 400
        
        if password == key and type == "get":
            print("Key is correct")
            result = GetDatabase(name)
            return jsonify(result)

        elif password == key and type == "update":
             if request.args.get('amount') is None:
                return 'Missing amount for update', 400
             else:
                print("Key is correct")
                UpdateDatabase(name, amount)
                return jsonify({'message': 'Updated successfully', 'player_name': name})

    return Response("Not Found", status=404)

def GetDatabase(selected_name):
    db_values = playerDataGet(selected_name)
    
    if isinstance(db_values, dict) and 'error' in db_values:
        print('Database connection failed or error:', db_values['error'])
        return {'error': 'Database connection failed or error'}

    if db_values is None:
        print(f'Player {selected_name} not found in database')
        # Optionally, initialize player with amount 0
        UpdateDatabase(selected_name, 0)
        return {
            'player_name': selected_name,
            'player_amount': 0
        }

    current_name = db_values['player_name']
    current_amount = db_values['player_amount']

    print(f'Current amount {current_amount} for player {current_name}')
    return {
        'player_name': current_name,
        'player_amount': current_amount
    }

def UpdateDatabase(selected_name, amount=0):
    db_values  =  playerDataUpdate(selected_name,amount)
    print(f"PlayerData: {db_values}")
    if db_values == None:
        print('Database is empty')
        return 'Database is empty'
    else:
        print("updated successfully")

       
if __name__ == '__main__':
    app.run()

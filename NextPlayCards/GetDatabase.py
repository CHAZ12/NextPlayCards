from flask import Flask, jsonify
import psycopg2
import os
from dotenv import load_dotenv
#from config import config
load_dotenv
app = Flask(__name__)


# Retrieve database configuration from environment variables
db_config = {
    'host': os.getenv('POSTGRES_HOST'),
    'database': os.getenv('POSTGRES_DATABASE'),
    'port': int(5432),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD')
}

def connect():
    try:
        #params = config()
        params = db_config
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        return connection, cursor
    except (Exception, psycopg2.DatabaseError) as error:
        print(f'Database connection failed connect: {error}')
        return None, None

def playerDataGet(name):
    connection, cursor = connect()
    if connection is None or cursor is None:
        print({'error': 'Database connection failed get data'}, 500)
        return {'error': 'Database connection failed'}
    try:
        print("GETTING DATABASE VALUES FOR:", name)
        cursor.execute('SELECT player_name, player_amount FROM playerdata WHERE player_name = %s', (name,))
        row = cursor.fetchone()
        if row is None:
            print(f"No data found for player: {name}")
            return None  # Or return {'player_name': name, 'player_amount': 0}
        row_dict = {
            'player_name': row[0],
            'player_amount': row[1]
        }
        return row_dict
    except Exception as e:
        print(f"Error fetching data: {e}")
        return {'error': str(e)}
    finally:
        cursor.close()
        connection.close()
    
def playerDataUpdate(name, amount):
    connection, cursor = connect()
    if connection is None or cursor is None:
        print({'error': 'Database connection failed get update'}, 500)
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        # Check if the player already exists
        cursor.execute('SELECT * FROM playerdata WHERE player_name = %s', (name,))
        row = cursor.fetchone()

        if not row:
            print("Player not found — inserting new player")
            cursor.execute(
                'INSERT INTO playerdata (player_name, player_amount) VALUES (%s, %s)',
                (name, amount)
            )
        else:
            print("Player found — updating existing player")
            cursor.execute(
                'UPDATE playerdata SET player_amount = %s WHERE player_name = %s',
                (amount, name)
            )

        connection.commit()
        return 'Database updated successfully'

    except (Exception, psycopg2.DatabaseError) as e:
        print(f"An error occurred: {e}")
        return 'Database update failed'

    finally:
        connection.close()
if __name__ == '__main__':
    app.run(debug=True)

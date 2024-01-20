import socketio

# Standard Python client based on the socketio package
sio = socketio.Client()

# The server URL, assuming it's running locally on port 5000
SERVER_URL = 'http://localhost:5000'

# Class for individual moves (should match the server's definition)
class Move:
    def _init_(self, position, movement_type=1, french_revolution=False, spawn_piece=None):
        self.position = position
        self.french_revolution = french_revolution
        self.movement_type = movement_type

@sio.event
def connect():
    print('Connected to the server.')
    # Try to find a game immediately upon connection
    sio.emit('find_game')

@sio.event
def disconnect():
    print('Disconnected from the server.')

@sio.on('joined_game')
def on_joined_game(data):
    print('Joined game with ID:', data['game_id'])
    # Save the game ID for later use
    global game_id
    game_id = data['game_id']

    # Here, you would wait for the opponent or start making moves
    # For example purposes, let's send a dummy move:
    move = Move(position='e2e4') # Standard chess notation
    make_move(move)

@sio.on('move_made')
def on_move_made(move):
    print('Opponent made a move:', move)
    # Update the game state with the opponent's move

def make_move(move):
    # Send a move to the server
    sio.emit('make_move', {'game_id': game_id, 'move': move._dict_})

if __name__ == '__main__':
    try:
        sio.connect(SERVER_URL)
    except socketio.exceptions.ConnectionError as err:
        print("Connection failed:", err)
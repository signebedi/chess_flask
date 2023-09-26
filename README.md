# chess_flask
a RESTful chess API 


### Examples

```python
import requests
import json

# Base URL
base_url = "http://127.0.0.1:5000"

# 1. Create a new game
response = requests.post(f"{base_url}/game")
if response.status_code == 201:
    game_data = response.json()
    game_id = game_data['game_id']
    print(f"Game {game_id} created successfully")
else:
    print(f"Failed to create game: {response.content}")

# 2. Make a move in the created game
move_data = {
    "move": "e2e4",
    "player": "w"
}
response = requests.put(f"{base_url}/game/{game_id}/move", json=move_data)
if response.status_code == 200:
    print("Move made successfully")
else:
    print(f"Failed to make move: {response.content}")

# 3. Get moves made in the game so far
response = requests.get(f"{base_url}/game/{game_id}/moves")
if response.status_code == 200:
    moves_data = response.json()
    moves = moves_data['moves']
    print(f"Moves: {moves}")
else:
    print(f"Failed to retrieve moves: {response.content}")

# 4. Get the position after a specific move number
move_number = 1
response = requests.get(f"{base_url}/game/{game_id}/position/{move_number}")
if response.status_code == 200:
    position_data = response.json()
    position = position_data['position']
    print(f"Position: {position}")
    print("Game: \n", position_data['board'])
else:
    print(f"Failed to retrieve position: {response.content}")
```
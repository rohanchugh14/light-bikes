import requests
import json
DIRECTION_OFFSETS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
def main():
  url = 'http://light-bikes.inseng.net/games'
  # res = requests.get('http://light-bikes.inseng.net/games')
  res = requests.post(f'{url}?addServerBot=true&boardSize=25&numPlayers=2&serverBotDifficulty=1')
  # convert to json
  data = res.json()
  print(data)
  game_id = data['id']

  res = requests.post(f'{url}/{game_id}/join?name=rohan')
  data = res.json()
  data = data[0]

  for datum in data:
    print(datum)
  print("players:", data['players'])
  board = data['board']
  print("player info:", data['current_player'])
  player_id = data['current_player']['id']
  # for row in board:
  #   print(row)
  while(data['winner'] == None):
    curr_loc = data['current_player']['x'], data['current_player']['y']
    print(curr_loc)
    x, y = get_best_direction(board, curr_loc)
    print(x,y)
    res = requests.post(f'{url}/{game_id}/move?playerId={player_id}&x={x}&y={y}')
    data = res.json()
    data = data[0]
    board = data['board']

def get_best_direction(board, curr_loc):
  # explore each direction and return the direction that has the most open spaces
  # where positive x is down and positive y is right
  # check up
  max_spaces = -1
  best_offset = None
  for offset in DIRECTION_OFFSETS:
    x, y = curr_loc
    spaces = 0
    x += offset[0]
    y += offset[1]
    while x >= 0 and y >= 0 and x < len(board) and y < len(board[0]) and board[x][y] == None:
      x += offset[0]
      y += offset[1]
      spaces += 1
    if(spaces > max_spaces):
      max_spaces = spaces
      best_offset = offset
  return (curr_loc[0] + best_offset[0], curr_loc[1] + best_offset[1])




  # # check up
  # while board[x][y] == None:
  #   up += 1
  #   x -= 1
  # if up > max_spaces:
  #   max_spaces = up
  #   updated_loc = (x + up - 1, y)
  # x, y = curr_loc
  # # check down
  # while board[x][y] == None:
  #   down += 1
  #   x += 1
  # if down > max_spaces:
  #   max_spaces = down
  #   updated_loc = (x - down + 1, y)

  # x, y = curr_loc
  # # check left
  # while board[x][y] == None:
  #   left += 1
  #   y -= 1
  # if left > max_spaces:
  #   max_spaces = left
  #   updated_loc = (x, y + left - 1)

  # x, y = curr_loc
  # # check right
  # while board[x][y] == None:
  #   right += 1
  #   y += 1
  # if right > max_spaces:
  #   max_spaces = right
  #   updated_loc = (x, y - right + 1)
  # return updated_loc
if __name__ == '__main__':
  main()
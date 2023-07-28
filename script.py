import requests
import json
DIRECTION_OFFSETS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
def main():
  url = 'http://light-bikes.inseng.net/games'
  # res = requests.get('http://light-bikes.inseng.net/games')
  res = requests.post(f'{url}?addServerBot=true&boardSize=50&numPlayers=2&serverBotDifficulty=2')
  # convert to json
  data = res.json()
  print(data)
  game_id = data['id']
  # game_id = 740
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
  # x, y = curr_loc
  # check if starting on wall
  # wall = get_wall(board, curr_loc)
  # if wall 
  found = False
  wall_offset = None
  while(data['winner'] == None):
    players = data['players']
    enemy_player = [player for player in players if player['name'] != data['current_player']['name']][0]
    enemy_loc = enemy_player['x'], enemy_player['y']
    curr_loc = data['current_player']['x'], data['current_player']['y']
    print(curr_loc)
    # x, y = get_best_direction(board, curr_loc)
    x, y, found, wall_offset = get_next_move(board, curr_loc, enemy_loc, found, wall_offset)
    print(x,y)
    res = requests.post(f'{url}/{game_id}/move?playerId={player_id}&x={x}&y={y}')
    data = res.json()
    data = data[0]
    board = data['board']

def get_next_move(board, curr_loc, enemy_loc, found, wall_offset):
  x, y = curr_loc
  enemy_x, enemy_y = enemy_loc
  x_diff = enemy_x - x
  y_diff = enemy_y - y
  if abs(x_diff) <= 1 and abs(y_diff) <= 1 or found:
    if(wall_offset != None):
      print("wall offset:", wall_offset)
      return (x + wall_offset[0], y + wall_offset[1], True, wall_offset)
    wall_offset = get_best_direction(board, curr_loc)
    print("wall offset:", wall_offset)
    return (x + wall_offset[0], y + wall_offset[0], True, wall_offset)
  if abs(x_diff) > abs(y_diff):
    if x_diff > 0:
      return (x + 1, y, False, None)
    else:
      return (x - 1, y, False, None)
  else:
    if y_diff > 0:
      return (x, y + 1, False, None)
    else:
      return (x, y - 1, False, None)

def get_wall(board, curr_loc):
  x, y = curr_loc
  if x == 0:
    return 'top'
  if y == 0:
    return 'left'
  if x == len(board) - 1:
    return 'bottom'
  if y == len(board[0]) - 1:
    return 'right'
  return 'middle'



def get_best_direction(board, curr_loc):
  # explore each direction and return the direction that has the most open spaces
  # where positive x is down and positive y is right
  # check up
  return find_nearest_wall(board, curr_loc)
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

def find_nearest_wall(board, curr_loc):
  # find the nearest wall
  # where positive x is down and positive y is right
  # check up
  # [left, right, top, bottom]
  # offsets to get to left, right, top, and bottom wall:
  offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]
  dists = [curr_loc[0], len(board[0]) - curr_loc[1], curr_loc[1], len(board) - curr_loc[0]]
  max_dist_index = dists.index(min(dists))
  return offsets[max_dist_index]
  return (curr_loc[0] + offsets[max_dist_index][0], curr_loc[1] + offsets[max_dist_index][1])



if __name__ == '__main__':
  main()
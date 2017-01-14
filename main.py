import random
import itertools
import math

class Illegal(Exception):
    pass

# field states
COVERED = 0
UNCOVERED = 1
FLAGGED = 2

#
MINE = -1

class Minesweeper:
  
  def __init__(self, height=10, width=10, mines=15):
    self.height = height
    self.width = width
    self.mines = mines

    self.grid = [[0 for _ in range(width)] for _ in range(height)]
    self._place_mines()
    for (i, j) in self.fields():
      if self.grid[i][j] == MINE: continue
      for (k,l) in self.neighbors(i, j):
        if self.grid[k][l] == MINE: 
          self.grid[i][j] += 1

    self.state_grid = [[COVERED for _ in range(width)] for _ in range(height)]

  def _place_mines(self):
    random.seed()
    for _ in range(self.mines):
      while True:
        (i, j) = (random.randrange(self.height), random.randrange(self.width))
        if self.grid[i][j] != MINE: break
      self.grid[i][j] = MINE

  def neighbors(self, i, j):
    """Returns the neighbor fields to a given field, _including_ itself!"""
    rows = range(max(i-1, 0), min(i+2, self.height))
    cols = range(max(j-1, 0), min(j+2, self.width))
    return itertools.product(rows, cols)

  def uncover(self, i, j):
    if self.state_grid[i][j] != COVERED:
      raise Illegal
    self.state_grid[i][j] = UNCOVERED
    if self.grid[i][j] != MINE and self.grid[i][j] == 0:
      self._uncover_cascade(i, j)

  def flag(self, i, j):
    if self.state_grid[i][j] != COVERED:
      raise Illegal
    self.state_grid[i][j] = FLAGGED

  def unflag(self, i, j):
    if self.state_grid[i][j] != FLAGGED:
      raise Illegal
    self.state_grid[i][j] = COVERED

  def game_lost(self):
    for (i, j) in self.fields():
      if self.grid[i][j] == MINE and self.state_grid[i][j] == UNCOVERED:
        return True
    return False

  def game_won(self):
    for (i, j) in self.fields():
      if self.grid[i][j] == MINE and self.state_grid[i][j] != FLAGGED:
        return False
      if self.grid[i][j] != MINE and self.state_grid[i][j] != UNCOVERED:
        return False
    return True

  def game_over(self):
    return self.game_lost() or self.game_won()

  def _uncover_cascade(self, i, j):
    todo = set(self.neighbors(i, j))
    while todo:
      (k, l) = todo.pop()
      if self.state_grid[k][l] != COVERED or self.grid[k][l] == MINE:
        continue
      
      self.state_grid[k][l] = UNCOVERED
      if self.grid[k][l] == 0:
        todo.update(self.neighbors(k, l))

  def fields(self):
    return itertools.product(range(self.height), range(self.width))

  def str_of_field(self, i, j, game_over=False):
    if self.state_grid[i][j] == COVERED and not game_over:
      return "[" + str(i*self.width + j) + "]"
    elif self.state_grid[i][j] == FLAGGED:
      if game_over and self.grid[i][j] != MINE:
        return "WF"
      return "F"
    elif self.state_grid[i][j] == UNCOVERED or game_over:
      if self.grid[i][j] == MINE:
        return "M"
      if self.grid[i][j] == 0:
        return "."
      else:
        return str(self.grid[i][j])
    else:
      raise Exception

  def __str__(self, game_over=False):
    field_width = math.floor(math.log((self.width+1) * (self.height+1), 10)) + 2
    f = (('{:^' + str(field_width) + '}') * self.width + '\n') * self.height
    return f.format(*(self.str_of_field(i,j, game_over) for (i,j) in self.fields()))
    

####################################################################################################

def try_input_until(prompt, p=lambda _: True):
  while True:
    try:
      inp = input(prompt)
    except:
      continue
    if p(inp):
      return inp

def custom_game_prompt():
  prompt = "Width?\n>> "
  inp = try_input_until(prompt, lambda s: s.isdigit() and (int(s) in range(1, 100)))
  width = int(inp)

  prompt = "Height?\n>> "
  inp = try_input_until(prompt, lambda s: s.isdigit() and (int(s) in range(1, 100)))
  height = int(inp)

  prompt = "Mines?\n>> "
  inp = try_input_until(prompt, lambda s: s.isdigit() and (int(s) in range(0, height*width)))
  mines = int(inp)

  return Minesweeper(height=height, width=width, mines=mines)

width = 80
while True:
  print("\n")
  print("#"*width)
  print(('{:#^' + str(width) + '}').format('  MINESWEEPER  '))
  print("#"*width)
  prompt = "What do you wanna do?\n\t(1) Quick Game\n\t(2) Custom Game\n\t(3) Exit\n>> "
  inp = try_input_until(prompt, lambda s: s.isdigit() and (int(s) in range(1,4)))
  inp = int(inp)
  if inp == 1:
    game = Minesweeper()
  elif inp == 2:
    game = custom_game_prompt()
  else:
    print("\n")
    break

  while not game.game_over():
    print("#"*width)
    print(game)

    prompt = "What do you wanna do?\n\t(1) Uncover\n\t(2) Flag\n\t(3) Unflag\n\t(4) Give Up\n>> "
    inp = try_input_until(prompt, lambda s: s.isdigit() and (int(s) in range(1,5)))
    action = int(inp)

    if action == 4:
      break
    prompt = "Position?\n>> "
    inp = try_input_until(prompt, lambda s: s.isdigit() and (int(s) in range(0,game.width*game.height)))
    pos = int(inp)
    i = pos // game.width
    j = pos % game.width
    if action == 1:
      game.uncover(i, j)
    elif action == 2:
      game.flag(i, j)
    elif action == 3:
      game.unflag(i, j)
    else:
      raise Exception

  print("#"*width)
  print("#"*width)
  print(game.__str__(True))
  if(game.game_won()):
    print("WINNER WINNER CHICKEN DINNER!!")
  elif(game.game_lost()):
    print("You lost, sucker!")
  try_input_until("Press enter to continue. ")

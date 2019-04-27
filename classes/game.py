import pygame

class Player:
    def __init__(self, id):
        self._id = id
    
    def get_id(self):
        return self._id

    def get_color(self):
        if self._id == 0:
            return (255,0,0)
        else:
            return (255,255,0)

    def get_name(self):
        if self._id == 0:
            return "Red"
        else:
            return "Yellow"

class Board:

  def __init__(self):
    self.ROWS = 6
    self.COLUMNS = 7
    self.clear()

  def clear(self):
    self._grid = [[None for i in range(self.COLUMNS)] for j in range(self.ROWS)]   

  def check_player_wins(self, player):

    id = player.get_id()
    
    # Check horizontal
    for c in range(self.COLUMNS-3):
      for r in range(self.ROWS):
        if self._grid[r][c] == id and self._grid[r][c+1] == id and self._grid[r][c+2] == id and self._grid [r][c+3] == id:
          return True

    # Check vertical
    for c in range(self.COLUMNS):
      for r in range(self.ROWS-3):
        if self._grid[r][c] == id and self._grid[r+1][c] == id and self._grid[r+2][c] == id and self._grid [r+3][c] == id:
          return True

    # Check positive diagonal
    for c in range(self.COLUMNS-3):
      for r in range(self.ROWS-3):
        if self._grid[r][c] == id and self._grid[r+1][c+1] == id and self._grid[r+2][c+2] == id and self._grid[r+3][c+3] == id:
          return True

    # Check negavtive diagonal
    for c in range(self.COLUMNS-3):
      for r in range(3, self.ROWS):
        if self._grid[r][c] == id and self._grid[r-1][c+1] == id and self._grid[r-2][c+2] == id and self._grid[r-3][c+3] == id:
          return True

    return False

  def add_chip(self, player, column):

    for row in range(self.ROWS):
      cell_value = self._grid[row][column]
      if cell_value is None:
        self._grid[row][column] = player.get_id()
        return row
        
    return -1

class GameUI:

  def __init__(self, game):
    self.CHIP_SIZE = 80
    self.OFFSET = 60
    self.CHIP_OFFSET = 20
    self.BOARD_HEIGHT = 600
    self.CHIP_RADIUS = int(self.CHIP_SIZE / 2)

    self._game = game

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Connect 4 with Python')

    self._screen = pygame.display.set_mode((800, 700))
    self._board_img = pygame.image.load("./img/board.png")
    self._board_img_numbers = pygame.image.load("./img/board_numbers.png")
    self._font = pygame.font.SysFont('Calibri', 26)

    self.init_ui()

  def init_ui(self):
    self._screen.fill((255, 255, 255))
    self.draw_board()
    self.draw_player()  
    
  def draw_player_won(self, player):
      pygame.draw.rect(self._screen, (255,255,255), [0, 0, 800, 50], 0)

      text = player.get_name() + " won! Restart (y | n)?"
      
      text = self._font.render(text, True, (0,0,0))
      self._screen.blit(text, (50, 10))

      pygame.display.flip()

  def draw_player(self):

      pygame.draw.rect(self._screen, (255,255,255), [0, 0, 800, 50], 0)

      text = "Current Player: " + self._game.get_current_player().get_name()
      
      text = self._font.render(text, True, (0,0,0))
      self._screen.blit(text, (50, 10))

      pygame.display.flip()

  def draw_board(self, player = None, row = -1, column = -1):

    if player is not None:

      pygame.draw.circle(self._screen, player.get_color(), 
      (self.OFFSET + self.CHIP_RADIUS + self.CHIP_OFFSET * column + self.CHIP_SIZE * column, 
       self.BOARD_HEIGHT - self.CHIP_SIZE * row - self.CHIP_OFFSET * row), self.CHIP_RADIUS)
 
    self._screen.blit(self._board_img, (self.OFFSET - 10, self.OFFSET - 10))
    self._screen.blit(self._board_img_numbers, (self.OFFSET + self.CHIP_RADIUS - 10, self.OFFSET + self.BOARD_HEIGHT - 5))

    pygame.display.flip()

  
class Game:

  def __init__(self):
    self._current_player = 0
    self._players = [Player(0), Player(1)]
    self._board = Board()
    self._gameUI = GameUI(self)

  def game_loop(self):
    valid_keys = [1,2,3,4,5,6,7]
    
    update_ui = False
    done = False
    player_won = False

    row = -1
    column = -1

    while not done:

      # check for player input events
      for event in pygame.event.get():

        if event.type == pygame.QUIT:
          done = True

        elif event.type == pygame.KEYUP:

          if player_won:

            # N key
            if event.key == 110:
              done = True

            # Y key
            elif event.key in [121,122]:
              
              player_won = False
              done = False
              self.restart()

          else:
            column = (event.key - 49)
            if column+1 in valid_keys:
              row = self.add_chip(column)
              if row > -1:
                player_won = self.check_player_wins(self.get_current_player())
                update_ui = True
            else:
              update_ui = False

      # UI has to be updated
      if update_ui:
        self._gameUI.draw_board(self.get_current_player(), row, column)

        if player_won:
          self._gameUI.draw_player_won(self.get_current_player())
        else:
          self.switch_player()
          self._gameUI.draw_player()

        update_ui = False
        

  def switch_player(self):
    self._current_player += 1
    self._current_player = self._current_player % 2

  def restart(self):
    self._board.clear()
    self._gameUI.init_ui()

  def add_chip(self, column):
    player = self.get_current_player()
    return self._board.add_chip(player, column)

  def check_player_wins(self, player):
    return self._board.check_player_wins(player)

  def get_board(self):
    return self._board

  def get_player(self, id):
    return self._players[id]

  def get_current_player(self):
      return self._players[self._current_player]
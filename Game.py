# Basic arcade program
# Displays a black window with a spaceship sprite

# Imports
import arcade

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Spaceship Battle"

class gameWindow(arcade.Window):
  def __init__(self):
    super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_background_color(arcade.color.BLACK)

    self.player_list = None
    self.planet_list = None
    self.bullet_list = None
  
  def setup(self):

    self.player_list = arcade.SpriteList()
    self.planet_list = arcade.SpriteList(use_spatial_hash = True)
    self.bullet_list = arcade.SpriteList()

    self.player_sprite = arcade.Sprite("sprites/spiked ship.png", 0.5)
    self.player_sprite.center_x = 200
    self.player_sprite.center_y = 200
    self.player_list.append(self.player_sprite)

  def on_draw(self):
    arcade.start_render()

    self.player_list.draw()
    self.planet_list.draw()
    self.bullet_list.draw()

def main():
  window = gameWindow()
  window.setup()
  arcade.run()

if __name__ == "__main__":
   main()
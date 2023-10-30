# Basic arcade program
# Displays a black window with a spaceship sprite

# Imports
import arcade

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Spaceship Battle"
PLAYER_MOVEMENT_SPEED = 5

class gameWindow(arcade.Window):
  def __init__(self):
    super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_background_color(arcade.color.BLACK)

    self.player_list = None
    self.planet_list = None
    self.bullet_list = None
    self.physics_engine = None
  
  def setup(self):

    self.player_list = arcade.SpriteList()
    self.planet_list = arcade.SpriteList(use_spatial_hash = True)
    self.bullet_list = arcade.SpriteList()

    self.player_sprite = arcade.Sprite("sprites/spiked ship.png", 0.5)
    self.player_sprite.center_x = 200
    self.player_sprite.center_y = 200
    self.player_list.append(self.player_sprite)

    # Create the 'physics engine'
    self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.planet_list)

  def on_key_press(self, key, modifiers):
    """Called whenever a key is pressed."""
    if key == arcade.key.UP or key == arcade.key.W:
      self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
    elif key == arcade.key.DOWN or key == arcade.key.S:
      self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
    elif key == arcade.key.LEFT or key == arcade.key.A:
      self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
    elif key == arcade.key.RIGHT or key == arcade.key.D:
      self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

  def on_key_release(self, key, modifiers):
    """Called when the user releases a key."""

    if key == arcade.key.UP or key == arcade.key.W:
      self.player_sprite.change_y = 0
    elif key == arcade.key.DOWN or key == arcade.key.S:
      self.player_sprite.change_y = 0
    elif key == arcade.key.LEFT or key == arcade.key.A:
      self.player_sprite.change_x = 0
    elif key == arcade.key.RIGHT or key == arcade.key.D:
      self.player_sprite.change_x = 0

  def on_update(self, delta_time):
    """Movement and game logic"""

    # Move the player with the physics engine
    self.physics_engine.update()

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
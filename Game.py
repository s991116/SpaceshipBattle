# Basic arcade program
# Displays a black window with a spaceship sprite

# Imports
import arcade
import math
from typing import Optional
from arcade.pymunk_physics_engine import PymunkPhysicsEngine

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Spaceship Battle"
PLAYER_MOVEMENT_SPEED = 5
PLAYER_MOVE_FORCE = 3000
PLAYER_ANGLE_STEP = 5
BULLET_SPEED = 10
class gameWindow(arcade.Window):
  def __init__(self):
    super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_background_color(arcade.color.BLACK)

    self.player_list = None
    self.planet_list = None
    self.bullet_list = None
    self.physics_engine: Optional[PymunkPhysicsEngine] = None
  
    # Track the current state of what key is pressed
    self.left_pressed = False
    self.right_pressed = False
    self.up_pressed = False
    self.down_pressed = False
    self.fire_pressed = False

  def setup(self):

    self.player_list = arcade.SpriteList()
    self.planet_list = arcade.SpriteList(use_spatial_hash = True)
    self.bullet_list = arcade.SpriteList()

    self.player_sprite = arcade.Sprite("sprites/spiked ship.png", 0.5)
    self.player_sprite.center_x = 200
    self.player_sprite.center_y = 200
    self.player_list.append(self.player_sprite)

    gravity = (0, 0)
    damping = 0.8

    # Create the physics engine
    self.physics_engine = PymunkPhysicsEngine(damping=damping, gravity=gravity)

    self.physics_engine.add_sprite(self.player_sprite,
                                       friction=1.0,
                                       moment=PymunkPhysicsEngine.MOMENT_INF,
                                       damping=0.8,
                                       collision_type="player",
                                       max_velocity=400)

  def on_key_press(self, key, modifiers):
      """Called whenever a key is pressed. """
      if key == arcade.key.UP:
          self.up_pressed = True
      elif key == arcade.key.DOWN:
          self.down_pressed = True
      elif key == arcade.key.LEFT:
          self.left_pressed = True
      elif key == arcade.key.RIGHT:
          self.right_pressed = True
      elif key == arcade.key.SPACE:
          self.fire_pressed = True

  def on_key_release(self, key, modifiers):
      """Called when the user releases a key. """
      if key == arcade.key.UP:
          self.up_pressed = False
      elif key == arcade.key.DOWN:
          self.down_pressed = False
      elif key == arcade.key.LEFT:
          self.left_pressed = False
      elif key == arcade.key.RIGHT:
          self.right_pressed = False
      elif key == arcade.key.SPACE:
          self.fire_pressed = False

  def on_update(self, delta_time):
    # Calculate speed based on the keys pressed
    self.player_sprite.change_x = 0
    self.player_sprite.change_y = 0
  
    if self.up_pressed and not self.down_pressed:
        angle_radians = math.radians(self.player_sprite.angle) + math.pi/2.0
        force = (math.cos(angle_radians)*PLAYER_MOVE_FORCE, math.sin(angle_radians)*PLAYER_MOVE_FORCE)
        self.physics_engine.apply_force(self.player_sprite, force)
    elif self.down_pressed and not self.up_pressed:
        angle_radians_opposite = math.radians(self.player_sprite.angle) + math.pi + math.pi/2.0
        force = (math.cos(angle_radians_opposite)*PLAYER_MOVE_FORCE, math.sin(angle_radians_opposite)*PLAYER_MOVE_FORCE)
        self.physics_engine.apply_force(self.player_sprite, force)

    # --- Move items in the physics engine
    self.physics_engine.step()

    if self.left_pressed and not self.right_pressed:
        self.player_sprite.change_angle += PLAYER_ANGLE_STEP
    elif self.right_pressed and not self.left_pressed:
        self.player_sprite.change_angle += -PLAYER_ANGLE_STEP
    
    #Fire pressed
    if self.fire_pressed:
      bullet = arcade.Sprite("sprites/bullet.png", 1)
      start_x = self.player_sprite.center_x
      start_y = self.player_sprite.center_y
      bullet.center_x = start_x
      bullet.center_y = start_y
      start_angle = self.player_sprite.change_angle + 90

      start_angle_radian = math.radians(start_angle)
      bullet.change_x = math.cos(start_angle_radian) * BULLET_SPEED
      bullet.change_y = math.sin(start_angle_radian) * BULLET_SPEED
      self.bullet_list.append(bullet)

    self.player_list.update()
    self.bullet_list.update()

    # If the bullet flies off-screen, remove it.
    for bullet in self.bullet_list:
      if bullet.bottom > self.width or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width:
          bullet.remove_from_sprite_lists()



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
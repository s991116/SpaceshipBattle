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


class SpaceshipOne:
    def __init__(self):
        self.MovementSpeed = 5
        self.MoveForce = 3000
        self.PlayerAngleStep = 5
        self.BulletSpeed = 10
        self.Sprite = arcade.Sprite("sprites/spiked ship.png", 0.5)
        self.Sprite.center_x = 200
        self.Sprite.center_y = 200

class ControllerState:
    def __init__(self):
        self.LeftPressed = False
        self.RightPressed = False
        self.UpPressed = False
        self.DownPressed = False
        self.FirePressed = False

    def keyReleased(self, key):
        if key == arcade.key.UP:
            self.UpPressed = False
        elif key == arcade.key.DOWN:
            self.DownPressed = False
        elif key == arcade.key.LEFT:
            self.LeftPressed = False
        elif key == arcade.key.RIGHT:
            self.RightPressed = False
        elif key == arcade.key.SPACE:
            self.FirePressed = False

    def keyPressed(self, key):
        if key == arcade.key.UP:
            self.UpPressed = True
        elif key == arcade.key.DOWN:
            self.DownPressed = True
        elif key == arcade.key.LEFT:
            self.LeftPressed = True
        elif key == arcade.key.RIGHT:
            self.RightPressed = True
        elif key == arcade.key.SPACE:
            self.FirePressed = True
        

class gameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        self.scene = None

        self.player_spaceship = SpaceshipOne()

        # self.player_sprite = None

        self.physics_engine: Optional[PymunkPhysicsEngine] = None

        # Track the current state of what key is pressed
        self.controllerState = ControllerState()

    def setup(self):
        self.scene = arcade.Scene()

        self.scene.add_sprite_list

        self.scene.add_sprite_list("Planet", use_spatial_hash=True)
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Bullet", use_spatial_hash=False)

        self.scene.add_sprite("Player", self.player_spaceship.Sprite)

        planet = arcade.Sprite("sprites/planet.png", 1.0)
        planet.center_x = 100
        planet.center_y = 50
        self.scene.add_sprite("Planet", planet)

        gravity = (0, 0)
        damping = 0.8

        # Create the physics engine
        self.physics_engine = PymunkPhysicsEngine(damping=damping, gravity=gravity)

        self.physics_engine.add_sprite(
            self.player_spaceship.Sprite,
            friction=1.0,
            moment=PymunkPhysicsEngine.MOMENT_INF,
            damping=0.8,
            collision_type="player",
            max_velocity=400,
        )

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        self.controllerState.keyPressed(key)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        self.controllerState.keyReleased(key)

    def on_update(self, delta_time):
        # Calculate speed based on the keys pressed
        self.player_spaceship.Sprite.change_x = 0
        self.player_spaceship.Sprite.change_y = 0

        if self.controllerState.UpPressed and not self.controllerState.DownPressed:
            angle_radians = (
                math.radians(self.player_spaceship.Sprite.angle) + math.pi / 2.0
            )
            force = (
                math.cos(angle_radians) * self.player_spaceship.MoveForce,
                math.sin(angle_radians) * self.player_spaceship.MoveForce,
            )
            self.physics_engine.apply_force(self.player_spaceship.Sprite, force)
        elif self.controllerState.DownPressed and not self.controllerState.UpPressed:
            angle_radians_opposite = (
                math.radians(self.player_spaceship.Sprite.angle)
                + math.pi
                + math.pi / 2.0
            )
            force = (
                math.cos(angle_radians_opposite) * self.player_spaceship.MoveForce,
                math.sin(angle_radians_opposite) * self.player_spaceship.MoveForce,
            )
            self.physics_engine.apply_force(self.player_spaceship.Sprite, force)

        # --- Move items in the physics engine
        self.physics_engine.step()

        if self.controllerState.LeftPressed and not self.controllerState.RightPressed:
            self.player_spaceship.Sprite.change_angle += (
                self.player_spaceship.PlayerAngleStep
            )
        elif self.controllerState.RightPressed and not self.controllerState.LeftPressed:
            self.player_spaceship.Sprite.change_angle += (
                -self.player_spaceship.PlayerAngleStep
            )

        # Fire pressed
        if self.controllerState.FirePressed:
            bullet = arcade.Sprite("sprites/bullet.png", 1)
            start_x = self.player_spaceship.Sprite.center_x
            start_y = self.player_spaceship.Sprite.center_y
            bullet.center_x = start_x
            bullet.center_y = start_y
            start_angle = self.player_spaceship.Sprite.change_angle + 90

            start_angle_radian = math.radians(start_angle)
            bullet.change_x = (
                math.cos(start_angle_radian) * self.player_spaceship.BulletSpeed
            )
            bullet.change_y = (
                math.sin(start_angle_radian) * self.player_spaceship.BulletSpeed
            )
            self.scene.add_sprite("Bullet", bullet)

        self.scene.get_sprite_list("Player").update()
        self.scene.get_sprite_list("Bullet").update()

        # If the bullet flies off-screen, remove it.
        for bullet in self.scene.get_sprite_list("Bullet"):
            if (
                bullet.bottom > self.width
                or bullet.top < 0
                or bullet.right < 0
                or bullet.left > self.width
            ):
                bullet.remove_from_sprite_lists()

    def on_draw(self):
        # Clear the screen to the background color
        self.clear()

        # Draw our Scene
        self.scene.draw()


#    arcade.start_render()
#    self.player_list.draw()
#    self.planet_list.draw()
#    self.bullet_list.draw()


def main():
    window = gameWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

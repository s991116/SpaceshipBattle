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

class ControllerKeys:
    def __init__(self, upKey, downKey, leftKey, rightKey, fireKey, specialKey):
        self.UpKey = upKey
        self.DownKey = downKey
        self.LeftKey = leftKey
        self.RightKey = rightKey
        self.FireKey = fireKey
        self.SpecialKey = specialKey

class ControllerState:
    def __init__(self, controllerKeys: ControllerKeys):
        self.LeftPressed = False
        self.RightPressed = False
        self.UpPressed = False
        self.DownPressed = False
        self.FirePressed = False

        self.ControllerKeys = controllerKeys

    def keyReleased(self, key):
        if key == self.ControllerKeys.UpKey:
            self.UpPressed = False
        elif key == self.ControllerKeys.DownKey:
            self.DownPressed = False
        elif key == self.ControllerKeys.LeftKey:
            self.LeftPressed = False
        elif key == self.ControllerKeys.RightKey:
            self.RightPressed = False
        elif key == self.ControllerKeys.FireKey:
            self.FirePressed = False

    def keyPressed(self, key):
        if key == self.ControllerKeys.UpKey:
            self.UpPressed = True
        elif key == self.ControllerKeys.DownKey:
            self.DownPressed = True
        elif key == self.ControllerKeys.LeftKey:
            self.LeftPressed = True
        elif key == self.ControllerKeys.RightKey:
            self.RightPressed = True
        elif key == self.ControllerKeys.FireKey:
            self.FirePressed = True
        

class gameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        self.scene = None

        self.physics_engine: Optional[PymunkPhysicsEngine] = None
        gravity = (0, 0)
        damping = 0.8

        # Create the physics engine
        self.physics_engine = PymunkPhysicsEngine(damping=damping, gravity=gravity)

        self.player1Spaceship = SpaceshipOne()

        # Track the current state of what key is pressed
        self.controllerKeys = ControllerKeys(arcade.key.UP,arcade.key.DOWN,arcade.key.LEFT,arcade.key.RIGHT,arcade.key.SPACE,arcade.key.MOD_SHIFT)
        self.controllerState = ControllerState(self.controllerKeys)

    def setup(self):
        self.scene = arcade.Scene()

        self.scene.add_sprite_list

        self.scene.add_sprite_list("Planet", use_spatial_hash=True)
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Bullet", use_spatial_hash=False)

        self.scene.add_sprite("Player", self.player1Spaceship.Sprite)

        planet = arcade.Sprite("sprites/planet.png", 1.0)
        planet.center_x = 100
        planet.center_y = 50
        self.scene.add_sprite("Planet", planet)

        self.physics_engine.add_sprite(
            self.player1Spaceship.Sprite,
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
        self.player1Spaceship.Sprite.change_x = 0
        self.player1Spaceship.Sprite.change_y = 0

        if self.controllerState.UpPressed and not self.controllerState.DownPressed:
            angle_radians = (
                math.radians(self.player1Spaceship.Sprite.angle) + math.pi / 2.0
            )
            force = (
                math.cos(angle_radians) * self.player1Spaceship.MoveForce,
                math.sin(angle_radians) * self.player1Spaceship.MoveForce,
            )
            self.physics_engine.apply_force(self.player1Spaceship.Sprite, force)
        elif self.controllerState.DownPressed and not self.controllerState.UpPressed:
            angle_radians_opposite = (
                math.radians(self.player1Spaceship.Sprite.angle)
                + math.pi
                + math.pi / 2.0
            )
            force = (
                math.cos(angle_radians_opposite) * self.player1Spaceship.MoveForce,
                math.sin(angle_radians_opposite) * self.player1Spaceship.MoveForce,
            )
            self.physics_engine.apply_force(self.player1Spaceship.Sprite, force)

        # --- Move items in the physics engine
        self.physics_engine.step()

        if self.controllerState.LeftPressed and not self.controllerState.RightPressed:
            self.player1Spaceship.Sprite.change_angle += (
                self.player1Spaceship.PlayerAngleStep
            )
        elif self.controllerState.RightPressed and not self.controllerState.LeftPressed:
            self.player1Spaceship.Sprite.change_angle += (
                -self.player1Spaceship.PlayerAngleStep
            )

        # Fire pressed
        if self.controllerState.FirePressed:
            bullet = arcade.Sprite("sprites/bullet.png", 1)
            start_x = self.player1Spaceship.Sprite.center_x
            start_y = self.player1Spaceship.Sprite.center_y
            bullet.center_x = start_x
            bullet.center_y = start_y
            start_angle = self.player1Spaceship.Sprite.change_angle + 90

            start_angle_radian = math.radians(start_angle)
            bullet.change_x = (
                math.cos(start_angle_radian) * self.player1Spaceship.BulletSpeed
            )
            bullet.change_y = (
                math.sin(start_angle_radian) * self.player1Spaceship.BulletSpeed
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

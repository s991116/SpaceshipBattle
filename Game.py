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

class BulletFactory:
    def __init__(self):
        self.a = 1

    def CreateBullet(self, positionX: float, positionY: float, angle: float, screenWidth: int, screenHeight: int, physicsEngine: PymunkPhysicsEngine):
        bullet = Bullet(positionX, positionY, angle, screenWidth, screenHeight, physicsEngine)        
        return bullet
        
class Bullet(arcade.Sprite):
    def __init__(
        self,
        positionX: float,
        positionY: float,
        angle: float,
        screenWidth: int,        
        screenHeight: int,
        physicsEngine: PymunkPhysicsEngine,
    ):
        super().__init__("sprites/bullet.png", 1)
        self.MoveForce = 2000
        self.angle = angle
        self.ScreenWidth = screenWidth
        self.ScreenHeight = screenHeight
        self.center_x = positionX
        self.center_y = positionY
        self.physicEngine = physicsEngine


        self.physicEngine.add_sprite(
            self,
            friction=1.0,
            moment=PymunkPhysicsEngine.MOMENT_INF,
            damping=0.8,
            collision_type="Bullet",
            max_velocity=1000,
            body_type=PymunkPhysicsEngine.DYNAMIC
        )
        self.physicEngine.apply_impulse(self, (self.MoveForce, 0))


    def update(self):

        super().update()

        if (
            self.bottom > self.ScreenHeight
            or self.top < 0
            or self.right < 0
            or self.left > self.ScreenWidth
        ):
            self.remove_from_sprite_lists()
            print("Remove Bullet")


class SpaceshipOne(arcade.Sprite):
    def __init__(
        self,
        positionX: float,
        positionY: float,
        angle: float,
        physicsEngine: PymunkPhysicsEngine,
        controllerState: ControllerState,        
        scene: arcade.Scene,
        screenWidth: int,
        screenHeight: int,
        bulletFactory: BulletFactory
    ):
        super().__init__("sprites/spiked ship.png", 0.5)

        self.center_x = positionX
        self.center_y = positionY
        self.angle = angle

        self.PhysicsEngine = physicsEngine
        self.ControllerState = controllerState
        self.Scene = scene
        self.ScreenWidth = screenWidth
        self.screenHeight = screenHeight
        self.bulletFactory = bulletFactory

        self.MovementSpeed = 5
        self.MoveForce = 3000
        self.PlayerAngleStep = 5

        self.PhysicsEngine.add_sprite(
            self,
            friction=1.0,
            moment=PymunkPhysicsEngine.MOMENT_INF,
            damping=0.8,
            collision_type="Player",
            max_velocity=400,
        )

        self.FirePressed = False

    def update(self):

        super().update()
        # Calculate speed based on the keys pressed
        self.change_x = 0
        self.change_y = 0

        if self.ControllerState.UpPressed and not self.ControllerState.DownPressed:
            angle_radians = math.radians(self.angle) + math.pi / 2.0
            force = (
                math.cos(angle_radians) * self.MoveForce,
                math.sin(angle_radians) * self.MoveForce,
            )
            self.PhysicsEngine.apply_force(self, force)
        elif self.ControllerState.DownPressed and not self.ControllerState.UpPressed:
            angle_radians_opposite = (
                math.radians(self.angle) + math.pi + math.pi / 2.0
            )
            force = (
                math.cos(angle_radians_opposite) * self.MoveForce,
                math.sin(angle_radians_opposite) * self.MoveForce,
            )
            self.PhysicsEngine.apply_force(self, force)

        if self.ControllerState.LeftPressed and not self.ControllerState.RightPressed:
            self.change_angle += self.PlayerAngleStep
        elif self.ControllerState.RightPressed and not self.ControllerState.LeftPressed:
            self.change_angle += -self.PlayerAngleStep

        # Fire pressed            
        if self.ControllerState.FirePressed and not self.FirePressed:
            self.FirePressed = True
            bullet_angle = self.angle+90
            bullet_angle_radians = math.radians(bullet_angle)
            offsetX = -12
            offsetY = 35
            centerX = self.center_x + math.sin(bullet_angle_radians)*offsetX + math.cos(bullet_angle_radians)*offsetY
            centerY = self.center_y + math.sin(bullet_angle_radians)*offsetY + math.cos(bullet_angle_radians)*offsetX

            bullet = self.bulletFactory.CreateBullet(
                centerX,
                centerY,
                bullet_angle,
                self.ScreenWidth,
                self.screenHeight,
                self.PhysicsEngine,
            )
            self.Scene.add_sprite("Bullet", bullet)

        if not self.ControllerState.FirePressed:
            self.FirePressed = False

class gameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.player_sprite: Optional[SpaceshipOne] = None

        # Sprite lists we need
        self.player_list: Optional[arcade.SpriteList] = None
        self.wall_list: Optional[arcade.SpriteList] = None
        self.bullet_list: Optional[arcade.SpriteList] = None
        self.item_list: Optional[arcade.SpriteList] = None
        arcade.set_background_color(arcade.color.BLACK)

        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]

    def setup(self):
        self.scene = arcade.Scene()

        # Track the current state of what key is pressed
        self.controller1Keys = ControllerKeys(
            arcade.key.UP,
            arcade.key.DOWN,
            arcade.key.LEFT,
            arcade.key.RIGHT,
            arcade.key.SPACE,
            arcade.key.MOD_SHIFT,
        )
        self.controller1State = ControllerState(self.controller1Keys)

        self.controller2Keys = ControllerKeys(
            arcade.key.W,
            arcade.key.S,
            arcade.key.A,
            arcade.key.D,
            arcade.key.F,
            arcade.key.G,
        )
        self.controller2State = ControllerState(self.controller2Keys)

        self.scene.add_sprite_list

        self.scene.add_sprite_list("Planet", use_spatial_hash=True)
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Bullet", use_spatial_hash=False)

        self.physics_engine = arcade.PymunkPhysicsEngine(
            damping=0.9, gravity=(0.0, 0.0)
        )

        bulletFactory = BulletFactory()

        left, screen_width, bottom, screen_height = self.get_viewport()

        self.player1Spaceship = SpaceshipOne(
            200,
            200,
            0,
            self.physics_engine,
            self.controller1State,
            self.scene,
            screen_width,
            screen_height,
            bulletFactory
        )
        self.scene.add_sprite("Player", self.player1Spaceship)

        self.player2Spaceship = SpaceshipOne(
            400,
            300,
            0,
            self.physics_engine,
            self.controller2State,
            self.scene,
            screen_width,
            screen_height,
            bulletFactory
        )
        self.scene.add_sprite("Player", self.player2Spaceship)

        planet = arcade.Sprite("sprites/planet.png", 1.0)
        planet.center_x = 100
        planet.center_y = 50
        self.scene.add_sprite("Planet", planet)

        def player_hit_handler(bullet_sprite, player_sprite, _arbiter, _space, _data):
            """ Called for bullet/wall collision """
            print("Bullet Hit Player")
            bullet_sprite.remove_from_sprite_lists()
            player_sprite.remove_from_sprite_lists()

        def bullet_hit_handler(bullet1_sprite, bullet2_sprite, _arbiter, _space, _data):
            """ Called for bullet/wall collision """
            print("Bullet Hit Bullet")
            bullet1_sprite.remove_from_sprite_lists()
            bullet2_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("Bullet", "Player", post_handler=player_hit_handler)
        self.physics_engine.add_collision_handler("Bullet", "Bullet", post_handler=bullet_hit_handler)



    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        self.controller1State.keyPressed(key)
        self.controller2State.keyPressed(key)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        self.controller1State.keyReleased(key)
        self.controller2State.keyReleased(key)

    def on_update(self, delta_time):
        self.physics_engine.step()
        self.scene.get_sprite_list("Player").update()
        self.scene.get_sprite_list("Bullet").update()

    def on_draw(self):
        # Clear the screen to the background color
        self.clear()

        # Draw our Scene
        self.scene.draw()


def main():
    window = gameWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

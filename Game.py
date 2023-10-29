# Basic arcade program
# Displays a black window with a triangle in the middle

# Imports
import arcade

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Spaceship Battle"
RADIUS = 150
TRIANGLE_SIZE = 10

class gameWindow(arcade.Window):
  def __init__(self):
    super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_background_color(arcade.color.BLACK)
  
  def setup(self):
    pass
  
  def on_draw(self):
    arcade.start_render()
    # Draw a blue circle
    triangle_pos_x = SCREEN_WIDTH / 2
    triangle_pos_y = SCREEN_HEIGHT / 2

    x1 = triangle_pos_x
    y1 = triangle_pos_y + 3 * TRIANGLE_SIZE

    x2 = triangle_pos_x - TRIANGLE_SIZE
    y2 = triangle_pos_y

    x3 = triangle_pos_x + TRIANGLE_SIZE
    y3 = triangle_pos_y
    arcade.draw_triangle_outline(x1,y1,x2,y2,x3,y3,arcade.color.ARMY_GREEN, border_width= 5)


def main():
  window = gameWindow()
  window.setup()
  arcade.run()

if __name__ == "__main__":
   main()
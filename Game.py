# Basic arcade program
# Displays a white window with a blue circle in the middle

# Imports
import arcade

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Spaceship Battle"
RADIUS = 150
TRIANGLE_SIZE = 10

# Open the window
arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

# Set the background color
arcade.set_background_color(arcade.color.WHITE)

# Clear the screen and start drawing
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
#arcade.draw_circle_filled(
#    SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, RADIUS, arcade.color.BLUE
#)

# Finish drawing
arcade.finish_render()

# Display everything
arcade.run()
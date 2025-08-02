import pygame  # Core Pygame library for game development
from pygame.locals import *  # Import common Pygame constants (e.g., K_LEFT, QUIT)
import time  # For time-related functions like sleep and tracking elapsed time
import random  # For generating random numbers (e.g., apple position, agent movement)
from datetime import (
    datetime,
)  # Although not used for elapsed time, imported for general time needs
import math  # For calculating Euclidean distance

# --- Game Configuration Constants ---
SIZE = 40  # Size of each block (snake segment, apple) in pixels
BACKGROUND_COLOR = (110, 110, 5)  # A greenish-brown color for fallback background


class Apple:
    """
    Represents the food that the snake eats.
    """

    def __init__(self, parent_screen):
        """
        Initializes the Apple object.
        Args:
            parent_screen (pygame.Surface): The Pygame surface (game window) to draw the apple on.
        """
        self.parent_screen = parent_screen
        # Load the apple image. Includes basic error handling for missing image.
        try:
            self.image = pygame.image.load("resources/apple.png").convert_alpha()
        except pygame.error:
            print(
                "Warning: 'resources/apple.png' not found. Using a red square as placeholder."
            )
            self.image = pygame.Surface((SIZE, SIZE))
            self.image.fill((255, 0, 0))  # Fallback to red color

        # Get screen dimensions for proper apple placement
        self.screen_width = parent_screen.get_width()
        self.screen_height = parent_screen.get_height()

        # Calculate grid dimensions
        self.grid_width = self.screen_width // SIZE
        self.grid_height = self.screen_height // SIZE

        # Initialize apple position
        self.x = 120
        self.y = 120

    def draw(self):
        """Draws the apple on the parent screen at its current (x, y) coordinates."""
        self.parent_screen.blit(self.image, (self.x, self.y))

    def move(self, snake_positions=None):
        """
        Moves the apple to a random position that doesn't overlap with the snake.
        Args:
            snake_positions (list): List of (x, y) tuples representing snake body positions
        """
        if snake_positions is None:
            snake_positions = []

        # Generate valid positions (not occupied by snake)
        valid_positions = []
        for x in range(0, self.screen_width - SIZE, SIZE):
            for y in range(0, self.screen_height - SIZE, SIZE):
                if (x, y) not in snake_positions:
                    valid_positions.append((x, y))

        if valid_positions:
            self.x, self.y = random.choice(valid_positions)
        else:
            # Fallback if no valid positions (shouldn't happen in normal gameplay)
            self.x = random.randint(0, self.grid_width - 1) * SIZE
            self.y = random.randint(0, self.grid_height - 1) * SIZE


class Snake:
    """
    Represents the snake controlled by the player (or agent).
    """

    def __init__(self, parent_screen):
        """
        Initializes the Snake object.
        Args:
            parent_screen (pygame.Surface): The Pygame surface to draw the snake on.
        """
        self.parent_screen = parent_screen
        # Load the snake block image. Includes basic error handling for missing image.
        try:
            self.image = pygame.image.load("resources/block.jpg").convert_alpha()
        except pygame.error:
            print(
                "Warning: 'resources/block.jpg' not found. Using a green square as placeholder."
            )
            self.image = pygame.Surface((SIZE, SIZE))
            self.image.fill((0, 128, 0))  # Fallback to green color

        self.direction = "down"  # Initial direction of the snake.
        self.best_time = ""  # To store the best time recorded for eating an apple.

        self.length = 1  # Initial length of the snake (one block).
        # Lists to store the (x, y) coordinates for each segment of the snake.
        self.x = [40]  # Initial x-coordinate of the head.
        self.y = [40]  # Initial y-coordinate of the head.

    def move_left(self):
        """Sets the snake's direction to 'left', preventing immediate U-turns."""
        if self.direction != "right":
            self.direction = "left"

    def move_right(self):
        """Sets the snake's direction to 'right', preventing immediate U-turns."""
        if self.direction != "left":
            self.direction = "right"

    def move_up(self):
        """Sets the snake's direction to 'up', preventing immediate U-turns."""
        if self.direction != "down":
            self.direction = "up"

    def move_down(self):
        """Sets the snake's direction to 'down', preventing immediate U-turns."""
        if self.direction != "up":
            self.direction = "down"

    def walk(self):
        """
        Updates the snake's position based on its current direction.
        Each body segment follows the segment in front of it, and the head moves
        according to the current direction.
        """
        # Move body segments: starting from the tail, each segment takes the position of the one in front of it.
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # Update head position based on current direction.
        if self.direction == "left":
            self.x[0] -= SIZE
        elif self.direction == "right":
            self.x[0] += SIZE
        elif self.direction == "up":
            self.y[0] -= SIZE
        elif self.direction == "down":
            self.y[0] += SIZE

        self.draw()  # Redraw the snake after moving.

    def draw(self):
        """Draws all segments of the snake on the parent screen."""
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

    def increase_length(self):
        """
        Increases the snake's length by adding a new segment.
        The new segment will be positioned at the tail and will move properly in the next walk cycle.
        """
        self.length += 1
        # Add new segment at the tail position
        self.x.append(self.x[-1])
        self.y.append(self.y[-1])

    def get_positions(self):
        """Returns a list of (x, y) tuples representing all snake body positions."""
        return [(self.x[i], self.y[i]) for i in range(self.length)]


class Game:
    """
    Manages the overall game logic, including initialization,
    game loop, score, time, and collision detection.
    """
   #//////////////////////////////Helper Functions//////////////////////////////////////
    def _get_wall_boundaries(self):
        """Returns a set of wall coordinates based on game size."""
        width, height = self.surface.get_width(), self.surface.get_height()
        wall_coords = set()
        for x in range(0, width, SIZE):
            for y in range(0, height, SIZE):
                if x < 0 or x >= width or y < 0 or y >= height:
                    wall_coords.add((x, y))
        return wall_coords

    def _is_valid_move(self, pos, model):
        """Returns True if move does not collide with wall or self, based on model."""
        x, y = pos
        width, height = self.surface.get_width(), self.surface.get_height()

        # Check wall collision
        if x < 0 or x >= width or y < 0 or y >= height:
            return False

        # Check snake body collision
        if pos in model["snake_body"]:
            return False

        return True

    def _set_snake_direction(self, direction):
        if direction == "left":
            self.snake.move_left()
        elif direction == "right":
            self.snake.move_right()
        elif direction == "up":
            self.snake.move_up()
        elif direction == "down":
            self.snake.move_down()
#--------------------------------------------------------------------------------------------------
    def __init__(self):
        """Initializes the Pygame environment and game components."""
        pygame.init()  # Initialize all the Pygame modules.
        pygame.display.set_caption("Snake Game")  # Set the window title.

        pygame.mixer.init()  # Initialize the mixer for sound playback.
        self.play_background_music()  # Start playing background music when the game initializes.

        # Set up the display surface (game window) with a resolution of 1000x800 pixels.
        self.surface = pygame.display.set_mode((1000, 800))
        # Initial background fill (this will be overwritten by the background image later).
        self.surface.fill(BACKGROUND_COLOR)

        # Create instances of the Snake and Apple classes, passing the game surface.
        self.snake = Snake(self.surface)
        self.snake.draw()  # Draw the snake's initial position.
        self.apple = Apple(self.surface)
        self.apple.draw()  # Draw the apple's initial position.

        self.game_speed = (
            0.15  # Controls how fast the snake moves (lower value = faster).
        )
        self.start_time = (
            time.time()
        )  # Records the timestamp when the current game session starts.

    def play_background_music(self):
        """Loads and plays background music in an infinite loop."""
        # try:
        #     pygame.mixer.music.load("resources/bg_music_1.mp3")
        #     pygame.mixer.music.play(-1, 0)  # -1 means loop indefinitely
        # except pygame.error:
        #     print("Warning: Background music file not found. Continuing without music.")

    def play_sound(self, sound_name):
        """
        Plays a specific sound effect based on its name.
        Args:
            sound_name (str): The name of the sound ('crash' or 'ding').
        """
        try:
            if sound_name == "crash":
                sound = pygame.mixer.Sound("resources/crash.mp3")
            elif sound_name == "ding":
                sound = pygame.mixer.Sound("resources/ding.mp3")
            else:
                return

            pygame.mixer.Sound.play(sound)
        except pygame.error:
            print(f"Warning: Sound file '{sound_name}.mp3' not found.")

    def reset(self):
        """Resets the game state for a new round after game over."""
        self.snake = Snake(self.surface)  # Recreate a new snake.
        self.apple = Apple(self.surface)  # Recreate a new apple.
        self.snake.best_time = ""  # Clear best time for eating an apple.
        self.start_time = time.time()  # Reset the start time for the new game.
        self.game_speed = 0.15  # Reset game speed

    def is_collision(self, x1, y1, x2, y2):
        """
        Checks for collision between two square objects.
        Args:
            x1, y1 (int): Coordinates (top-left) of the first object.
            x2, y2 (int): Coordinates (top-left) of the second object.
        Returns:
            bool: True if collision occurs, False otherwise.
        """
        return x1 == x2 and y1 == y2

    def self_collision(self):
        """
        Checks if the snake's head has collided with any of its own body segments.
        Returns:
            bool: True if self-collision occurs, False otherwise.
        """
        # Only check collision if snake has more than 4 segments to avoid false positives
        # when the snake just ate food and is still growing
        if self.snake.length < 4:
            return False

        # Check collision with body segments (excluding the head itself)
        # Skip the first few segments to avoid collision detection issues right after eating
        for i in range(4, self.snake.length):
            if self.is_collision(
                self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]
            ):
                return True
        return False

    def check_wall_collision(self):
        """
        Checks if the snake's head has collided with any of the screen boundaries (walls).
        Returns:
            bool: True if a wall collision occurs, False otherwise.
        """
        head_x, head_y = self.snake.x[0], self.snake.y[0]
        screen_width, screen_height = (
            self.surface.get_width(),
            self.surface.get_height(),
        )

        # Check collision with walls
        if (
            head_x < 0
            or head_x >= screen_width
            or head_y < 0
            or head_y >= screen_height
        ):
            return True
        return False

    def render_background(self):
        """Loads and blits the background image onto the game surface."""
        try:
            bg = pygame.image.load("resources/background.jpg").convert()
            self.surface.blit(bg, (0, 0))
        except pygame.error:
            self.surface.fill(BACKGROUND_COLOR)  # Fallback to solid color

    def play(self):
        """
        Performs one full step of the game:
        1. Renders the background, snake, and apple.
        2. Updates and displays score and time.
        3. Checks for eating apple, self-collision, and wall collision.
        """
        self.render_background()  # Draw the game background.
        self.snake.walk()  # Update and draw the snake's new position.
        self.apple.draw()  # Draw the apple.
        self.display_score()  # Display the current score.
        self.display_time(False)  # Display the elapsed time
        pygame.display.flip()  # Update the entire screen to show all drawn elements.

        # Snake eating apple scenario.
        if self.is_collision(
            self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y
        ):
            self.display_time(True)  # Capture the time at which this apple was eaten.
            self.play_sound("ding")  # Play ding sound.
            self.snake.increase_length()  # Increase snake's length.

            # Increase game speed every 3 apples eaten to increase difficulty.
            if self.snake.length % 3 == 0 and self.game_speed > 0.05:
                self.game_speed = max(0.05, self.game_speed - 0.02)

            # Move apple to new position, avoiding snake body
            self.apple.move(self.snake.get_positions())

        # Snake colliding with itself.
        if self.self_collision():
            self.play_sound("crash")  # Play crash sound.
            raise Exception("Self Collision!")

        # Snake colliding with wall.
        if self.check_wall_collision():
            self.play_sound("crash")  # Play crash sound.
            raise Exception("Wall Collision!")

    def display_score(self):
        """Renders and displays the current score on the screen."""
        font = pygame.font.SysFont("arial", 30)
        score_text = font.render(
            f"Score: {self.snake.length - 1}", True, (255, 255, 255)
        )
        self.surface.blit(score_text, (850, 10))

    def display_time(self, score_t=False):
        """
        Renders and displays the elapsed time on the screen.
        Args:
            score_t (bool): If True, captures the current elapsed time as the 'best_time'
        """
        font = pygame.font.SysFont("arial", 30)
        elapsed_seconds = int(time.time() - self.start_time)
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        time_string = f"{minutes:02d}:{seconds:02d}"

        if score_t:
            self.snake.best_time = time_string

        time_text = font.render(f"Time: {time_string}", True, (255, 255, 255))
        self.surface.blit(time_text, (10, 10))

    def show_game_over(self):
        """
        Displays the game over screen with the final score and instructions.
        """
        self.render_background()
        font = pygame.font.SysFont("arial", 30)

        # Calculate final time
        elapsed_seconds = int(time.time() - self.start_time)
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        final_time = f"{minutes:02d}:{seconds:02d}"

        # Display game over messages
        line1 = font.render("Game Over!", True, (255, 255, 255))
        self.surface.blit(line1, (400, 200))

        line2 = font.render(f"Score: {self.snake.length - 1}", True, (255, 255, 255))
        self.surface.blit(line2, (400, 280))

        line3 = font.render(f"Time: {final_time}", True, (255, 255, 255))
        self.surface.blit(line3, (400, 320))

        if self.snake.best_time:
            line4 = font.render(
                f"Last Apple: {self.snake.best_time}", True, (255, 255, 255)
            )
            self.surface.blit(line4, (400, 360))

        line5 = font.render(
            "Press Enter to play again or Escape to exit", True, (255, 255, 255)
        )
        self.surface.blit(line5, (250, 450))

        try:
            pygame.mixer.music.pause()
        except:
            pass
        pygame.display.flip()
    #//////////////////////////////////////Main Control/////////////////////////////////////
    def auto_control(self):
        """
        A model-based agent that uses an internal model of the game environment
        to select the best next action.
        """
        head_x, head_y = self.snake.x[0], self.snake.y[0]
        apple_x, apple_y = self.apple.x, self.apple.y

        # Internal model: walls and snake body
        model = {
            "walls": self._get_wall_boundaries(),
            "snake_body": self.snake.get_positions()[1:],  # Exclude head
            "apple": (apple_x, apple_y)
        }

        possible_directions = {
            "left": (head_x - SIZE, head_y),
            "right": (head_x + SIZE, head_y),
            "up": (head_x, head_y - SIZE),
            "down": (head_x, head_y + SIZE),
        }

        safe_moves = []

        for direction, (nx, ny) in possible_directions.items():
            if self._is_valid_move((nx, ny), model):
                # Use internal model to calculate predicted cost (Euclidean distance to apple)
                distance = math.sqrt((apple_x - nx) ** 2 + (apple_y - ny) ** 2)
                safe_moves.append((direction, distance))

        # Choose move that brings snake closest to apple safely
        if safe_moves:
            best_direction = min(safe_moves, key=lambda x: x[1])[0]
            self._set_snake_direction(best_direction)


    def _would_collide(self, x, y):
        """Check if moving to position (x, y) would cause a collision."""
        # Check wall collision
        if (
            x < 0
            or x >= self.surface.get_width()
            or y < 0
            or y >= self.surface.get_height()
        ):
            return True

        # Check self collision - only check against body segments that are far enough from head
        # Skip immediate neck segments to avoid false positives
        for i in range(3, self.snake.length):
            if x == self.snake.x[i] and y == self.snake.y[i]:
                return True

        return False
    #///////////////////////////////////////////////////////////////////////////////////////////
    def run(self):
        """
        The main game loop. Handles events, updates game state, and controls game flow.
        """
        running = True
        pause = False
        clock = pygame.time.Clock()  # For better frame rate control

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        try:
                            pygame.mixer.music.unpause()
                        except:
                            pass
                        pause = False
                        self.reset()

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        elif event.key == K_RIGHT:
                            self.snake.move_right()
                        elif event.key == K_UP:
                            self.snake.move_up()
                        elif event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            # Auto control (comment out if you want manual control)
            if not pause:
                self.auto_control()

            # Game logic
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True

            # Use clock for better timing instead of time.sleep()
            clock.tick(int(1 / self.game_speed))


# Entry point of the game application.
if __name__ == "__main__":
    game = Game()
    game.run()

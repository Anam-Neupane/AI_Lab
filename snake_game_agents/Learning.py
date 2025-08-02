import pygame  # Core Pygame library for game development
from pygame.locals import *  # Import common Pygame constants (e.g., K_LEFT, QUIT)
import time  # For time-related functions like sleep and tracking elapsed time
import random  # For generating random numbers (e.g., apple position, agent movement)
import numpy as np  # For Q-learning table and calculations

SIZE = 40  # Size of each block (snake segment, apple) in pixels
BACKGROUND_COLOR = (110, 110, 5)  # A greenish-brown color for fallback background


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        try:
            self.image = pygame.image.load("resources/apple.png").convert_alpha()
        except pygame.error:
            print(
                "Warning: 'resources/apple.png' not found. Using a red square as placeholder."
            )
            self.image = pygame.Surface((SIZE, SIZE))
            self.image.fill((255, 0, 0))

        self.x = 120
        self.y = 120

        self.x_list = [
            320, 160, 680, 280, 400, 240, 960, 80, 40, 760, 720, 880, 400, 680, 480,
            480, 520, 160, 760, 480, 720, 360, 960, 160, 80, 400, 760, 680, 760, 800,
        ]
        self.y_list = [
            560, 40, 440, 280, 240, 560, 80, 200, 240, 80, 80, 520, 720, 360, 680,
            760, 680, 320, 80, 360, 720, 120, 280, 280, 320, 680, 320, 40, 520, 600,
        ]
        self.count = 0

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = self.x_list[self.count]
        self.y = self.y_list[self.count]
        self.count = (self.count + 1) % len(self.x_list)


class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        try:
            self.image = pygame.image.load("resources/block.jpg").convert_alpha()
        except pygame.error:
            print(
                "Warning: 'resources/block.jpg' not found. Using a green square as placeholder."
            )
            self.image = pygame.Surface((SIZE, SIZE))
            self.image.fill((0, 128, 0))

        self.direction = "down"
        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        if self.direction != "right":
            self.direction = "left"

    def move_right(self):
        if self.direction != "left":
            self.direction = "right"

    def move_up(self):
        if self.direction != "down":
            self.direction = "up"

    def move_down(self):
        if self.direction != "up":
            self.direction = "down"

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "left":
            self.x[0] -= SIZE
        elif self.direction == "right":
            self.x[0] += SIZE
        elif self.direction == "up":
            self.y[0] -= SIZE
        elif self.direction == "down":
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class QLearningAgent:
    def __init__(self, actions, learning_rate=0.1, discount_factor=0.9, epsilon=0.2):
        self.q_table = {}  # state -> action-values
        self.actions = actions  # ['left', 'right', 'up', 'down']
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon

    def get_state(self, snake, apple):
        head_x, head_y = snake.x[0], snake.y[0]
        apple_x, apple_y = apple.x, apple.y

        dx = 0
        if apple_x > head_x:
            dx = 1
        elif apple_x < head_x:
            dx = -1

        dy = 0
        if apple_y > head_y:
            dy = 1
        elif apple_y < head_y:
            dy = -1

        direction_map = {"left": 0, "right": 1, "up": 2, "down": 3}
        dir_code = direction_map.get(snake.direction, -1)

        return (dx, dy, dir_code)

    def choose_action(self, state):
        if np.random.rand() < self.epsilon or state not in self.q_table:
            return np.random.choice(self.actions)
        else:
            action_values = self.q_table[state]
            return self.actions[np.argmax(action_values)]

    def learn(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(len(self.actions))
        if next_state is not None and next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(len(self.actions))

        action_index = self.actions.index(action)
        predict = self.q_table[state][action_index]

        if next_state is None:
            target = reward  # Terminal state
        else:
            target = reward + self.gamma * np.max(self.q_table[next_state])

        self.q_table[state][action_index] += self.lr * (target - predict)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Codebasics Snake And Apple Game")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill(BACKGROUND_COLOR)

        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

        self.elapsed_time = ""
        self.game_speed = 0.05
        self.start_time = time.time()

        # Initialize Q-learning agent
        self.agent = QLearningAgent(actions=["left", "right", "up", "down"])
        self.prev_state = None
        self.prev_action = None

    def play_background_music(self):
        pass

    def play_sound(self, sound_name):
        pass

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.elapsed_time = ""
        self.start_time = time.time()
        self.prev_state = None
        self.prev_action = None

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def self_collision(self):
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                return True
        return False

    def check_wall_collision(self):
        head_x, head_y = self.snake.x[0], self.snake.y[0]
        screen_width, screen_height = self.surface.get_width(), self.surface.get_height()

        if head_x < 0 or head_x >= screen_width:
            return True
        if head_y < 0 or head_y >= screen_height:
            return True
        return False

    def render_background(self):
        try:
            bg = pygame.image.load("resources/background.jpg").convert()
            self.surface.blit(bg, (0, 0))
        except pygame.error:
            self.surface.fill(BACKGROUND_COLOR)

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        self.display_time(False)
        pygame.display.flip()

        # Check apple eaten
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.display_time(True)
            self.snake.increase_length()
            self.game_speed = 0.05
            self.apple.move()
            return 10  # reward for eating apple
        return 0

    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        score_text = font.render(f"Score: {self.snake.length - 1}", True, (200, 200, 200))
        self.surface.blit(score_text, (850, 10))

    def display_time(self, score_t=False):
        font = pygame.font.SysFont("arial", 30)
        elapsed_seconds = int(time.time() - self.start_time)
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        time_string = f"{minutes:02d}:{seconds:02d}"
        self.elapsed_time = time_string
        if score_t:
            pass  # Could track apple eating time if desired
        time_text = font.render(f"Time: {time_string}", True, (200, 200, 200))
        self.surface.blit(time_text, (10, 10))

    def show_game_over(self, message="Game Over!"):
        self.render_background()
        font = pygame.font.SysFont("arial", 30)
        line1 = font.render(f"Game is over! {message}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 200))
        line2 = font.render(f"Your score = {self.snake.length - 1}", True, (255, 255, 255))
        self.surface.blit(line2, (250, 350))
        line3 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line3, (200, 550))
        pygame.display.flip()

    def learning_control(self):
        state = self.agent.get_state(self.snake, self.apple)
        action = self.agent.choose_action(state)

        # Apply action
        if action == "left":
            self.snake.move_left()
        elif action == "right":
            self.snake.move_right()
        elif action == "up":
            self.snake.move_up()
        elif action == "down":
            self.snake.move_down()

        # Play one step
        reward = self.play()  # Returns +10 if apple eaten, else 0

        # Check collisions
        if self.self_collision() or self.check_wall_collision():
            reward = -10
            # Learn with terminal state
            self.agent.learn(self.prev_state, self.prev_action, reward, None)
            raise Exception("Collision Occurred")

        # Learn from last action
        if self.prev_state is not None and self.prev_action is not None:
            self.agent.learn(self.prev_state, self.prev_action, reward, state)

        # Update previous state/action
        self.prev_state = state
        self.prev_action = action


    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False
                        self.reset()

                elif event.type == QUIT:
                    running = False

            if not pause:
                try:
                    self.learning_control()
                except Exception as e:
                    self.show_game_over(str(e))
                    pause = True

            time.sleep(self.game_speed)


if __name__ == "__main__":
    game = Game()
    game.run()

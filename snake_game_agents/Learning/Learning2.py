
import pygame
from pygame.locals import *
import time
import random
import numpy as np
import pickle
import os
from datetime import datetime

SIZE = 40
BACKGROUND_COLOR = (0, 0, 30)  # Darker background for visual contrast
SAVE_PATH = "q_table2.pkl"
LOG_PATH = "game_log2.csv"

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        try:
            self.image = pygame.image.load("resources/apple.png").convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((SIZE, SIZE))
            self.image.fill((255, 0, 0))
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 24) * SIZE
        self.y = random.randint(0, 19) * SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        try:
            self.image = pygame.image.load("resources/block.jpg").convert_alpha()
        except pygame.error:
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
        self.q_table = self.load_q_table()
        self.actions = actions
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon

    def load_q_table(self):
        if os.path.exists(SAVE_PATH):
            with open(SAVE_PATH, "rb") as f:
                return pickle.load(f)
        return {}

    def save_q_table(self):
        with open(SAVE_PATH, "wb") as f:
            pickle.dump(self.q_table, f)

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
        return self.actions[np.argmax(self.q_table[state])]

    def learn(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(len(self.actions))
        if next_state is not None and next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(len(self.actions))

        a_idx = self.actions.index(action)
        predict = self.q_table[state][a_idx]
        target = reward if next_state is None else reward + self.gamma * np.max(self.q_table[next_state])
        self.q_table[state][a_idx] += self.lr * (target - predict)

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 800))
        pygame.display.set_caption("Learning Snake")
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.agent = QLearningAgent(actions=["left", "right", "up", "down"])
        self.prev_state = None
        self.prev_action = None
        self.score = 0
        self.start_time = time.time()
        self.game_speed = 0.05

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.prev_state = None
        self.prev_action = None
        self.score = 0
        self.start_time = time.time()

    def is_collision(self):
        x, y = self.snake.x[0], self.snake.y[0]
        if x < 0 or x >= 1000 or y < 0 or y >= 800:
            return True
        for i in range(3, self.snake.length):
            if self.snake.x[i] == x and self.snake.y[i] == y:
                return True
        return False

    def play_step(self):
        self.surface.fill(BACKGROUND_COLOR)
        self.snake.walk()
        self.apple.draw()
        pygame.display.flip()

        state = self.agent.get_state(self.snake, self.apple)
        action = self.agent.choose_action(state)

        if action == "left":
            self.snake.move_left()
        elif action == "right":
            self.snake.move_right()
        elif action == "up":
            self.snake.move_up()
        elif action == "down":
            self.snake.move_down()

        reward = 0
        if self.snake.x[0] == self.apple.x and self.snake.y[0] == self.apple.y:
            self.snake.increase_length()
            self.apple.move()
            reward = 10
            self.score += 1

        if self.is_collision():
            reward = -10
            self.agent.learn(self.prev_state, self.prev_action, reward, None)
            return False

        if self.prev_state is not None and self.prev_action is not None:
            self.agent.learn(self.prev_state, self.prev_action, reward, state)

        self.prev_state = state
        self.prev_action = action
        return True

    def log_result(self, episode):
        duration = int(time.time() - self.start_time)
        log_line = f"{episode},{datetime.now()},{self.score},{duration}\n"
        header = "episode,timestamp,score,time_seconds\n"
        if not os.path.exists(LOG_PATH):
            with open(LOG_PATH, "w") as log:
                log.write(header)
        with open(LOG_PATH, "a") as log:
            log.write(log_line)

    def run(self, episodes=500):
        for ep in range(episodes):
            self.reset()
            alive = True
            while alive:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.agent.save_q_table()
                        pygame.quit()
                        return
                alive = self.play_step()
                time.sleep(self.game_speed)
            self.log_result(ep + 1)
        self.agent.save_q_table()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run(episodes=50)

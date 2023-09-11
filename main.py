from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Rectangle
from kivy.core.window import Window
import random

class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        self.snake_segments = [(5, 5)]
        self.food_position = (random.randint(0, 19), random.randint(0, 19))
        self.direction = (1, 0)  # Initial direction (right)
        self.score = 0

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.update_interval = 0.2  # Snake movement speed
        self.update()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        key = keycode[1]
        if key == 'up' and self.direction != (0, -1):
            self.direction = (0, 1)
        elif key == 'down' and self.direction != (0, 1):
            self.direction = (0, -1)
        elif key == 'left' and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif key == 'right' and self.direction != (-1, 0):
            self.direction = (1, 0)

    def update(self):
        new_head = (self.snake_segments[0][0] + self.direction[0], self.snake_segments[0][1] + self.direction[1])

        if new_head == self.food_position:
            self.snake_segments.insert(0, new_head)
            self.food_position = (random.randint(0, 19), random.randint(0, 19))
            self.score += 1
        else:
            self.snake_segments.insert(0, new_head)
            self.snake_segments.pop()

        if (
            new_head in self.snake_segments[1:]
            or new_head[0] < 0
            or new_head[0] >= 20
            or new_head[1] < 0
            or new_head[1] >= 20
        ):
            self.game_over()

        self.canvas.clear()
        with self.canvas:
            for segment in self.snake_segments:
                Rectangle(pos=(segment[0] * 20, segment[1] * 20), size=(20, 20))
            Rectangle(pos=(self.food_position[0] * 20, self.food_position[1] * 20), size=(20, 20))

        Clock.schedule_once(self.update, self.update_interval)

    def game_over(self):
        self.snake_segments = [(5, 5)]
        self.food_position = (random.randint(0, 19), random.randint(0, 19))
        self.direction = (1, 0)
        self.score = 0

class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        return game

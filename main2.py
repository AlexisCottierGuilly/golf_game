import arcade

class FloodFillAnimation(arcade.Animation):
    def __init__(self, sprite, color, duration):
        super().__init__(sprite, duration)
        self.color = color

    def update(self, delta_time):
        super().update(delta_time)
        self.sprite.color = self.color

    def on_complete(self):
        self.sprite.color = self.color

    def on_start(self):
        self.sprite.color = self.color

    def on_update(self, progress):
        self.sprite.color = self.color

class Ball(arcade.Sprite):
    def __init__(self, x, y, scale):
        super().__init__("images/ball.png", scale)
        self.center_x = x
        self.center_y = y
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.mass = 1
        self.speed = 1
        self.color = arcade.color.WHITE
        self.flood_fill_animation = FloodFillAnimation(self, arcade.color.WHITE, 0.5)
        self.flood_fill_animation.start()

    def update(self):
        self.center_x += self.velocity[0] * self.speed
        self.center_y += self.velocity[1] * self.speed
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        self.flood_fill_animation.update(1/60)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.velocity[1] = 1
        elif key == arcade.key.DOWN:
            self.velocity[1] = -1
        elif key == arcade.key.LEFT:
            self.velocity[0] = -1
        elif key == arcade.key.RIGHT:
            self.velocity[0] = 1

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.velocity[1] = 0
        elif key == arcade.key.DOWN:
            self.velocity[1] = 0
        elif key == arcade.key.LEFT:
            self.velocity[0] = 0
        elif key == arcade.key.RIGHT:
            self.velocity[0] = 0

    def on_mouse_press(self, x, y, button, modifiers):
        self.flood_fill_animation = FloodFillAnimation(self, arcade.color.RED, 0.5)
        self.flood_fill_animation.start()

    def on_mouse_release(self, x, y, button, modifiers):
        self.flood_fill_animation = FloodFillAnimation(self, arcade.color.WHITE, 0.5)
        self.flood_fill_animation.start()

    def on_mouse_motion(self, x, y, dx, dy):
        self.center_x = x
        self.center_y = y

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.center_x = x
        self.center_y = y

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.speed += scroll_y

    def on_update(self, delta_time):
        self.update()

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)
        self.ball = Ball(100, 100, 0.5)

    def on_draw(self):
        arcade.start_render()
        self.ball.draw()

    def on_update(self, delta_time):
        self.ball.update()

    def on_key_press(self, key, modifiers):
        self.ball.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.ball.on_key_release(key, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        self.ball.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.ball.on_mouse_release(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.ball.on_mouse_motion(x, y, dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.ball.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.ball.on_mouse_scroll(x, y, scroll_x, scroll_y)

    def on_update(self, delta_time):
        self.ball.on_update(delta_time)

    def on_close(self):
        arcade.close_window()

def main():
    window = MyGame(800, 600, "My Game")
    arcade.run()

if __name__ == "__main__":
    main()

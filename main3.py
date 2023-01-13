import arcade, math

# Angry bird game

# Constants
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
GRAVITY = 1

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.05
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128

# Movement speed of birds, in pixels per frame
BIRD_MOVEMENT_SPEED_X = 20
BIRD_MOVEMENT_SPEED_Y = 35

# Classes

def size_to_scale(sprite_size, target_size):
    return target_size / sprite_size

def angle_to_xy(angle):
    return math.cos(angle), math.sin(angle)

class Bird(arcade.Sprite):
    """ Bird Class """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_shooting = False

    def update(self):
        """ Move the bird """
        if self.is_shooting:
            self.change_y -= GRAVITY
            self.center_x += self.change_x
            self.center_y += self.change_y

    def update_animation(self, delta_time: float = 1/60):
        """ Manage the animation """
        if self.is_shooting:
            self.angle += -10

    def shoot(self, angle, strenght):
        """ Shoot the bird """
        self.is_shooting = True
        self.change_x = BIRD_MOVEMENT_SPEED_X * angle_to_xy(angle)[0] * (strenght / 200)
        self.change_y = BIRD_MOVEMENT_SPEED_Y * angle_to_xy(angle)[1] * (strenght / 200)

    def reset(self):
        """ Reset the bird """
        self.is_shooting = False
        self.center_x = 100
        self.center_y = 100
        self.change_x = 0
        self.change_y = 0
        self.angle = 0


class Brick(arcade.Sprite):
    """ Brick Class """

    def __init__(self, x, y, durability=1):
        super().__init__("assets/brick.png", TILE_SCALING)
        self.durability = durability
        self.center_x = x
        self.center_y = y

    def update(self):
        """ Update the brick """
        pass

    def hit(self, strenght):
        """ Hit the brick """
        self.durability -= strenght
        if self.durability <= 0:
            self.kill()

    def reset(self):
        """ Reset the brick """
        self.durability = 1


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Angry Bird Game")
        arcade.set_background_color(arcade.color.AMAZON)
        self.bird = Bird("assets/bird.png", CHARACTER_SCALING)
        self.bird.center_x = 100
        self.bird.center_y = 100
        self.brick_list = arcade.SpriteList()
        self.shoot_angle = 0
        self.shoot_strenght = 0
        self.first_mouse_pos = 0, 0
        self.shot_preview = arcade.SpriteList()
        self.mouse_pressed = False
        for i in range(200):
            dot = arcade.Sprite("assets/hole.png", 0.01)
            dot.center_x = -100
            dot.center_y = -100
            dot.alpha = 100
            self.shot_preview.append(dot)

        # Add the bricks (reate a block of bricks)
        brick_block_size = 15, 10
        brick_block_position = 500, 50
        x, y = brick_block_position
        for i in range(brick_block_size[0]):
            for j in range(brick_block_size[1]):
                b = Brick(x, y)
                b.scale = size_to_scale(b.texture.size[0], 50)
                self.brick_list.append(b)
                y += 50
            x += 50
            y = brick_block_position[1]

    def on_draw(self):
        arcade.start_render()
        self.brick_list.draw()
        self.shot_preview.draw()
        self.bird.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.bird.shoot()
            self.bird.change_y = BIRD_MOVEMENT_SPEED_Y
        if key == arcade.key.R:
            self.bird.reset()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.mouse_pressed = True
        self.first_mouse_pos = x, y

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        if self.mouse_pressed:
            self.shoot_angle = math.atan2(y - self.first_mouse_pos[1], x - self.first_mouse_pos[0])
            self.shoot_strenght = math.sqrt((y - self.first_mouse_pos[1]) ** 2 + (x - self.first_mouse_pos[0]) ** 2)
            n = 0
            for dot in self.shot_preview.sprite_list:
                # The dots should make a curve
                dot.center_x = self.bird.center_x + (self.shoot_strenght / 200) * BIRD_MOVEMENT_SPEED_X * angle_to_xy(self.shoot_angle)[0] * n
                dot.center_y = self.bird.center_y + (self.shoot_strenght / 200) * BIRD_MOVEMENT_SPEED_Y * angle_to_xy(self.shoot_angle)[1] * n - 0.5 * GRAVITY * n ** 2
                n += 1
    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        self.mouse_pressed = False
        self.shoot_angle = math.atan2(y - self.first_mouse_pos[1], x - self.first_mouse_pos[0])
        self.shoot_strenght = math.sqrt((y - self.first_mouse_pos[1]) ** 2 + (x - self.first_mouse_pos[0]) ** 2)
        self.bird.shoot(self.shoot_angle, self.shoot_strenght)

        for dot in self.shot_preview.sprite_list:
            dot.center_x = -100
            dot.center_y = -100

    def on_update(self, delta_time):
        self.bird.update()
        self.brick_list.update()
        self.bird.update_animation(delta_time)

        # Deal bird collision with bricks (the bricks should be mouved)
        for brick in self.brick_list:
            if arcade.check_for_collision(self.bird, brick):
                self.bird.change_y *= -1
                brick.hit(1)



def main():
    window = Game()
    arcade.run()

if __name__ == "__main__":
    main()

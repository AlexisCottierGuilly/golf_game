import arcade, random, math

# Constants

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def get_scale_with_size(width, height, sprite):
    return min(width / sprite.width, height / sprite.height)


def get_map(width, height):
    map = []
    for i in range(height):
        map.append([])
        for j in range(width):
            prob = random.random()
            try:
                if j != 0 and map[i][j - 1] == 1:
                    prob = 0.75
                if i != 0 and map[i - 1][j] == 1:
                    prob += 0.2
            except IndexError:
                pass
            if random.random() > prob:
                map[i].append(1)
            else:
                map[i].append(0)
    return map


# Create a golf ball
class Ball(arcade.Sprite):
    def __init__(self):
        super().__init__("C:/Users/cottierguillya/PycharmProjects/Etape_1/copilot_tests2/assets/ball.png", 0.5)
        self.center_x = 100
        self.center_y = 100
        v = random.uniform(-1, 1)
        self.velocity = [v, 2-(v+1)-1]  # direction (total 1.0)
        self.speed = 20  # pixels per frame

    def update(self):
        self.center_x += self.velocity[0] * self.speed
        self.center_y += self.velocity[1] * self.speed


class Wall(arcade.Sprite):
    def __init__(self, x, y, scale):
        super().__init__("C:/Users/cottierguillya/PycharmProjects/Etape_1/copilot_tests2/assets/wall.png", 0.5)
        self.center_x = x
        self.center_y = y
        self.scale = scale

    def update(self):
        pass


# Create a golf hole
class Hole(arcade.Sprite):
    def __init__(self):
        super().__init__("C:/Users/cottierguillya/PycharmProjects/Etape_1/copilot_tests2/assets/hole.png", 0.5)
        self.center_x = 500
        self.center_y = 500

    def update(self):
        pass


# Create a golf game
class GolfGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Golf Game")
        arcade.set_background_color(arcade.color.AMAZON)
        self.ball = Ball()
        self.ball.scale = get_scale_with_size(SCREEN_WIDTH / 35, SCREEN_HEIGHT / 35, self.ball)
        self.hole = Hole()
        self.hole.scale = get_scale_with_size(SCREEN_WIDTH / 20, SCREEN_HEIGHT / 20, self.hole)

        self.walls = arcade.SpriteList()
        self.load_map(get_map(round(SCREEN_WIDTH / 25), round(SCREEN_HEIGHT / 30)))

    def load_map(self, map):
        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == 1:
                    wall = Wall(j * 20, i * 20, 0.5)
                    wall.scale = get_scale_with_size(SCREEN_WIDTH / 25, SCREEN_HEIGHT / 30, wall)
                    self.walls.append(wall)

    def on_draw(self):
        arcade.start_render()
        self.ball.draw()
        self.hole.draw()
        self.walls.draw()

    def update(self, delta_time):
        # Deal ball collision with screen edges
        self.hole.update()
        self.walls.update()

        if SCREEN_WIDTH < self.ball.center_x + self.ball.width / 2:
            self.ball.velocity[0] *= -1
            self.ball.center_x = SCREEN_WIDTH - self.ball.width / 2
        elif self.ball.center_x - self.ball.width / 2 < 0:
            self.ball.velocity[0] *= -1
            self.ball.center_x = self.ball.width / 2

        if SCREEN_HEIGHT < self.ball.center_y + self.ball.height / 2:
            self.ball.velocity[1] *= -1
            self.ball.center_y = SCREEN_HEIGHT - self.ball.height / 2
        elif self.ball.center_y - self.ball.height / 2 < 0:
            self.ball.velocity[1] *= -1
            self.ball.center_y = self.ball.height / 2

        # Deal ball collision with walls
        for wall in self.walls:
            if wall.collides_with_sprite(self.ball):
                # Calculate the angle of the collision
                angle = math.atan2(self.ball.center_y - wall.center_y, self.ball.center_x - wall.center_x)
                # Calculate the new velocity
                self.ball.velocity = [math.cos(angle), math.sin(angle)]
                # Move the ball out of the wall
                self.ball.center_x += self.ball.velocity[0] * self.ball.speed
                self.ball.center_y += self.ball.velocity[1] * self.ball.speed

        # Deal ball collision with hole
        if arcade.check_for_collision(self.ball, self.hole):
            print("You win!")
            arcade.close_window()

        self.ball.update()


def main():
    game = GolfGame()
    arcade.run()


if __name__ == "__main__":
    main()

import pgzrun
import sys
import random

mod = sys.modules['__main__']


def draw():
    """
    Drawing ball, paddle, bars, and background
    """
    if game_status == 'active':
        draw_game_run()
    if game_status == 'game_over':
        draw_game_over()


def draw_game_run():
    mod.screen.blit("background.jpg", (0, 0))
    paddle.draw()
    ball.draw()
    for bar in bars_list:
        bar.draw()


def draw_game_over():
    mod.screen.clear()
    mod.screen.blit("background.jpg", (0, 0))
    game_over.draw()


def update():
    """
    Listening to keyboard events.
    Update coordinates of ball and paddle.
    """
    global ball_x_speed, ball_y_speed, paddle_speed, ball_acceleration, ball_speed_limit, lives, game_status
    if mod.keyboard.left:
        paddle.x = paddle.x - paddle_speed
    if mod.keyboard.right:
        paddle.x = paddle.x + paddle_speed

    update_ball()
    for bar in bars_list:
        if ball.colliderect(bar):
            bars_list.remove(bar)
            ball_y_speed *= -1
            accelerate_ball()

    if paddle.colliderect(ball):
        ball_y_speed *= -1
        # randomly move ball left or right on hit
        rand = random.randint(0, 1)
        if rand:
            ball_x_speed *= -1
    if ball.y > paddle.y:
        lives -= 1
        # global game_status
        if lives == 0:
            game_status = 'game_over'
        ball.x = 30
        ball.y = 300
        paddle.x = 120
        paddle.y = 420


def accelerate_ball():
    """
    Apply ball acceleration.
    """
    global ball_x_speed, ball_y_speed, ball_acceleration, ball_speed_limit
    if abs(ball_x_speed * ball_acceleration) <= ball_speed_limit and \
            abs(ball_y_speed * ball_acceleration) <= ball_speed_limit:
        ball_y_speed *= ball_acceleration
        ball_x_speed *= ball_acceleration


def update_ball():
    """
    Update ball coordinates.
    """
    global ball_x_speed, ball_y_speed
    ball.x -= ball_x_speed
    ball.y -= ball_y_speed
    if (ball.x >= WIDTH) or (ball.x <= 0):
        ball_x_speed *= -1
    if (ball.y >= HEIGHT) or (ball.y <= 0):
        ball_y_speed *= -1


def set_actor(image: str, x: int, y: int) -> mod.Actor:
    """
    Specify an image as pygame zero object.
    :param image:  Image name (should be in 'images' folder).
    :param x: image left border.
    :param y: image right border.
    :return: pygame zero Actor class object.
    """
    actor = mod.Actor(image)
    actor.x = x
    actor.y = y
    return actor


def place_bars():
    """
    Create list of all bars.
    :return:
    """

    def place_bars_line(bars_, x, y, image):
        """
        Creat line of bars with the same color.
        :rtype: object
        """
        bar_x = x
        bar_y = y
        for i in range(8):
            bar = mod.Actor(image)
            bar.x = bar_x
            bar.y = bar_y
            bar_x += 70
            bars_.append(bar)
        return bars_

    coloured_box_list = ["element_blue_rectangle_glossy.png", "element_green_rectangle_glossy.png",
                         "element_red_rectangle_glossy.png"]
    x = 120
    y = 100
    bars = []

    for coloured_box in coloured_box_list:
        bars = place_bars_line(bars, x, y, coloured_box)
        y += 50
    return bars


TITLE = "Arkanoid Alena Reshetnikova project"
WIDTH = 800
HEIGHT = 500
game_status = 'active'

paddle_speed = 7
lives = 3

# ускорение шара, предел скорости шара
ball_x_speed = 2
ball_y_speed = 2
ball_acceleration = 1.2
ball_speed_limit = 6

paddle = set_actor("paddleblue.png", 120, 420)
ball = set_actor("ballblue.png", 30, 300)
bar = set_actor("element_blue_rectangle_glossy.png", 120, 100)
game_over = set_actor("game_over.jpg", WIDTH // 2, HEIGHT // 2)

bars_list = place_bars()

pgzrun.go()

import pgzrun
import sys
import random

mod = sys.modules['__main__']


def draw():
    """
    Drawing ball, paddle, bars, and background
    """
    mod.screen.blit("background.jpg", (0, 0))
    paddle.draw()
    ball.draw()
    for bar in bars_list:
        bar.draw()


def update():
    """
    Listening to keyboard events.
    Update coordinates of ball and paddle.
    """
    global ball_x_speed, ball_y_speed
    if mod.keyboard.left:
        paddle.x = paddle.x - 5
    if mod.keyboard.right:
        paddle.x = paddle.x + 5

    update_ball()
    for bar in bars_list:
        if ball.colliderect(bar):
            bars_list.remove(bar)
            ball_y_speed *= -1

    if paddle.colliderect(ball):
        ball_y_speed *= -1
        # randomly move ball left or right on hit
        rand = random.randint(0, 1)
        if rand:
            ball_x_speed *= -1


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
    bars=[]

    for coloured_box in coloured_box_list:
        bars = place_bars_line(bars, x, y, coloured_box)
        y += 50
    return bars


TITLE = "Arkanoid Alena Reshetnikova project"
WIDTH = 800
HEIGHT = 500

paddle = set_actor("paddleblue.png", 120, 420)
ball = set_actor("ballblue.png", 30, 300)
bar = set_actor("element_blue_rectangle_glossy.png", 120, 100)

ball_x_speed = 1
ball_y_speed = 1

bars_list = place_bars()

pgzrun.go()

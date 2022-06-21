import random
import sys
import os
import pygame
import pgzrun
import time
from settings import *

mod = sys.modules['__main__']


def draw():
    """
    Drawing ball, paddle, bars, and background
    """
    if game_status == 'active':
        draw_game_run()
    if game_status == 'game_over':
        draw_game_over()
    if game_status == "player_won":
        draw_you_won()


def draw_game_run():
    mod.screen.blit(BACKGROUND_IMAGE, (0, 0))
    paddle.draw()
    ball.draw()
    for bar in bars_list:
        bar.draw()
    draw_menu()


def draw_you_won():
    mod.screen.clear()
    mod.screen.blit("background.jpg", (0, 0))
    you_won.draw()


def draw_menu():
    mod.screen.draw.text(f"M - music", (20, 5), color=COLOR_GRAY, fontsize=MENU_TEXT_SIZE)
    draw_ball_lives()


def draw_ball_lives():
    mod.screen.draw.text(f"{lives}", (750, 5), color=COLOR_WHITE_BLUE, fontsize=MENU_TEXT_SIZE)
    mod.screen.blit(BALL_IMAGE, (770, 5))


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
        move_paddle("left")
    if mod.keyboard.right:
        move_paddle("right")
    if mod.keyboard.m:
        music_on_off()

    update_ball()
    for bar in bars_list:
        if ball.colliderect(bar):
            bar_on_hit(bar, BAR_COLORS_LIST)
            ball_y_speed *= -1
            accelerate_ball()
    if bars_list == []:
        game_status = 'player_won'
    if paddle.colliderect(ball):
        ball_y_speed *= -1
        # randomly move ball left or right on hit
        rand = random.randint(0, 1)
        if rand:
            ball_x_speed *= -1
        sound_common_hit()
    if ball.y > paddle.y:
        lives -= 1
        ball_x_speed = 2
        ball_y_speed = 2
        # global game_status
        if lives == 0:
            game_status = 'game_over'
        ball.x = WIDTH // 2
        ball.y = HEIGHT // 2 + 100
        paddle.x = WIDTH // 2
        paddle.y = HEIGHT + 100 // 2 - 100


def move_paddle(direction):
    if direction == "left":
        if paddle.left > 0:
            paddle.x = paddle.x - paddle_speed
    if direction == "right":
        if paddle.right <= WIDTH:
            paddle.x = paddle.x + paddle_speed


def music_on_off():
    global music_status, time_last_key_pressed
    if time.time() - time_last_key_pressed > 0.3 and BACKGROUND_MUSIC:
        if music_status == 'on':
            mod.music.pause()
            music_status = 'off'
            time_last_key_pressed = time.time()
        else:
            mod.music.unpause()
            music_status = 'on'
            time_last_key_pressed = time.time()


def bar_on_hit(hit_bar, color_list):
    if hit_bar.image == color_list[-1]:
        bars_list.remove(hit_bar)
    else:
        hit_bar.image = color_list[color_list.index(hit_bar.image) + 1]
    sound_common_hit()


def sound_common_hit():
    mod.sounds.hit_sound.play()


def accelerate_ball():
    """
    Apply ball acceleration.
    """
    global ball_x_speed, ball_y_speed, ball_acceleration, ball_speed_limit
    ball_y_speed_try = round((abs(ball_y_speed) + ball_acceleration) * (ball_y_speed / abs(ball_y_speed)), 2)
    ball_x_speed_try = round((abs(ball_x_speed) + ball_acceleration) * (ball_x_speed / abs(ball_x_speed)), 2)
    if abs(ball_y_speed_try) <= ball_speed_limit and abs(ball_x_speed_try) <= ball_speed_limit:
        ball_y_speed = ball_y_speed_try
        ball_x_speed = ball_x_speed_try
        print(ball_x_speed, ball_y_speed, ball_acceleration, ball_speed_limit)


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


def place_bars(coloured_box_list):
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
        for i in range(11):
            bar = mod.Actor(image)
            bar.x = bar_x
            bar.y = bar_y
            bar_x += 70
            bars_.append(bar)
        return bars_

    x = 50
    y = 100
    bars = []

    for coloured_box in coloured_box_list:
        bars = place_bars_line(bars, x, y, coloured_box)
        y += 50
    return bars


# TODO 1. 1. Add sounds, refactor ball reflections after hit
# TODO 2. Add levels, save them to separate file with JSON structure
# TODO 3. Panel should not leave game area
# TODO 4. ----Game should create main window in the center of the screen
# TODO 5. Add key 'M' binding for music control (on/off), show in the top menu, refactor it to play without stop
# TODO 6. Refactor acceleration - increment should be added, not multipliyed
# TODO 7. Won / Lose - should stop the game entirely, stop sounds and music


paddle = set_actor(PADDLE_IMAGE, WIDTH // 2, HEIGHT + 100 // 2 - 100)
ball = set_actor(BALL_IMAGE, WIDTH // 2, HEIGHT // 2 + 100)
game_over = set_actor(GAME_OVER_IMAGE, WIDTH // 2, HEIGHT // 2)
you_won = set_actor(YOU_WON_IMAGE, WIDTH // 2, HEIGHT // 2)
time_last_key_pressed = time.time()

bars_list = place_bars(BAR_COLORS_LIST)
if BACKGROUND_MUSIC:
    mod.music.play(BACKGROUND_MUSIC)
    mod.music.set_volume(0.5)

pgzrun.go()

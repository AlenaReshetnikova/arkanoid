import wget
import pathlib

TITLE = "Arkanoid Alena Reshetnikova project"
WIDTH = 800
HEIGHT = 500
game_status = 'active'
music_status = 'on'

paddle_speed = 7
lives = 300

# ускорение шара, предел скорости шара
ball_x_speed = 2
ball_y_speed = 2
ball_acceleration = 0.2
# ball_acceleration = 1
ball_speed_limit = 6

# Bar colors
BAR_RED = "element_red_rectangle_glossy.png"
BAR_BLUE = "element_blue_rectangle_glossy.png"
BAR_GREEN = "element_green_rectangle_glossy.png"
BAR_COLORS_LIST = [BAR_RED, BAR_BLUE, BAR_GREEN]

BALL_IMAGE = "ballblue.png"
PADDLE_IMAGE = "paddleblue.png"
GAME_OVER_IMAGE = "game_over.jpg"
BACKGROUND_IMAGE = "background.jpg"
YOU_WON_IMAGE = "you_won.jpg"

COLOR_WHITE_BLUE = (122, 207, 243)
COLOR_GRAY = (160, 167, 162)
MENU_TEXT_SIZE = 35


# trying to download music from Google drive
def get_background_music(name: str):
    URL = 'https://drive.google.com/u/0/uc?id=1ft4B-Sg5YzdGGpf0zn_YhSQIn8SUr_Or&export=download'
    BACKGROUND_MUSIC_PATH = f'music\{name}.mp3'
    path = pathlib.Path(BACKGROUND_MUSIC_PATH)
    if not path.exists():
        try:
            print('Downloading music')
            wget.download(URL, BACKGROUND_MUSIC_PATH)
        except Exception as ex:
            print(repr(ex))
            print("Can't download music")
            return None
    return name


BACKGROUND_MUSIC = get_background_music('background_music')

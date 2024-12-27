from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

# Constants
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 720
SHOOTER_RADIUS = 20
BULLET_RADIUS = 10
METEOR_MIN_RADIUS = 15
METEOR_MAX_RADIUS = 26
INITIAL_LIVES = 3

# Game State Variables
game = ""
scr = 0
lives = INITIAL_LIVES
misses = 0
bullets = []  # [radius, x, y]
meteors = []  # [radius, x, y]
c_x = WINDOW_WIDTH // 2  # Shooter position
last_frame_time = time.time()

# Circle Drawing

def midpoint_circle(radius, cx, cy):
    x, y = 0, radius
    d = 1 - radius
    draw_symmetric_points(x, y, cx, cy)
    while x < y:
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
        draw_symmetric_points(x, y, cx, cy)

def draw_symmetric_points(x, y, cx, cy):
    glBegin(GL_POINTS)
    glVertex2f(cx + x, cy + y)
    glVertex2f(cx - x, cy + y)
    glVertex2f(cx + x, cy - y)
    glVertex2f(cx - x, cy - y)
    glVertex2f(cx + y, cy + x)
    glVertex2f(cx - y, cy + x)
    glVertex2f(cx + y, cy - x)
    glVertex2f(cx - y, cy - x)
    glEnd()

# AABB Collision Detection
def has_collided(box1, box2):
    return (
        box1['x'] < box2['x'] + box2['width'] and
        box1['x'] + box1['width'] > box2['x'] and
        box1['y'] < box2['y'] + box2['height'] and
        box1['y'] + box1['height'] > box2['y']
    )

# Game Logic Functions
def reset_game():
    global scr, lives, misses, meteors, bullets, game, c_x
    scr = 0
    lives = INITIAL_LIVES
    misses = 0
    meteors = [[random.randint(METEOR_MIN_RADIUS, METEOR_MAX_RADIUS), random.randint(10, WINDOW_WIDTH - 10), WINDOW_HEIGHT] for _ in range(5)]
    bullets = []
    c_x = WINDOW_WIDTH // 2
    game = ""

def animate():
    global meteors, bullets, lives, misses, scr, game, last_frame_time
    current_time = time.time()
    delta_time = current_time - last_frame_time
    last_frame_time = current_time

    if game == "":
        for meteor in meteors:
            meteor[2] -= 100 * delta_time  # Falling speed
            if meteor[2] < SHOOTER_RADIUS:
                lives -= 1
                meteors.remove(meteor)
                meteors.append([random.randint(METEOR_MIN_RADIUS, METEOR_MAX_RADIUS), random.randint(10, WINDOW_WIDTH - 10), WINDOW_HEIGHT])

        for bullet in bullets[:]:
            bullet[2] += 200 * delta_time  # Bullet speed
            if bullet[2] > WINDOW_HEIGHT:
                misses += 1
                bullets.remove(bullet)

        # Collision detection
        for meteor in meteors[:]:
            for bullet in bullets[:]:
                distance = ((meteor[1] - bullet[1]) ** 2 + (meteor[2] - bullet[2]) ** 2) ** 0.5
                if distance < meteor[0] + bullet[0]:
                    scr += 1
                    meteors.remove(meteor)
                    bullets.remove(bullet)
                    meteors.append([random.randint(METEOR_MIN_RADIUS, METEOR_MAX_RADIUS), random.randint(10, WINDOW_WIDTH - 10), WINDOW_HEIGHT])

        if lives <= 0 or misses >= 3:
            game = "over"
    glutPostRedisplay()

def keyboard_listener(key, x, y):
    global c_x, bullets
    if game != "over":
        if key == b'a' and c_x - SHOOTER_RADIUS > 0:
            c_x -= 15
        elif key == b'd' and c_x + SHOOTER_RADIUS < WINDOW_WIDTH:
            c_x += 15
        elif key == b' ':
            bullets.append([BULLET_RADIUS, c_x, SHOOTER_RADIUS])

# Display Function
def display():
    global game, c_x
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Draw shooter
    glColor3f(1, 1, 1)
    midpoint_circle(SHOOTER_RADIUS, c_x, SHOOTER_RADIUS)

    # Draw bullets
    glColor3f(1, 0, 0)
    for bullet in bullets:
        midpoint_circle(bullet[0], bullet[1], bullet[2])

    # Draw meteors
    glColor3f(0, 1, 0)
    for meteor in meteors:
        midpoint_circle(meteor[0], meteor[1], meteor[2])

    glutSwapBuffers()

# Initialization
def initialize_game():
    global meteors, last_frame_time
    meteors = [[random.randint(METEOR_MIN_RADIUS, METEOR_MAX_RADIUS), random.randint(10, WINDOW_WIDTH - 10), WINDOW_HEIGHT] for _ in range(5)]
    last_frame_time = time.time()
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Shoot The Circles!")
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    initialize_game()
    glutMainLoop()

if __name__ == "__main__":
    reset_game()
    main()
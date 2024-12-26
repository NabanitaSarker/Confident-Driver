# Import OpenGL modules
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


window_width = 500
window_height = 700
car_x = 250
car_y = 120

lane_speed = 3.5

shooter_x = window_width // 2
shooter_y = 100
shooter_width = 50
shooter_height = 80
lane_width = 200
cars = []
projectiles = []
score = 0
game_over = False
pause = False
level = 1
level_time = 0


shooter_color = (0.0, 1.0, 0.0)
car_color = (1.0, 0.0, 0.0)
background_color = (0.0, 0.0, 0.0)


car_speed = 5
projectile_speed = 10
level_duration = 700

refill_radius = 10
refill_radius_delta = 1.5
min_refill_radius = 4
max_refill_radius = 20

refill_active = False
refill_timer = 0
refill_lane = None
refill_y = window_height
max_shots = 3



def spawn_refill_logic():
    global refill_timer
    if refill_timer <= 0 and not refill_active:
        spawn_refill()
        refill_timer = random.randint(500, 1000)
    else:
        refill_timer -= 1

def spawn_refill():
    global refill_active, refill_lane, refill_y


    lane_centers = [150, 250, 350]


    available_lanes = []
    for lane in lane_centers:
        is_lane_free = True
        for car in cars:
            if car['x'] == lane and abs(car['y'] - window_height) < shooter_height + 50:
                is_lane_free = False
                break
        if is_lane_free:
            available_lanes.append(lane)


    if available_lanes:
        refill_lane = random.choice(available_lanes)
        refill_y = window_height
        refill_active = True

def check_refill_collision():
    global refill_active, current_shots, max_shots, refill_timer, refill_lane, refill_y

    if refill_active:

        refill_left = refill_lane - 15
        refill_right = refill_lane + 15
        refill_top = refill_y + 15
        refill_bottom = refill_y - 15

        car_left = car_x - 30
        car_right = car_x + 30
        car_top = car_y + 50
        car_bottom = car_y - 50


        if (car_left < refill_right and car_right > refill_left and
            car_top > refill_bottom and car_bottom < refill_top):
            max_shots = 3
            current_shots = max_shots
            refill_active = False


            print("Refill collected! Shots reset.")
            glutPostRedisplay()

def update_refill():
    global refill_y, refill_active
    if not pause:
        if refill_active:
            refill_y -= 3.5


            if refill_y < 0:
                refill_active = False
                refill_y = window_height


def update_refill_circle():
    global refill_radius, refill_radius_delta

    if not pause:
        refill_radius += refill_radius_delta
        if refill_radius >= max_refill_radius or refill_radius <= min_refill_radius:
            refill_radius_delta = -refill_radius_delta


def draw_refill():
    global refill_radius
    if refill_active:
        glColor3f(0.0, 1.0, 0.0)
        draw_circle(refill_lane, refill_y, refill_radius)





def draw_buttons():
    global pause
    start_x = 460
    start_y = 620
    spacing = 80
    button_size = 40


    glColor3f(0.0, 1.0, 1.0)
    line_drawing(start_x - button_size // 2, start_y, start_x + button_size // 2, start_y)
    line_drawing(start_x - button_size // 2, start_y, start_x, start_y - button_size // 2)
    line_drawing(start_x - button_size // 2, start_y, start_x, start_y + button_size // 2)


    glColor3f(1.0, 1.0, 0.0)
    pause_y = start_y - spacing
    if pause:
        line_drawing(start_x - button_size // 2, pause_y - 5, start_x + button_size // 2, pause_y)
        line_drawing(start_x + button_size // 2, pause_y, start_x - button_size // 2, pause_y + 5)
    else:
        line_drawing(start_x - button_size // 4, pause_y - button_size // 2, start_x - button_size // 4,
                     pause_y + button_size // 2)
        line_drawing(start_x + button_size // 4, pause_y - button_size // 2, start_x + button_size // 4,
                     pause_y + button_size // 2)


    glColor3f(1.0, 0.0, 0.0)
    cancel_y = start_y - 2 * spacing
    line_drawing(start_x - button_size // 2, cancel_y + button_size // 2, start_x + button_size // 2,
                 cancel_y - button_size // 2)
    line_drawing(start_x + button_size // 2, cancel_y + button_size // 2, start_x - button_size // 2,
                 cancel_y - button_size // 2)


def stop():
    global pause
    if pause:
        print('Resumed!!')
    else:
        print('pause!!')
    pause = not pause
    glutPostRedisplay()


def cross():
    global score
    print(f'The end!! Score: {score}')
    glutLeaveMainLoop()


def reset():
    global car_x, car_y, lanes, score, pause, over, cars, projectiles, game_over, level, level_time, car_speed, projectile_speed, level_duration, refill_active, refill_timer, refill_lane, refill_y, max_shots,refill_radius ,refill_radius_delta,min_refill_radius ,max_refill_radius
    car_x = 250
    car_y = 120
    lanes = [i for i in range(700, 1400, 100)]

    score = 0
    pause = False
    over = False
    print('Game Reset!')
    max_shots = 3
    cars = []
    projectiles = []

    game_over = False
    level = 1
    level_time = 0

    car_speed = 5
    projectile_speed = 10
    level_duration = 700

    refill_radius = 10
    refill_radius_delta = 1.5
    min_refill_radius = 4
    max_refill_radius = 20
    refill_active = False
    refill_timer = 0
    refill_lane = None
    refill_y = window_height
    max_shots = 3
    car_speed = 5
    projectile_speed = 10
    level_duration = 300



def mouse_callback(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        ogl_x = x
        ogl_y = 700 - y

        button_size = 40
        start_x = 460
        start_y = 620
        spacing = 80


        if (start_x - button_size // 2 <= ogl_x <= start_x + button_size // 2 and
                start_y - button_size // 2 <= ogl_y <= start_y + button_size // 2):
            reset()
            glutPostRedisplay()


        pause_y = start_y - spacing
        if (start_x - button_size // 2 <= ogl_x <= start_x + button_size // 2 and
                pause_y - button_size // 2 <= ogl_y <= pause_y + button_size // 2):
            stop()
            glutPostRedisplay()


        cancel_y = start_y - 2 * spacing
        if (start_x - button_size // 2 <= ogl_x <= start_x + button_size // 2 and
                cancel_y - button_size // 2 <= ogl_y <= cancel_y + button_size // 2):
            cross()
            glutPostRedisplay()
        if game_over:

            button_x = window_width // 2 - 50
            button_y = window_height // 2 - 160
            button_width = 100
            button_height = 40
            if (button_x <= ogl_x <= button_x + button_width and
                    button_y <= ogl_y <= button_y + button_height):
                reset()
                glutPostRedisplay()



def display():
    global game_over, pause

    glClear(GL_COLOR_BUFFER_BIT)

    if game_over:
        draw_game_over_screen()
    else:
        draw_game()
        draw_refill()
        update_refill()
        update_refill_circle()



    glutSwapBuffers()



lanes = [i for i in range(700, 1400, 100)]




def draw_car(x, y):
    glColor3f(0.0, 0.0, 0.0)
    line_drawing(x, y-50 , x, y + 50)
    # Carbody
    glColor3f(0.0, 0.5, 1.0)
    draw_rectangle(x, y, 60, 100)

    draw_buttons()
    # windows
    glColor3f(0.7, 0.9, 1.0)
    draw_rectangle(x, y + 20, 40, 40)
    draw_rectangle(x, y - 20, 40, 40)

    # wheels
    glColor3f(0.3, 0.3, 0.3)
    draw_circle(x - 25, y + 35, 10)
    draw_circle(x + 25, y + 35, 10)
    draw_circle(x - 25, y - 35, 10)
    draw_circle(x + 25, y - 35, 10)

def draw_main_car(x, y):
    glColor3f(0.0, 0.0, 0.0)
    line_drawing(x, y - 50, x, y + 50)
    # Carbody
    glColor3f(1.0, 0.5, 0.7)
    draw_rectangle(x, y, 60, 100)
    draw_buttons()
    # windows
    glColor3f(0.8, 0.8, 0.9)
    draw_rectangle(x, y + 20, 40, 40)
    draw_rectangle(x, y - 20, 40, 40)

    # wheels
    glColor3f(0.3, 0.3, 0.3)
    draw_circle(x - 25, y + 35, 10)
    draw_circle(x + 25, y + 35, 10)
    draw_circle(x - 25, y - 35, 10)
    draw_circle(x + 25, y - 35, 10)



def draw_rectangle(x, y, width, height):
    line_drawing(x - width // 2, y - height // 2, x + width // 2, y - height // 2)
    line_drawing(x + width // 2, y - height // 2, x + width // 2, y + height // 2)
    line_drawing(x + width // 2, y + height // 2, x - width // 2, y + height // 2)
    line_drawing(x - width // 2, y + height // 2, x - width // 2, y - height // 2)



def draw_lanes():

    glColor3f(1.0, 1.0, 1.0)

    # Vertical borders
    line_drawing(100, 0, 100, 700)
    line_drawing(200, 0, 200, 700)
    line_drawing(300, 0, 300, 700)
    line_drawing(400, 0, 400, 700)


    for lane_y in lanes:
        line_drawing(150, lane_y, 150, lane_y - 50)
        line_drawing(250, lane_y, 250, lane_y - 50)
        line_drawing(350, lane_y, 350, lane_y - 50)




def draw_circle(center_x, center_y, r):
    x = 0
    y = r
    d = 1 - r
    while x <= y:
        circle_pixels(x, y, center_x, center_y)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1


def circle_pixels(x, y, cx, cy):
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


def line_drawing(x0, y0, x1, y1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        glBegin(GL_POINTS)
        glVertex2f(x0, y0)
        glEnd()
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


def draw_game():
    global cars, projectiles, score, pause, level, car_x, car_y, max_shots


    draw_lanes()


    draw_main_car(car_x, car_y)

    for car in cars:
        draw_car(car['x'], car['y'])

    draw_text(10, window_height - 30, f"Score: {score}", (1.0, 1.0, 1.0))

    #draw remained bullet
    draw_text(10, window_height - 70, f"Bullet: {max_shots}", (1.0, 1.0, 1.0))

    bullet_spacing = 25
    bullet_start_x = 20
    bullet_y = window_height - 100
    for i in range(max_shots):
        draw_circle(bullet_start_x + i * bullet_spacing, bullet_y, 10)


    for projectile in projectiles:
        draw_circle(projectile['x'], projectile['y'], 10)

    draw_text(window_width // 2 - 50, window_height - 50, f"Level {level}", (1.0, 1.0, 0.0))
    draw_refill()
    if pause:
        draw_text(window_width // 2 - 50, window_height // 2, "pause", (1.0, 1.0, 0.0))



def draw_game_over_screen():
    glColor3f(1.0, 0.0, 0.0)
    line_drawing(150, 450, 200, 450)
    line_drawing(150, 450, 150, 400)
    line_drawing(150, 400, 200, 400)
    line_drawing(200, 400, 200, 425)
    line_drawing(175, 425, 200, 425)

    # A
    line_drawing(210, 400, 230, 450)
    line_drawing(230, 450, 250, 400)
    line_drawing(220, 425, 240, 425)

    # M
    line_drawing(260, 400, 260, 450)
    line_drawing(260, 450, 280, 425)
    line_drawing(280, 425, 300, 450)
    line_drawing(300, 450, 300, 400)

    # E
    line_drawing(310, 400, 310, 450)
    line_drawing(310, 450, 340, 450)
    line_drawing(310, 425, 330, 425)
    line_drawing(310, 400, 340, 400)

    # O
    line_drawing(150, 350, 200, 350)
    line_drawing(150, 350, 150, 300)
    line_drawing(150, 300, 200, 300)
    line_drawing(200, 300, 200, 350)

    # V
    line_drawing(210, 350, 230, 300)
    line_drawing(230, 300, 250, 350)

    # E
    line_drawing(260, 300, 260, 350)
    line_drawing(260, 350, 290, 350)
    line_drawing(260, 325, 280, 325)
    line_drawing(260, 300, 290, 300)

    # R
    line_drawing(300, 300, 300, 350)
    line_drawing(300, 350, 330, 350)
    line_drawing(330, 350, 330, 325)
    line_drawing(330, 325, 300, 325)
    line_drawing(300, 325, 330, 300)

    button_x = window_width // 2 - 50
    button_y = window_height // 2 - 160
    button_width = 100
    button_height = 40


    glColor3f(0.0, 1.0, 0.5)
    draw_rectangle(button_x + button_width // 2, button_y + button_height // 2, button_width, button_height)


    draw_text(button_x + 10, button_y + 15, "RESTART", (0.0, 1.0, 0.5))

    draw_text(window_width // 2 - 55, window_height // 2 -100 , f"Final Score: {score}", (1.0, 1.0, 0.0))
    draw_text(window_width // 2 - 80, window_height // 2 - 190, "Or press R to restart", (0.0, 0.5, 0.5))


# Draw text on screen
def draw_text(x, y, text, color):
    glColor3f(*color)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))



last_speed_increase_time = 0



def check_aabb_collision(a, b):

    return (a['x'] < b['x'] + b['width'] and
            a['x'] + a['width'] > b['x'] and
            a['y'] < b['y'] + b['height'] and
            a['y'] + a['height'] > b['y'])



def check_collisions():
    global cars, projectiles, score, game_over


    for projectile in projectiles[:]:
        for car in cars[:]:
            if check_aabb_collision(projectile, car):
                projectiles.remove(projectile)
                cars.remove(car)
                score += 10
                break


    shooter_box = {
        'x': car_x - shooter_width // 2,
        'y': car_y,
        'width': shooter_width,
        'height': shooter_height}
    for car in cars[:]:
        if check_aabb_collision(shooter_box, car):
            game_over = True
            break

def spawn_car():
    global shooter_height


    lane_centers = [150, 250, 350]


    lane = random.randint(0, 2)
    x = lane_centers[lane]
    y = window_height


    for car in cars:
        if car['x'] == x and car['y'] > window_height - shooter_height - 50:
            return


    cars.append({'x': x, 'y': y, 'width': shooter_width, 'height': shooter_height})



def fire_projectile():
    global projectiles, max_shots
    projectile_width = 10
    projectile_height = 20
    max_shots -= 1

    projectiles.append({
        'x': car_x - projectile_width // 2,
        'y': car_y + 50,
        'width': projectile_width,
        'height': projectile_height
    })



def special_key_handler(key, x, y):
    global car_x, pause, game_over, max_shots

    step = 100

    if key == GLUT_KEY_LEFT and not pause:
        if car_x > 150:
            car_x -= step
    elif key ==GLUT_KEY_RIGHT and not pause:
        if car_x < 350:
            car_x += step



def keyboard(key, x, y):
    global car_x, pause, game_over, max_shots

    step = 100

    if key == b'a' and not pause:
        if car_x > 150:
            car_x -= step
    elif key == b'd' and not pause:
        if car_x < 350:
            car_x += step
    elif key == b' ' and not pause and max_shots>0:
        fire_projectile()

    elif key == b'p':
        pause = not pause
    elif key == b'r' and game_over:
        restart_game()

    glutPostRedisplay()



def restart_game():
    global cars, projectiles, score, game_over, pause, level, level_time, car_speed, max_shots
    cars = []
    projectiles = []
    score = 0
    game_over = False
    pause = False
    level = 1
    level_time = 0
    car_speed = 5
    max_shots=3


def update(value):
    global cars, projectiles, score, game_over, pause, level, level_time, car_speed, lane_speed, refill_y, refill_active

    if not game_over and not pause:

        for car in cars[:]:
            car['y'] -= car_speed
            if car['y'] < -shooter_height:
                cars.remove(car)
                score += 1


        for projectile in projectiles[:]:
            projectile['y'] += projectile_speed
            if projectile['y'] > window_height:
                projectiles.remove(projectile)

        if refill_active:
            refill_y -= 1


            if refill_y < 0:
                refill_active = False

        check_collisions()
        update_refill()
        update_refill_circle()
        check_refill_collision()
        spawn_refill_logic()
        draw_refill()

        for i in range(len(lanes)):
            lanes[i] -= lane_speed
            if lanes[i] < -50:
                lanes[i] = 750


        if random.random() < 0.01:
            spawn_car()


        level_time += 1
        if level_time >= level_duration:
            level_time = 0
            level += 1
            car_speed += 2
            lane_speed += 2
            refill_y -=2



    glutPostRedisplay()


    glutTimerFunc(16, update, 0)


# Initialize OpenGL
def init_gl():
    glClearColor(*background_color, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)


# Main function
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(window_width, window_height)
glutCreateWindow(b"Car Shooting Game")
init_gl()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special_key_handler)
glutMouseFunc(mouse_callback)
glutTimerFunc(16, update, 0)
glutMainLoop()
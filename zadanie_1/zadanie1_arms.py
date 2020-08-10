import pygame
from pygame.locals import DOUBLEBUF
from pygame.locals import OPENGL
from OpenGL.GL import glVertex2f
from OpenGL.GL import glColor4f
from OpenGL.GLU import gluOrtho2D
from OpenGL.GL import glClear
from OpenGL.GL import glBegin
from OpenGL.GL import glEnd
from OpenGL.GL import glPushMatrix
from OpenGL.GL import glTranslated
from OpenGL.GL import glRotated
from OpenGL.GL import glCallList
from OpenGL.GL import glPopMatrix
from OpenGL.GL import glGenLists
from OpenGL.GL import glNewList
from OpenGL.GL import glEndList
from OpenGL.GL import GL_COMPILE
from OpenGL.GL import GL_POLYGON
from OpenGL.GL import GL_COLOR_BUFFER_BIT
from OpenGL.GL import GL_DEPTH_BUFFER_BIT
# from OpenGL.GLU import gluPerspective
# from OpenGL.GL import glTranslatef
# from OpenGL.GL import glRotatef


def my_paint_1(params):
    glColor4f(1.0, 0.0, 0.0, 1.0)
    glCallList(params['arm_part'])


def my_paint_2(params):
    glPushMatrix()
    glTranslated(params['pos_x'], params['pos_y'], 0)
    glRotated(params['angle_1'], 0, 0, 1)
    glColor4f(1.0, 0.0, 0.0, 1.0)
    glCallList(params['arm_part'])
    glPopMatrix()


def my_paint_3(params):
    glPushMatrix()
    glTranslated(params['pos_x'], params['pos_y'], 0)
    glRotated(params['angle_1'], 0, 0, 1)
    glPushMatrix()
    glTranslated(90, 0, 0)
    glRotated(params['angle_2'], 0, 0, 1)
    glColor4f(0.0, 1.0, 0.0, 1.0)
    glCallList(params['arm_part'])
    glPopMatrix()
    glColor4f(1.0, 0.0, 0.0, 1.0)
    glCallList(params['arm_part'])
    glPopMatrix()


def show_arms(paint_function):
    params = {
        'pos_x': 0,
        'pos_y': 0,
        'angle_1': 0,
        'angle_2': 0,
        'arm_part': 0,
        'right_down_pos': (0, 0),
        'left_down_pos': (0, 0),
        'right_button_down': False,
        'left_button_down': False
    }

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    rate = display[0] / display[1]
    # gluPerspective(45, rate, 0.1, 50.0)
    gluOrtho2D(0.0, 500.0*rate, 0.0, 500.0)
    # glTranslatef(0.0, 0.0, -5)
    params['arm_part'] = glGenLists(1)

    glNewList(params['arm_part'], GL_COMPILE)
    glBegin(GL_POLYGON)
    glVertex2f(-10.0, 10.0)
    glVertex2f(-10.0, -10.0)
    glVertex2f(100.0, -10.0)
    glVertex2f(100.0, 10.0)
    glEnd()
    glEndList()

    done = False

    while True:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT, pygame.KEYDOWN, pygame.K_q]:
                pygame.quit()
                done = True
            elif event.type == pygame.MOUSEMOTION:
                if params['left_button_down']:
                    params['angle_1'] += params['left_down_pos'][0] - event.pos[0]
                    params['angle_2'] += params['left_down_pos'][1] - event.pos[1]
                    params['left_down_pos'] = event.pos
                elif params['right_button_down']:
                    params['pos_x'] -= params['right_down_pos'][0] - event.pos[0]
                    params['pos_y'] += params['right_down_pos'][1] - event.pos[1]
                    params['right_down_pos'] = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    params['left_button_down'] = True
                    params['left_down_pos'] = event.pos
                elif event.button == 3:
                    params['right_button_down'] = True
                    params['right_down_pos'] = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    params['left_button_down'] = False
                elif event.button == 3:
                    params['right_button_down'] = False

            if done:
                break

        if done:
            break

        # glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        paint_function(params)
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    show_arms(my_paint_3)

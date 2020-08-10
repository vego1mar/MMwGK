import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


def main():
    vertices = (
        (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),  # front
        (1, -1, 1), (1, 1, 1), (-1, 1, 1), (-1, -1, 1)  # back
    )
    edges = (
        (0, 3), (0, 1), (0, 4),  # front top left; change in (x, y, z)
        (2, 1), (2, 3), (2, 6),  # front bottom right
        (5, 6), (5, 4), (5, 1),  # back bottom right; while facing at the wall straight
        (7, 4), (7, 6), (7, 3)  # back top left
    )
    surfaces = (
        (0, 1, 2, 3), (7, 6, 5, 4),  # front and back
        (4, 5, 1, 0), (3, 2, 6, 7),  # left and right
        (4, 0, 3, 7), (1, 5, 6, 2)  # top and bottom
    )
    colors = (
        (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (1, 1, 0), (0, 1, 1)
    )

    initialize()
    graphics_args = {
        'vertices': vertices,
        'edges': edges,
        'surfaces': surfaces,
        'colors': colors
    }
    graphics_loop(graphics_args)


def draw_cube(args):
    draw_surfaces(args)
    draw_lines(args)


def draw_lines(args):
    glEnable(GL_DEPTH_TEST)
    glBegin(GL_LINES)

    for edge in args['edges']:
        for vertex in edge:
            glVertex3fv(args['vertices'][vertex])

    glEnd()
    glDisable(GL_DEPTH_TEST)


def draw_surfaces(args):
    glEnable(GL_DEPTH_TEST)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glBegin(GL_QUADS)
    i = 0

    for surface in args['surfaces']:
        surface_color = args['colors'][i]
        i += 1

        for vertex in surface:
            glColor3fv(surface_color)
            glVertex3fv(args['vertices'][vertex])

    glEnd()
    glDisable(GL_DEPTH_TEST)


def on_keydown_pressed(event):
    if event.key == pygame.K_LEFT:
        glTranslatef(-1, 0, 0)
    elif event.key == pygame.K_RIGHT:
        glTranslatef(1, 0, 0)
    elif event.key == pygame.K_UP:
        glTranslatef(0, 1, 0)
    elif event.key == pygame.K_DOWN:
        glTranslatef(0, -1, 0)


def on_mouse_motion(event, button_down):
    if button_down:
        glRotatef(event.rel[1], 1, 0, 0)
        glRotatef(event.rel[0], 0, 1, 0)


def graphics_loop(args):
    button_down = False
    done = False

    glMatrixMode(GL_MODELVIEW)
    model_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)

    while not done:
        glPushMatrix()
        glLoadIdentity()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                done = True

            if done:
                break

            if event.type == pygame.KEYDOWN:
                on_keydown_pressed(event)

            if event.type == pygame.MOUSEMOTION:
                on_mouse_motion(event, button_down)

        if done:
            break

        for _ in pygame.mouse.get_pressed():
            if pygame.mouse.get_pressed()[0] == 1:
                button_down = True
            elif pygame.mouse.get_pressed()[0] == 0:
                button_down = False

        # glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMultMatrixf(model_matrix)
        model_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glLoadIdentity()
        glTranslatef(0, 0, -1)
        glMultMatrixf(model_matrix)
        draw_cube(args)
        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)


def initialize():
    pygame.init()
    display = (1024, 728)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    display_ratio = display[0] / display[1]

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, display_ratio, 1, 10)
    glTranslatef(0.0, 0.0, -5.0)


if __name__ == '__main__':
    main()

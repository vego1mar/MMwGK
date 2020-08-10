import pygame
from pygame.locals import DOUBLEBUF
from pygame.locals import OPENGL
from OpenGL.GLU import gluOrtho2D
from OpenGL.GL import glClear
from OpenGL.GL import glBegin
from OpenGL.GL import glEnd
from OpenGL.GL import glVertex2f
from OpenGL.GL import glColor4f
from OpenGL.GL import GL_POLYGON
from OpenGL.GL import GL_COLOR_BUFFER_BIT
from OpenGL.GL import GL_DEPTH_BUFFER_BIT
# from OpenGL.GLU import gluPerspective
# from OpenGL.GL import glTranslatef
# from OpenGL.GL import glRotatef


def triangle_paint():
    glBegin(GL_POLYGON)
    glColor4f(1.0, 0.0, 0.0, 1.0)
    glVertex2f(100.0, 50.0)
    glColor4f(0.0, 1.0, 0.0, 1.0)
    glVertex2f(450.0, 450.0)
    glColor4f(0.0, 0.0, 1.0, 1.0)
    glVertex2f(450.0, 50.0)
    glEnd()


def triangle_show():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    rate = display[0] / display[1]
    # gluPerspective(45, 500.0*rate, 0.1, 50.0)
    gluOrtho2D(0.0, 500.0*rate, 0.0, 500.0)
    # glTranslatef(0.0, 0.0, -5.0)
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                done = True

        if not done:
            # glRotatef(1.0, 3.0, 1.0, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            triangle_paint()
            pygame.display.flip()
            pygame.time.wait(25)


if __name__ == '__main__':
    triangle_show()

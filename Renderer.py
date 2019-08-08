import pygame as pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import glPointSize, GL_TRIANGLES, GL_POINTS, glVertex3fv, glColor3fv, glRotatef, glTranslatef, glBegin, glEnable, glEnd, glClear, GL_DEPTH_TEST, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
from OpenGL.GLU import gluPerspective
from Objloader import Objloader


class Renderer:
    def __init__(self, badch, color1):
        # load headcap
        headcap = Objloader()
        self.vertices = headcap.loader('headcap_version2.obj')

        # vertices = headcap.vertices
        self.edges = headcap.index

        # bad channels list 0-15
        self.bad_channels = badch

        # load head
        head = Objloader()
        self.vertices2 = head.loader('head.obj')
        self.edges2 = head.index

        # color data
        self.color = color1

    def EEGCap(self, col):
        glBegin(GL_TRIANGLES)
        for edge in self.edges:
            for vertex in edge:
                x = vertex % 15
                glColor3fv(col[3*x:3*(x+1)])
                glVertex3fv(self.vertices[vertex])
        glEnd()

    def Head(self):
        glBegin(GL_TRIANGLES)
        for edge in self.edges2:
            for vertex in edge:
                glColor3fv([0.2, 0.2, 0.2])
                glVertex3fv(self.vertices2[vertex])
        glEnd()

    def RenderPoints(self):
        glPointSize(14)
        glBegin(GL_POINTS)
        for i in range(len(self.vertices)):
            if i not in self.bad_channels:
                glColor3fv([0.1, 0.7, 0.1])
                glVertex3fv(self.vertices[i])
        glEnd()
        glPointSize(20)
        glBegin(GL_POINTS)
        for vertex in self.bad_channels:
            glColor3fv([1.0, 0.1, 0.2])
            glVertex3fv([i*1.01 for i in self.vertices[vertex]])
        glEnd()

    def render(self):
        limit = len(self.color)
        # flags
        show_head = False
        drag_lock = False
        is_paused = False
        autorotate_enable = False
        # counters
        m = 0
        ind = 0
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        gluPerspective(45, 4/3, 0.1, 50.0)
        now = []
        glTranslatef(0.0, 0.0, -5)
        glRotatef(0, 0, 0, 0)
        glEnable(GL_DEPTH_TEST)
        speed = 50
        color_len = len(self.color[0])
        diff = []
        for i in range(color_len):
            diff.append((self.color[(m+1) % limit]
                         [i] - self.color[m][i]) / speed)

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if pygame.key.get_focused() and pygame.key.get_pressed()[K_SPACE]:
                        is_paused = not is_paused

                    if pygame.key.get_focused() and pygame.key.get_pressed()[K_GREATER]:
                        if speed > 5:
                            speed -= 5
                    if pygame.key.get_focused() and pygame.key.get_pressed()[K_LESS]:
                        speed += 5
                    if pygame.key.get_focused() and pygame.key.get_pressed()[K_n]:
                        show_head = not show_head
                    if pygame.key.get_focused() and pygame.key.get_pressed()[K_b]:
                        autorotate_enable = not autorotate_enable
                if drag_lock:
                    prev = now
                    now = pygame.mouse.get_pos()
                    glRotatef(1, 0, (now[0]-prev[0])/8, 0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        glTranslatef(0, 0, 1.0)
                    if event.button == 5:
                        glTranslatef(0, 0, -1.0)
                    if event.button == 1:
                        drag_lock = True
                        now = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        drag_lock = False

            if autorotate_enable:
                glRotatef(0.4, 0, 0.4, 0)
            if not is_paused:
                ind += 1
                if ind % speed == 0 and m < limit - 1:
                    ind = 0
                    m = (m+1) % limit
                    for i in range(color_len):
                        diff.append(
                            (self.color[(m+1) % limit][i] - self.color[m][i]) / speed)
                col = [self.color[m][i] + (diff[i])*(ind+1)
                       for i in range(color_len)]

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            if show_head:
                self.Head()
            self.EEGCap(col)
            self.RenderPoints()
            pygame.display.flip()
            pygame.time.wait(10)

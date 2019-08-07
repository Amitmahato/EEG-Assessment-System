import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Objloader import Objloader

class Renderer:
    def __init__(self,badch,color1):
        # load headcap
        headcap = Objloader()
        self.vertices = headcap.loader('headcap_version2.obj')
        
        # vertices = headcap.vertices
        self.edges = headcap.index

        # bad channels list 0-15
        self.bader = badch

        #load head 
        head = Objloader()
        self.vertices2 = head.loader('head.obj')
        self.edges2 = head.index


        # color data
        self.color = color1
        self.showhead = False    

    def Cube(self,col):
        glBegin(GL_TRIANGLES)
        for edge in self.edges:
            for vertex in edge:
                x=vertex%15
                glColor3fv(col[3*x:3*(x+1)])
                
                glVertex3fv(self.vertices[vertex])   
        glEnd()

    def Head(self):
        glBegin(GL_TRIANGLES)
        for edge in self.edges2:
            for vertex in edge:
                glColor3fv([0.2,0.2,0.2])
                glVertex3fv(self.vertices2[vertex])   
        glEnd()

    def bad(self):
        glPointSize(14)
        glBegin(GL_POINTS)
        for i in range(len(self.vertices)):
            glColor3fv([0.1,0.7,0.1])
            glVertex3fv(self.vertices[i])
        glEnd()
        glPointSize(20)
        glBegin(GL_POINTS)
        for vertex in self.bader:
            glColor3fv([1.0,0.1,0.2])
            glVertex3fv([i*1.01 for i in self.vertices[vertex]])
        glEnd()

    def render(self):
        limit = len(self.color)
        m = 0
        ind = 0
        pygame.init()
        display = (800,600)
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
        p_tr = False
        rectangle_draging = False
        pause = False
        autorotate = False
        gluPerspective(45 , 4/3 , 0.1 ,50.0)
        now = []
        glTranslatef(0.0,0.0,-5)
        glRotatef(0,0,0,0)
        glEnable(GL_DEPTH_TEST)
        x=50
        color_len = len(self.color[0])
        speed = 10
        diff = []
        for i in range(color_len):
            diff.append((self.color[(m+1)%limit][i] - self.color[m][i]) / x)

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                
                if event.type == pygame.KEYDOWN:
                    if pygame.key.get_focused() and pygame.key.get_pressed()[K_SPACE]:
                        pause = not pause
                    if pygame.key.get_focused() and pygame.key.get_pressed()[K_GREATER]:
                        speed +=5
                    if pygame.key.get_focused() and pygame.key.get_pressed()[K_LESS]:
                        if speed > 5:
                            speed -=5
                if rectangle_draging:
                    prev = now
                    now = pygame.mouse.get_pos()
                    glRotated(1,(now[1]-prev[1])/speed,(now[0]-prev[0])/speed,0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        glTranslatef(0,0,1.0)
                    if event.button == 5:
                        glTranslatef(0,0,-1.0)
                    if event.button == 1:            
                        rectangle_draging = True
                        now = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:            
                        rectangle_draging = False

                # if rectangle_draging:
                #     motion = pygame.mouse.get_rel()
                #     print(motion,motion[0],motion[1])
                #     glRotatef(1,motion[1],motion[0] ,0)

                # glClearColor(1.0, 1.0, 1.0, 1.0)
            if not pause:
                if autorotate:
                    glRotatef(0.4, 0, 0.4, 0)
                ind += 1  
                if ind % x == 0 and m < limit - 1:
                    ind = 0
                    m = (m+1)%limit
                    # print(m)
                    for i in range(color_len):
                        diff.append((self.color[(m+1)%limit][i] - self.color[m][i]) / x)
                col = [self.color[m][i] + (diff[i])*(ind+1) for i in range(color_len)]

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            if self.showhead:
                self.Head()
            self.Cube(col)
            self.bad()
            pygame.display.flip()
            pygame.time.wait(10)
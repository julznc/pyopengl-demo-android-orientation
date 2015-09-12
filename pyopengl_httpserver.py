#!/usr/bin/python3

# yus 20150912

import socket, threading, sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class MyReqHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            azimuth, pitch, roll = self.path.split(',')
            rotX = float(roll) * 57.296 + 90.0
            rotY = float(pitch) * 57.296 + 0.0
            rotZ = float(azimuth) * 57.296 + 0.0
            print(rotX, rotY, rotZ)
            self.server.setRotations(rotX, rotY, rotZ)
        except:
            pass
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'<html><head><title>Title</title></head>')
        self.wfile.write(b'<body><p>ok</p></body>')
        self.wfile.write(b'</html>')

class MyServer(HTTPServer, threading.Thread):
    def __init__(self):
        self.hostName = socket.gethostbyname(socket.gethostname())
        self.hostPort = 8080
        HTTPServer.__init__(self, (self.hostName, self.hostPort), MyReqHandler)
        threading.Thread.__init__(self)

        self.rotX, self.rotY, self.rotZ = 20.0, 40.0, 30.0
        
    def run(self):
        print('Server Starts - %s:%s' % (self.hostName, self.hostPort))
        self.serve_forever()
        #self.server_close()
        print('Server Stoped')

    def getRotations(self):
        return self.rotX, self.rotY, self.rotZ

    def setRotations(self, rx, ry, rz):
        self.rotX, self.rotY, self.rotZ = rx, ry, rz
        
class MyGLDisplay:
    def __init__(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

        width, height = 640, 480
        glutInitWindowSize(width, height)
        window = glutCreateWindow(b'Android Orientation')
        self.server = MyServer()

        # Initialize our window.
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

        self.ReSizeGLScene(width, height)

        glutDisplayFunc(self.DrawGLScene)
        glutIdleFunc(self.DrawGLScene)
        glutReshapeFunc(self.ReSizeGLScene)
        glutKeyboardFunc(self.keyPressed)

    def loop(self):
        # Start Event Processing Engine
        self.server.start()
        #print('press Esc to stop')
        glutMainLoop()
        

    def ReSizeGLScene(self, Width, Height):
        glViewport(0, 0, Width, Height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def DrawGLScene(self):        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        glLoadIdentity();
        glTranslatef(0.0,0.0,-32.0);

        rotX, rotY, rotZ = self.server.getRotations()
        glRotatef(rotX,1.0,0.0,0.0)
        glRotatef(rotY,0.0,1.0,0.0)
        glRotatef(rotZ,0.0,0.0,1.0)
        glBegin(GL_QUADS);

        glColor3f(0.0,1.0,0.0)     # 1
        glVertex3f( 4.0, 8.0,-1.0)
        glVertex3f(-4.0, 8.0,-1.0)
        glVertex3f(-4.0, 8.0, 1.0)
        glVertex3f( 4.0, 8.0, 1.0)

        glColor3f(1.0,0.5,0.0)     # 2
        glVertex3f( 4.0,-8.0, 1.0)
        glVertex3f(-4.0,-8.0, 1.0)
        glVertex3f(-4.0,-8.0,-1.0)
        glVertex3f( 4.0,-8.0,-1.0)

        glColor3f(1.0,0.0,0.0)     # 3
        glVertex3f( 4.0, 8.0, 1.0)
        glVertex3f(-4.0, 8.0, 1.0)
        glVertex3f(-4.0,-8.0, 1.0)
        glVertex3f( 4.0,-8.0, 1.0)

        glColor3f(1.0,1.0,0.0)     # 4
        glVertex3f( 4.0,-8.0,-1.0)
        glVertex3f(-4.0,-8.0,-1.0)
        glVertex3f(-4.0, 8.0,-1.0)
        glVertex3f( 4.0, 8.0,-1.0)

        glColor3f(0.0,0.0,1.0)     # 5
        glVertex3f(-4.0, 8.0, 1.0)
        glVertex3f(-4.0, 8.0,-1.0)
        glVertex3f(-4.0,-8.0,-1.0)
        glVertex3f(-4.0,-8.0, 1.0)

        glColor3f(1.0,0.0,1.0)     # 6
        glVertex3f( 4.0, 8.0,-1.0)
        glVertex3f( 4.0, 8.0, 1.0)
        glVertex3f( 4.0,-8.0, 1.0)
        glVertex3f( 4.0,-8.0,-1.0)

        glEnd();
        glutSwapBuffers()

    def keyPressed(self, *args):
        if args[0] == b'\x1b': #  ESC
            self.server.shutdown()
            sys.exit()

if __name__ == '__main__':
    disp = MyGLDisplay()
    disp.loop()



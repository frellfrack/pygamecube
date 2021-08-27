#!/usr/bin/python3
import pygame
from math import pi,sin,cos
from time import sleep

# Why didn't I pay attention in maths at schooooooollllll?

class cube:
    def __init__(self):
        pygame.init()
        self.width=1024
        self.height=768
        self.size = [self.width,self.height]
        self.screen = pygame.display.set_mode(self.size)  
        pygame.display.set_caption("Cube")

        self.centreX = self.width/2
        self.centreY = self.height/2
        self.labelColour=(255,255,255)
        self.backgroundColour = (0,0, 0)
        self.nodeColour = (255, 255, 250)
        self.edgeColour = (0, 100, 255)
        self.nodeSize = 4.5
        self.fillColour=(0,0,50)
        
        self.options =[
        {'label':"Start / Stop",'callback': 'self.startStop()' },
        {'label':'Up', 'callback': 'self.rotateX3D(-0.01)'},
        {'label':'Down', 'callback': 'self.rotateX3D(0.01)'},
        {'label':'Left', 'callback': 'self.rotateY3D(0.01)'},
        {'label':'Right', 'callback': 'self.rotateY3D(-0.01)'},
        {'label':'Zoom In', 'callback': 'self.zoom(1.01)'},
        {'label':'Zoom Out', 'callback': 'self.zoom(0.99)'}
        ]
        
        self.optionsLen = len(self.options)
        self.optionColour = (100,100,100)
        self.optionHeight = 40
        self.optionWidth =160
        self.optionSpacer=1
        self.menuHeight = self.optionsLen * self.optionHeight + self.optionSpacer
        self.menuWidth = self.optionWidth
        self.menuTop = 1
        self.menuLeft = self.width-self.menuWidth-2
        self.menuBottom = self.menuTop + self.menuHeight
        self.menuRight = self.menuLeft+self.menuWidth
        
        #coordinates for corners of cube in x,y,z relative to zero  
        self.nodes= [
        [-150, -150, -150],
        [-150, -150,  150],
        [-150,  150, -150],
        [-150,  150,  150],
        [ 150, -150, -150],
        [ 150, -150,  150],
        [ 150,  150, -150],
        [ 150,  150,  150]
        ]
        self.nodLen = len(self.nodes)
       
        self.edges= [
        [0, 1],
        [1, 3],
        [3, 2],
        [2, 0],
        [4, 5],
        [5, 7],
        [7, 6],
        [6, 4],
        [0, 4],
        [1, 5],
        [2, 6],
        [3, 7]
        ]
        self.edgeLen = len(self.edges)
        
        self.surfaces =[
        [0,1,3,2,(255,0,0)],
        [1,0,4,5,(200,0,50)],
        [1,5,7,3,(150,0,100)],
        [0,4,6,2,(100,0,150)],
        [2,3,7,6,(50,0,200)],
        [6,4,5,7,(0,0,255)]
        ]        
        self.surfaceLen = len(self.surfaces)        


        self.clock = pygame.time.Clock()        
        self.animate = False
        self.mouseDown = False
        self.clickStart =[]
        self.clickFinish=[]
        
        #self.rotateX3D(10)
        #self.rotateY3D(10)
        #self.rotateZ3D(10)
        
        self.mainLoop()
        
    def mainLoop(self):
        self.done = False
        while not self.done:
            self.captureEvents()
            if (self.animate==True):
                self.rotateX3D(0.01)
                self.rotateY3D(0.01)
                self.rotateZ3D(0.01) 
                sleep(0.01)
                self.drawCube()
            else:
                self.drawCube() # no need to redraw if nothing has changed             
                while (self.animate==False and self.done == False):
                    self.captureEvents()
                    sleep(0.01)
        pygame.quit()
        
    def captureEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                self.done=True     
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouseDown = True
                mouse_presses = pygame.mouse.get_pressed()
                x,y = pygame.mouse.get_pos()
                if (x > self.menuLeft and y < self.menuBottom):
                    for i in range(0, self.optionsLen, 1):                
                        top = self.menuTop+(self.optionHeight+self.optionSpacer)*i
                        bottom = top+self.optionHeight
                        if(y > top and y < bottom):
                            eval(self.options[i]['callback'])
                self.clickStart = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouseDown = False
                self.clickFinish = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEWHEEL:
                if(event.y < 0):
                    self.zoom(1.01)
                else:
                    self.zoom(0.99)
                self.doOrDoNot()
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP):
                    self.rotateX3D(0.01)
                elif (event.key == pygame.K_DOWN):
                    self.rotateX3D(-0.01)
                elif (event.key == pygame.K_LEFT):
                    self.rotateY3D(0.01)
                elif (event.key == pygame.K_RIGHT):
                    self.rotateY3D(-0.01)
                elif (event.key == pygame.K_EQUALS):
                    self.zoom(1.01)
                elif (event.key == pygame.K_MINUS):
                    self.zoom(0.99)
                elif (event.key == pygame.K_SPACE):
                    self.startStop()
                elif (event.key == pygame.K_q):
                    self.done=True  
                self.doOrDoNot()  
            if (self.mouseDown==True):
                x,y = pygame.mouse.get_pos()
                self.rotateX3D(-((y-self.clickStart[1])/10000));      
                self.rotateY3D((x-self.clickStart[0])/10000);
                self.doOrDoNot()

    def startStop (self):
        if (self.animate==False):
            self.animate=True
        else:
            self.animate=False

    def doOrDoNot (self):
        if (self.animate == False):
            self.drawCube()
            
    def rotateX3D(self,theta):
        sinTheta = sin(theta)
        cosTheta = cos(theta)
        for i in range(0, self.nodLen, 1):
            y = self.nodes[i][1]
            z = self.nodes[i][2]
            self.nodes[i][1] = y * cosTheta - z * sinTheta
            self.nodes[i][2] = z * cosTheta + y * sinTheta
                
    def rotateY3D(self,theta):
        sinTheta = sin(theta)
        cosTheta = cos(theta)
        for i in range(0, self.nodLen, 1):
            x = self.nodes[i][0]
            z = self.nodes[i][2] 
            self.nodes[i][0] = x * cosTheta + z * sinTheta
            self.nodes[i][2] = z * cosTheta - x * sinTheta

    def rotateZ3D(self, theta):
        sinTheta = sin(theta)
        cosTheta = cos(theta)
        for i in range(0, self.nodLen, 1):
            x = self.nodes[i][0]
            y = self.nodes[i][1]
            self.nodes[i][0] = x * cosTheta - y * sinTheta
            self.nodes[i][1] = y * cosTheta + x * sinTheta

    def zoom(self,z):
        for y in range(0, len(self.nodes), 1):
            for x in range(0, len(self.nodes[y]), 1):
                self.nodes[y][x]=self.nodes[y][x]*z    

    def drawCube(self):
        self.screen.fill(self.backgroundColour)
        self.drawFaces()
        #self.drawEdges()    
        #self.drawNodes()
        #self.drawLabels()
        self.drawMenu ()
        self.drawCords ()                   
        pygame.display.flip()
  
    def drawCords(self):
        for i in range(0, self.nodLen, 1):
            message = "Node:%i [%.2f,%.2f,%.2f]" % (i, self.nodes[i][0],self.nodes[i][1],self.nodes[i][2])
            self.drawLabel ([5,30*i+10],message ,22)
        
    def drawMenu (self):
        for i in range(0, self.optionsLen, 1):    
            top = self.menuTop+(self.optionHeight+self.optionSpacer)*i
            pygame.draw.rect(self.screen, self.optionColour, [self.menuLeft, top, self.optionWidth, self.optionHeight])
            self.drawLabel ([self.menuLeft+5,top+10],self.options[i]['label'],28)

    def drawSurfaces (self):
        for i in range(0, self.surfaceLen, 1):   
            self.drawFace(
            [
            self.surfaces[i][0],
            self.surfaces[i][1],
            self.surfaces[i][2],
            self.surfaces[i][3]
            ],
            (0,0,20)
            )
              
    def drawFaces(self):
        surfaceTotals ={}
        print ("\n")
        for i in range(0, self.surfaceLen, 1):
            surfaceTotals[i]= self.sumNodes (i)  
            print (surfaceTotals[i])
        surfaceTotals ={k:v for k, v in sorted(surfaceTotals.items(),key=lambda item:item[1])} 
        i=0           
        for key, value in surfaceTotals.items():
            i=i+1
            if (i>3):
                self.drawFace(
                [
                self.surfaces[key][0],
                self.surfaces[key][1],
                self.surfaces[key][2],
                self.surfaces[key][3]
                ],
                self.surfaces[key][4])
            
    def sumNodes (self, surface):
        total = 0
        tmp =[]
        for i in range(0, 4, 1):
            #print  (self.nodes[self.surfaces[surface][i]][2])
            tmp.append(self.nodes[self.surfaces[surface][i]][2])
        return min(tmp)
        
    def drawFace(self,nodes,colour):
        pygame.draw.polygon(self.screen, colour, [
        [self.nodes[nodes[0]][0]+self.centreX,self.nodes[nodes[0]][1]+self.centreY], 
        [self.nodes[nodes[1]][0]+self.centreX,self.nodes[nodes[1]][1]+self.centreY],
        [self.nodes[nodes[2]][0]+self.centreX,self.nodes[nodes[2]][1]+self.centreY],
        [self.nodes[nodes[3]][0]+self.centreX,self.nodes[nodes[3]][1]+self.centreY]
        ])        
        
    def drawEdges(self):
        for i in range(0, self.edgeLen, 1):
            n0 = self.edges[i][0]
            n1 = self.edges[i][1]
            node0 = self.nodes[n0]
            node1 = self.nodes[n1]
            pygame.draw.lines(
            self.screen, 
            self.edgeColour, 
            False,
            [
            [node0[0]+self.centreX,node0[1]+self.centreY],
            [node1[0]+self.centreX,node1[1]+self.centreY]
            ],
            1
            ) 

    def drawNodes(self):
        for i in range(0, self.nodLen, 1):
            x =self.nodes[i][0]+self.centreX
            y = self.nodes[i][1]+self.centreY
            pygame.draw.circle(self.screen,self.nodeColour, [x, y], self.nodeSize)
            
    def drawLabels(self):
        for i in range(0, self.nodLen, 1):
            x =self.nodes[i][0]+self.centreX
            y = self.nodes[i][1]+self.centreY
            label = "Node: %d" % i
            self.drawLabel([x+5,y-5],label,28)
            
    def drawLabel (self,cords,message,fontsize):
        font = pygame.font.SysFont(None, fontsize)
        text = font.render(message, True, self.labelColour)
        
        #textRect.center = (cords[0], cords[1])
        self.screen.blit(text,(cords[0], cords[1]))
                        
if __name__ == "__main__":
    tmp =  cube()

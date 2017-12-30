# Tran, Thang
# 1001-233-804
# 2017-08-31
# Assignment_00_03

import numpy as np

class cl_world:
    def __init__(self, objects=[], canvases=[]):
        self.objects = objects
        self.canvases = canvases
        # self.display

    def add_canvas(self, canvas):
        self.canvases.append(canvas)
        canvas.world = self

    def create_graphic_objects(self, canvas):
        self.objects.append(canvas.create_line(0, 0, canvas.cget("width"), canvas.cget("height")))
        self.objects.append(canvas.create_line(canvas.cget("width"), 0, 0, canvas.cget("height")))
        self.objects.append(canvas.create_oval(int(0.25 * int(canvas.cget("width"))),
                                               int(0.25 * int(canvas.cget("height"))),
                                               int(0.75 * int(canvas.cget("width"))),
                                               int(0.75 * int(canvas.cget("height")))))

    def redisplay(self, canvas, event):
        if self.objects:
            canvas.coords(self.objects[0], 0, 0, event.width, event.height)
            canvas.coords(self.objects[1], event.width, 0, 0, event.height)
            canvas.coords(self.objects[2], int(0.25 * int(event.width)),
                          int(0.25 * int(event.height)),
                          int(0.75 * int(event.width)),
                          int(0.75 * int(event.height)))
    
    def drawObject(filename):
      arrayVertex = np.array([[0,0]],dtype=float)
      arrayTriangle = []
      arrayWindow = []
      arrayView = []
      file = open(filename, "r")
      for line in file:
          firstList = line.split()
          if firstList[0] == "v":
        #print (firstList[1],firstList[2])
              temp_array = np.array([[firstList[1], firstList[2]]],dtype=float)
        #print (temp_array)
              arrayVertex = np.concatenate((arrayVertex, temp_array))
          if firstList[0] == "f":
        #print (firstList)
        #print (len(firstList))
              temp_F = []
              for i in range (1,len(firstList)):
                  temp_F.append(firstList[i])
                  arrayTriangle.append(temp_F)
          if firstList[0] == "w":
              for i in range(1, len(firstList)):
                  arrayWindow.append(firstList[i])
          if firstList[0] == "s":
              for i in range(1, len(firstList)):
                  arrayView.append(firstList[i])

      print(arrayVertex)
      print(arrayTriangle)
      print(arrayWindow)
      print(arrayView)

    
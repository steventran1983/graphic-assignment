import numpy as np
from math import *
from numpy import *

class cl_world:
    def __init__(self, objects=[], canvases=[], screen_width=0, screen_height=0):
        self.objects = objects
        self.canvases = canvases
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.vertex_global_array = []
        self.global_triangle = []
        self.global_window = []
        self.global_view = []
        # self.display

    def add_canvas(self, canvas):
        self.canvases.append(canvas)
        canvas.world = self

    # Method : create_graphic_object()
    # parameter: elf, canvas, filename
    # Description: Read content from text file
    def create_graphic_objects(self, canvas, filename):
        canvas.delete("all")
        self.objects = []
        self.vertex_global_array = [[0, 0, 0]]
        self.global_triangle = []
        self.global_window = []
        self.global_view = []
        array_triangle = []
        array_view = []
        array_window = []
        array_vertex = np.array([[0, 0, 0]], dtype=float)
        file = open(filename, "r")
        for line in file:
            if len(line.strip()) == 0:
                break
            else:
                first_list = line.split()
                if first_list[0] == "v":
                    temp_array = np.array([[first_list[1], first_list[2], first_list[3]]], dtype=float)
                    temp_array_global = [first_list[1], first_list[2], first_list[3]]
                    array_vertex = np.concatenate((array_vertex, temp_array))
                    self.vertex_global_array.append(temp_array_global)
                if first_list[0] == "f":
                    temp_f = []
                    for i in range(1, len(first_list)):
                        temp_f.append(first_list[i])
                        array_triangle.append(temp_f)
                        self.global_triangle.append(temp_f)
                if first_list[0] == "w":
                    for i in range(1, len(first_list)):
                        array_window.append(first_list[i])
                        self.global_window.append(first_list[i])
                if first_list[0] == "s":
                    for i in range(1, len(first_list)):
                        array_view.append(first_list[i])
                        self.global_view.append(first_list[i])
        xwmin = float(array_window[0])
        xwmax = float(array_window[2])
        ywmin = float(array_window[1])
        ywmax = float(array_window[3])
        # Define normalized viewport coordinates
        nxvmin = float(array_view[0])
        nxvmax = float(array_view[2])
        nyvmin = float(array_view[1])
        nyvmax = float(array_view[3])
        # Find actual viewport coordinates
        self.screen_width = int(canvas.cget("width"))
        self.screen_height = int(canvas.cget("height"))
        xvmin = int(nxvmin * self.screen_width)
        xvmax = int(nxvmax * self.screen_width)
        yvmin = int(nyvmin * self.screen_height)
        yvmax = int(nyvmax * self.screen_height)
        sx = (xvmax - xvmin) / (xwmax - xwmin)
        sy = (yvmax - yvmin) / (ywmax - ywmin)
        self.objects.append(canvas.create_rectangle(xvmin, yvmin, xvmax, yvmax, outline='black'))
        for i in range(0, len(array_triangle)):
            list_drawing = []
            for j in range(0, len(array_triangle[i])):
                temp_index = int(array_triangle[i][j])
                psx = xvmin + int(sx * (float(array_vertex[temp_index][0]) - xwmin))
                psy = yvmin + int(sy * (ywmax - float(array_vertex[temp_index][1])))
                list_drawing.append(psx)
                list_drawing.append(psy)
            if i % 2 == 0:
                self.objects.append(canvas.create_polygon(list_drawing, outline='black', fill='red', width=1))
            else:
                self.objects.append(canvas.create_polygon(list_drawing, outline='black', fill='blue', width=1))

    # Method : redisplay()
    # parameter: self,canvas,event
    # Description: Scale all point of object into new canvas
    def redisplay(self, canvas, event):
        if self.objects:
            # ratio between previous canvas and current canvas
            ratio_width = float(event.width / self.screen_width)
            ratio_height = float(event.height / self.screen_height)
            # Loop through all Object
            for i in range(0, len(self.objects)):
                temp = canvas.coords(self.objects[i])
                # for the viewpoint
                if i == 0:
                    canvas.coords(self.objects[i], (temp[0] * ratio_width), (temp[1] * ratio_height),
                                  (temp[2] * ratio_width), (temp[3] * ratio_height))
                # for 3 vertexes of polygon object
                else:
                    canvas.coords(self.objects[i], (temp[0] * ratio_width), (temp[1] * ratio_height),
                                  (temp[2] * ratio_width), (temp[3] * ratio_height),
                                  (temp[4] * ratio_width), (temp[5] * ratio_height))
            self.screen_width = event.width
            self.screen_height = event.height

    def translate(self, canvas, numpy_input, step):
        input_step_array = numpy_input/step
        for i in range(0,step):
            self.translate_method(canvas, input_step_array)
            canvas.update()

    def translate_method(self, canvas, numpy_input):
        # Measure increament
        x_axis_increa = numpy_input[0]
        y_axis_increa = numpy_input[1]
        xwmin = float(self.global_window[0])
        xwmax = float(self.global_window[2])
        ywmin = float(self.global_window[1])
        ywmax = float(self.global_window[3])
        # Define normalized viewport coordinates
        nxvmin = float(self.global_view[0])
        nxvmax = float(self.global_view[2])
        nyvmin = float(self.global_view[1])
        nyvmax = float(self.global_view[3])
        # Find actual viewport coordinates
        self.screen_width = int(canvas.cget("width"))
        self.screen_height = int(canvas.cget("height"))
        xvmin = int(nxvmin * self.screen_width)
        xvmax = int(nxvmax * self.screen_width)
        yvmin = int(nyvmin * self.screen_height)
        yvmax = int(nyvmax * self.screen_height)
        sx = (xvmax - xvmin) / (xwmax - xwmin)
        sy = (yvmax - yvmin) / (ywmax - ywmin)

        for i in range(0, len(self.global_triangle)):
            list_drawing = []
            for j in range(0, len(self.global_triangle[i])):
                temp_index = int(self.global_triangle[i][j])
                x = float(self.vertex_global_array[temp_index][0]) + x_axis_increa
                y = float(self.vertex_global_array[temp_index][1]) + y_axis_increa
                psx = xvmin + int(sx * (x - xwmin))
                psy = yvmin + int(sy * (ywmax - y))
                list_drawing.append(psx)
                list_drawing.append(psy)
            canvas.coords(self.objects[i+1], list_drawing[0],list_drawing[1],list_drawing[2],list_drawing[3],
                          list_drawing[4],list_drawing[5])

        for i in range(1, len(self.vertex_global_array)):
            self.vertex_global_array[i][0] = float(self.vertex_global_array[i][0]) + float(numpy_input[0])
            self.vertex_global_array[i][1] = float(self.vertex_global_array[i][1]) + float(numpy_input[1])
            self.vertex_global_array[i][2] = float(self.vertex_global_array[i][2]) + float(numpy_input[2])
            # print("thang",self.vertex_global_array)

    def scale(self, canvas, point, step, scale_ratio):
        temp_scale_ratio = scale_ratio/step
        for i in range(0,step):
            self.scale_method(canvas, point, temp_scale_ratio)
            canvas.update()
            time.sleep(0.1)

    def scale_method(self, canvas,  point, scale_ratio):
        # Measure increament
        # increament = float(scale_ratio) / step
        xwmin = float(self.global_window[0])
        xwmax = float(self.global_window[2])
        ywmin = float(self.global_window[1])
        ywmax = float(self.global_window[3])
        # Define normalized viewport coordinates
        nxvmin = float(self.global_view[0])
        nxvmax = float(self.global_view[2])
        nyvmin = float(self.global_view[1])
        nyvmax = float(self.global_view[3])
        # Find actual viewport coordinates
        self.screen_width = int(canvas.cget("width"))
        self.screen_height = int(canvas.cget("height"))
        xvmin = int(nxvmin * self.screen_width)
        xvmax = int(nxvmax * self.screen_width)
        yvmin = int(nyvmin * self.screen_height)
        yvmax = int(nyvmax * self.screen_height)
        sx = (xvmax - xvmin) / (xwmax - xwmin)
        sy = (yvmax - yvmin) / (ywmax - ywmin)
        translate_matrix = array([[1, 0, -point[0]], [0, 1, -point[1]], [0, 0, 1]], dtype= float)
        translate_matrix_xyz = array([[1, 0, 0, -point[0]], [0, 1, 0, -point[1]],[0, 0, 1, -point[2]], [0, 0,0, 1]], dtype= float)

        translate_reverse = array([[1, 0, -point[0]], [0, 1, -point[1]], [0, 0, 1]], dtype=float)
        translate_reverse_xyz = array([[1, 0, 0, point[0]], [0, 1, 0, point[1]],[0, 0, 1, point[2]], [0, 0,0, 1]], dtype= float)

        scale_ratio_matrix = array([[scale_ratio[0], 0, 0], [0, scale_ratio[1], 0], [0, 0, 1]])
        scale_ratio_matrix_xyz = array([[scale_ratio[0], 0, 0,0], [0, scale_ratio[1], 0,0], [0, 0,scale_ratio[2], 0], [0,0, 0, 1]])
        for i in range(0, len(self.global_triangle)):
            list_drawing = []
            for j in range(0, len(self.global_triangle[i])):
                temp_index = int(self.global_triangle[i][j])
                temp_array = array([[self.vertex_global_array[temp_index][0]], [self.vertex_global_array[temp_index][1]],[1]], dtype= float)
                print("temp_array",temp_array)
                temp_points = translate_matrix.dot(temp_array)
                print("temp_point",temp_points)
                temp_scale = scale_ratio_matrix.dot(temp_points)
                print("temp_scale",temp_scale)
                final_point = translate_reverse.dot(temp_scale)
                print("final",final_point)
                psx = xvmin + int(sx * (float(final_point[0][0]) - xwmin))
                psy = yvmin + int(sy * (ywmax - float(final_point[1][0])))
                print("psx",psx)
                print("psy", psy)
                list_drawing.append(psx)
                list_drawing.append(psy)
            canvas.coords(self.objects[i + 1], list_drawing[0], list_drawing[1], list_drawing[2], list_drawing[3],
                          list_drawing[4], list_drawing[5])

        for i in range(1, len(self.vertex_global_array)):
            vertex_current_array = array([[self.vertex_global_array[i][0]],[self.vertex_global_array[i][1]],
                                         [self.vertex_global_array[i][2]],[1]],dtype =float)
            vertex_translate = translate_matrix_xyz.dot(vertex_current_array)
            vertex_scale = scale_ratio_matrix_xyz.dot(vertex_translate)
            vertex_final = translate_reverse_xyz.dot(vertex_scale)
            self.vertex_global_array[i][0] = vertex_final[0][0]
            self.vertex_global_array[i][1] = vertex_final[1][0]
            self.vertex_global_array[i][2] = vertex_final[2][0]

    def rotation(self, canvas, A, B, step, degree):
        degree_step = float(degree/step)
        for i in range(0, step):
            self.rotation_method(canvas, A, B, degree_step)
            canvas.update()

    def rotation_method(self,canvas, A, B, degree):
        # Translation Matrix
        T = array([[1, 0, 0, -A[0]], [0, 1, 0, -A[1]], [0, 0, 1, -A[2]], [0, 0, 0, 1]])
        Ap = T.dot(A)
        Bp = T.dot(B)
        # Matrix for rotation around x
        sq = sqrt(Bp[1]**2 + Bp[2]**2)
        if sq > 0:
            Rx = array([[1, 0, 0, 0], [0, Bp[2] / sq, -Bp[1] / sq, 0], [0, Bp[1] / sq, Bp[2] / sq, 0], [0, 0, 0, 1]])
        else:
            Rx = array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        Bpp = Rx.dot(Bp)
        # Matrix for rotation around y
        sq = sqrt(Bpp[0] ** 2 + Bpp[2] ** 2)
        if sq > 0:
            Ry = array([[Bpp[2][0] / sq, 0, -Bpp[0][0] / sq, 0], [0, 1, 0, 0], [Bpp[0][0] / sq, 0, Bpp[2][0] / sq, 0],
                        [0, 0, 0, 1]])
        else:
            Ry = array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        Bppp = Ry.dot(Bpp)
        # Convert degrees to radians
        theta = pi * degree / 180.0
        # Matrix for rotation around z
        Rz = array([[cos(theta), -sin(theta), 0, 0], [sin(theta), cos(theta), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        # Composite matrix
        # Note: The inverse of a rotation matrix around an axis is equal to the transpose of that matrix.
        # This property is not valid for the translation matrix
        Rx_inv = Rx.transpose()
        Ry_inv = Ry.transpose()
        T_inv = array([[1, 0, 0, float(A[0])], [0, 1, 0, float(A[1])], [0, 0, 1, float(A[2])], [0, 0, 0, 1]])
        C = T_inv.dot(Rx_inv.dot(Ry_inv.dot(Rz.dot(Ry.dot(Rx.dot(T))))))

        xwmin = float(self.global_window[0])
        xwmax = float(self.global_window[2])
        ywmin = float(self.global_window[1])
        ywmax = float(self.global_window[3])
        # Define normalized viewport coordinates
        nxvmin = float(self.global_view[0])
        nxvmax = float(self.global_view[2])
        nyvmin = float(self.global_view[1])
        nyvmax = float(self.global_view[3])
        # Find actual viewport coordinates
        self.screen_width = int(canvas.cget("width"))
        self.screen_height = int(canvas.cget("height"))
        xvmin = int(nxvmin * self.screen_width)
        xvmax = int(nxvmax * self.screen_width)
        yvmin = int(nyvmin * self.screen_height)
        yvmax = int(nyvmax * self.screen_height)
        sx = (xvmax - xvmin) / (xwmax - xwmin)
        sy = (yvmax - yvmin) / (ywmax - ywmin)
        if self.objects:
            for j in range(1,len(self.vertex_global_array)):
                point = array([self.vertex_global_array[j][0], self.vertex_global_array[j][1],
                               self.vertex_global_array[j][2], 1], dtype=float)
                point_rotation = C.dot(point)
                self.vertex_global_array[j][0] = point_rotation[0][0]
                self.vertex_global_array[j][1] = point_rotation[1][0]
                self.vertex_global_array[j][2] = point_rotation[2][0]
            for i in range(0, len(self.global_triangle)):
                list_drawing = []
                for j in range(0, len(self.global_triangle[i])):
                    temp_index = int(self.global_triangle[i][j])
                    psx = xvmin + int(sx * (self.vertex_global_array[temp_index][0] - xwmin))
                    psy = yvmin + int(sy * (ywmax - self.vertex_global_array[temp_index][1]))
                    list_drawing.append(psx)
                    list_drawing.append(psy)
                canvas.coords(self.objects[i + 1], list_drawing[0], list_drawing[1], list_drawing[2], list_drawing[3],
                              list_drawing[4], list_drawing[5])


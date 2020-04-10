import cv2
import os
import PIL


def find_boxes(filepath):
    cwd = os.path.abspath(os.getcwd())
    image = PIL.Image.open(filepath, 'r').convert('1')
    width, height = image.size
    
    #vert_line = PIL.Image.new('1', (1, height)
    #vert_line = vert_line.save(cwd+'/gvis/images/vertical.bmp')
    vline = cv2.imread(cwd+'/images/comp/vertical.bmp')
    #hor_line = PIL.Image.new('1', (width, 1))
    #hor_line = hor_line.save(cwd+'/gvis/images/horizontal.bmp')
    hline = cv2.imread(cwd+'/images/comp/horizontal.bmp')
    
    x_points = list()
    y_points = list()

    for x in range(0, width, 1):
        crop_rect = (x, 0, x+1, height)
        img_vl = image.crop(crop_rect)
        img_vl = img_vl.save(cwd+'/tmp/img_vl.bmp')
        i_line = cv2.imread(cwd+'/tmp/img_vl.bmp')
        diff = cv2.subtract(i_line, vline)
        b, g, r = cv2.split(diff)
        if(cv2.countNonZero(b) < 300):
            x_points.append(x)
    
    for y in range(0, height, 1):
        crop_rect = (0, y, width, y+1)
        img_vl = image.crop(crop_rect)
        img_vl = img_vl.save(cwd+'/tmp/img_hz.bmp')
        i_line = cv2.imread(cwd+'/tmp/img_hz.bmp')
        diff = cv2.subtract(i_line, hline)
        b, g, r = cv2.split(diff)
        if(y < 1500):
            if(cv2.countNonZero(b) < 200):
                y_points.append(y)
        else:
            if(cv2.countNonZero(b) < 500):
                y_points.append(y)

    #print(y_points)
    boxes = list()
        
    for j in range(len(y_points)-1):
        for i in range(len(x_points)-1):
            if(x_points[i+1] - x_points[i] > 5 and y_points[j+1] - y_points[j] > 5):
                box = list()
                box.extend((x_points[i], y_points[j], x_points[i+1], y_points[j+1]))
                boxes.append(box)
        
    #for box in boxes:
    #    print('{}, {}, {}, {}'.format(box[0], box[1], box[2], box[3]))
    
    return boxes	

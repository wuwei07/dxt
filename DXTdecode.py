import numpy as np
from PIL import Image

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

width, height = 1920, 1080
BSIZE_x, BSIZE_y = 4, 4
img = Image.new('RGB', (width, height))
img2 = np.array(img.convert("RGB"))
f =  open('D:/dxt1c_rtl_output0.hex', 'r')

if width < height:
    height, width = width, height;

# with open('D:/A.txt', 'r') as f:
    # while f.readable:
for y in my_range(0, height-1, BSIZE_y):
    for x in my_range(0, width-1, BSIZE_x):
        
        block = img2[y:y + BSIZE_y, x:x + BSIZE_x]
        
        hex_str = f.readline()
        if hex_str == 'xxxx':
            break
        # hex_str = f.read(4)
        maxcolor = int(hex_str, 16)
        maxcolor = '{:016b}'.format(maxcolor)
        colorarray1 = np.array((maxcolor[0:5], maxcolor[5:11], maxcolor[11:16]))
        colorstring = colorarray1[0]+ colorarray1[0][2:5] + colorarray1[1] + colorarray1[1][4:6] + colorarray1[2] + colorarray1[2][2:5]
        color0 = [int(colorstring[i:i+8], 2) for i in range(0, len(colorstring), 8)]   
        
        hex_str = f.readline()
        # hex_str = f.read(4)
        mincolor = int(hex_str, 16)
        mincolor = '{:016b}'.format(mincolor)
        colorarray2 = np.array((mincolor[0:5], mincolor[5:11], mincolor[11:16]))
        colorstring = colorarray2[0] + colorarray2[0][2:5] + colorarray2[1] + colorarray2[1][4:6] + colorarray2[2] + colorarray2[2][2:5]
        color1 = [int(colorstring[i:i+8], 2) for i in range(0, len(colorstring), 8)]
        
        # color0 = list(map(float, color0))
        # color1 = list(map(float, color1))
        color2 = np.add(list(map(lambda x: x * 2/3, color0)) , list(map(lambda x: x * 1/3, color1)))
        color3 = np.add(list(map(lambda x: x * 1/3, color0)) , list(map(lambda x: x * 2/3, color1)))
#      
     #--readline   
        hex_str = f.readline()
        hex_int = int(hex_str, 16)
        row = '{:016b}'.format(hex_int)
        row1 = row[0:8]
        row0 = row[8:16]
    
        hex_str = f.readline()
        hex_int = int(hex_str, 16)
        row = '{:016b}'.format(hex_int)
        row3 = row[0:8]
        row2 = row[8:16]
        
    #no line
        # hex_str = f.read(2)
        # hex_int = int(hex_str, 16)
        # row1 = '{:08b}'.format(hex_int)
        # hex_str = f.read(2)
        # hex_int = int(hex_str, 16)
        # row0 = '{:08b}'.format(hex_int)
        # hex_str = f.read(2)
        # hex_int = int(hex_str, 16)
        # row3 = '{:08b}'.format(hex_int)
        # hex_str = f.read(2)
        # hex_int = int(hex_str, 16)
        # row2 = '{:08b}'.format(hex_int)
        
        #reconstruct index matrix
        w, h = 4, 4;
        matrix = [[0 for x in range(w)] for y in range(h)]
        
        for i in range(w):
            matrix[0][i] = row0[0 + i*2: 2 + i*2]
        
        for i in range(w):
            matrix[1][i] = row1[0 + i*2: 2 + i*2]
            
        for i in range(w):
            matrix[2][i] = row2[0 + i*2: 2 + i*2]
            
        for i in range(w):
            matrix[3][i] = row3[0 + i*2: 2 + i*2]
        # print(matrix)
        
        #reconstruct color block
        for i in range(h):
            for j in range(w):
                if matrix[i][j] == '00':
                    block[i][j] = color0
                elif matrix[i][j] == '01':
                    block[i][j] = color1
                elif matrix[i][j] == '10':
                    block[i][j] = color2
                else:
                    block[i][j] = color3
                    
        img2[y:y + BSIZE_y, x:x + BSIZE_x] = block;
        
img = Image.fromarray(img2)
img.save('D:/test.png')        
f.close
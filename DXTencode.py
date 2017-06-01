from PIL import Image
import numpy as np
import sys

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step
    
def to565(color):    
    return ((color[0] >> 3) << 11) | ((color[1] >> 2 ) << 5) | (color[2] >> 3);

def BTC(IMG, BSIZE_x, BSIZE_y):
    (height, width) = IMG.size;
    IMG2 = np.array(IMG.convert("RGB"));
    # IMG2 = np.array(IMG);
    r, g, b = IMG.convert("RGB").split();
    r_array = np.array(r, int);
    g_array = np.array(g, int);
    b_array = np.array(b, int);
    pnum = BSIZE_x * BSIZE_y;
    f = open('D:/hexFile.txt', 'w')
    
    if width < height:
        height, width = width, height;
    
    for y in my_range(0, height-1, BSIZE_y):
        for x in my_range(0, width-1, BSIZE_x):
            
            R = r_array[y:y + BSIZE_y, x:x + BSIZE_x];
            G = g_array[y:y + BSIZE_y, x:x + BSIZE_x];
            B = b_array[y:y + BSIZE_y, x:x + BSIZE_x];
            block = IMG2[y:y + BSIZE_y, x:x + BSIZE_x];
            
    #---Finding a Line Through Color Space---#
            # --based on the euclidean distance--
            # minC = sys.maxsize;
            # maxC = -1;
            # maxdist = -1;
            # a = [];
            # for i in my_range(0, 3, 1):
            #     for j in my_range(0, 3, 1):
            #         a.append(block[i, j]); 
            #         
            # for i in my_range(0, 15, 1):
            #     for j in my_range(i + 1, 15, 1):
            #         dist = ColorDistance(a[i], a[j]);
            #         if dist > maxdist:
            #             minC = a[i];
            #             maxC = a[j];
            #             maxdist = dist;
      
        #--based on the luminance--
            # Y = (R + G*2 + B);
            # 
            # maxL = -1;
            # minL =  sys.maxsize;
            # it = np.nditer(Y, flags=['multi_index']);
            # while not it.finished:
            #     if it[0] > maxL:
            #         maxL = it[0];
            #         maxC = block[it.multi_index];
            #         
            #     if it[0] < minL:
            #         minL = it[0];
            #         minC = block[it.multi_index];
            #         
            #     it.iternext();
    
        #--base on extents of the bounding box
            maxR = 0;
            minR = 255;
            maxG = 0;
            minG = 255;
            maxB = 0;
            minB = 255;
            
            bound_x, bound_y = R.shape;
      
            for i in my_range(0, bound_x - 1, 1):
                for j in my_range(0, bound_y - 1, 1):
                    if R[i][j] <= minR:
                        minR = R[i][j];
                    if R[i][j] > maxR:
                        maxR = R[i][j];
                        
                    if G[i][j] <= minG:
                        minG = G[i][j];
                    if G[i][j] > maxG:
                        maxG = G[i][j];
                        
                    if B[i][j] <= minB:
                        minB = B[i][j];
                    if B[i][j] > maxB:
                        maxB = B[i][j];
                        
            insetR = (maxR - minR)>>4;
            insetG = (maxG - minG)>>4;
            insetB = (maxB - minB)>>4;
            
            if (minR + insetR) <= 255:
                minR = minR + insetR;
            else:
                minR = 255;
            if (minG + insetG) <= 255:
                minG = minG + insetG;
            else:
                minG = 255;
            if (minB + insetB) <= 255:
                minB = minB + insetB;
            else:
                minB = 255;
            
            if maxR >= insetR:
                maxR = maxR - insetR;
            else:
                maxR =  0;
            if maxG >= insetG:
                maxG = maxG - insetG;
            else:
                maxG =  0;
            if maxB >= insetB:
                maxB = maxB - insetB;
            else:
                maxB =  0;
                        
            minC = np.array((minR, minG, minB));
            maxC = np.array((maxR, maxG, maxB));
            
        #--decode
            if to565(maxC) < to565(minC):
                 maxC, minC = minC, maxC;
            
            c0 = maxC;
            c1 = minC;
            c2 = (2*c0 + 1*c1) / 3;
            c3 = (1*c0 + 2*c1) / 3;
            c_array = np.array((c0, c1, c2, c3));

            w, h = 4, 4;
            index_table = [[0 for x in range(w)] for y in range(h)]
    #---Finding Matching Points On The Line Through Color Space---#
            for i in range(4):
                for j in range(4):
                    cb0 = block[i, j][0]
                    cb1 = block[i, j][1]
                    cb2 = block[i, j][2]
                    
                    d0 = abs(c0[0] - cb0) + abs(c0[1] - cb1) + abs(c0[2] - cb2)
                    d1 = abs(c1[0] - cb0) + abs(c1[1] - cb1) + abs(c1[2] - cb2)
                    d2 = abs(c2[0] - cb0) + abs(c2[1] - cb1) + abs(c2[2] - cb2)
                    d3 = abs(c3[0] - cb0) + abs(c3[1] - cb1) + abs(c3[2] - cb2)
                    
                    b0 = d0 > d3
                    b1 = d1 > d2
                    b2 = d0 > d2
                    b3 = d1 > d3
                    b4 = d2 > d3
                    
                    x0 = b1 & b2
                    x1 = b0 & b3
                    x2 = b0 & b4
                    
                    result = x2 | ((x0 | x1) << 1)
                    if result == 0:
                        block[i, j] = c0
                    elif result == 1:
                        block[i, j] = c1
                    elif result == 2:
                        block[i, j] = c2
                    else:
                        block[i, j] = c3
                    index_table[i][j] = '{0:02b}'.format(result)
                            
            IMG2[y:y + BSIZE_y, x:x + BSIZE_x] = block;
                        
            row0 = index_table[0][0] + index_table[0][1] + index_table[0][2] + index_table[0][3]
            row1 = index_table[1][0] + index_table[1][1] + index_table[1][2] + index_table[1][3]
            row2 = index_table[2][0] + index_table[2][1] + index_table[2][2] + index_table[2][3]
            row3 = index_table[3][0] + index_table[3][1] + index_table[3][2] + index_table[3][3]
            
            min565 = to565(minC)
            max565 = to565(maxC)
            # with open('D:/hexFile.txt', 'w') as f:
            f.write('{:04x}'.format(max565))
            f.write('{:04x}'.format(min565))
            f.write('{:02x}'.format(int(row1, 2))) #row1
            f.write('{:02x}'.format(int(row0, 2))) #row0
            f.write('{:02x}'.format(int(row3, 2))) #row3
            f.write('{:02x}'.format(int(row2, 2))) #row2
                    
    # img = Image.merge('RGB', (r, g, b));
    img = Image.fromarray(IMG2);
    img.save("D:/mutest_L.bmp");
    img.close;
    f.close
    
im = Image.open("D:/mu.bmp");
BTC(im, 4, 4);
im.close;

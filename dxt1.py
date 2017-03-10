from PIL import Image
import numpy as np

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step
        
def ColorDistance(c1, c2):
    return ((c1[0] - c2[0]) * (c1[0] - c2[0])) + ((c1[1] - c2[1]) * (c1[1] - c2[1])) + ((c1[2] - c2[2]) * (c1[2] - c2[2]));
    
def to565(color):    
    return ((color[0] >> 3) << 11) | ((color[1] >> 2 ) << 5) | (color[2] >> 3);

def BTC(IMG, BSIZE_x, BSIZE_y):
    (height, width) = IMG.size;
    IMG2 = np.array(IMG.convert("RGB"));
    # IMG2 = np.array(IMG);
    r, g, b = IMG.convert("RGB").split();
    r_array = np.array(r);
    g_array = np.array(g);
    b_array = np.array(b);
    pnum = BSIZE_x * BSIZE_y;
    
    # if width < height:
    #     height, width = width, height;
    
    for y in my_range(0, height-1, BSIZE_y):
        for x in my_range(0, width-1, BSIZE_x):
            
            R = r_array[y:y + BSIZE_y, x:x + BSIZE_x];
            G = g_array[y:y + BSIZE_y, x:x + BSIZE_x];
            B = b_array[y:y + BSIZE_y, x:x + BSIZE_x];
            
            block = IMG2[y:y + BSIZE_y, x:x + BSIZE_x];
            
            R_d = R/10;
            G_d = G/10;
            B_d = B/10;
            
    #---Finding a Line Through Color Space---#
            
        # --based on the euclidean distance--
            # minC = 1024;
            # maxC = -1;
            # maxdist = -1;
            # a = [];
            # for i in my_range(0, 3, 1):
            #     for j in my_range(0, 3, 1):
            #         a.append(block[i, j]); 
            #         
            # for i in my_range(0, 15, 1):
            #     for j in my_range(i, 15, 1):
            #         dist = ColorDistance(a[i], a[j]);
            #         if dist > maxdist:
            #             minC = a[i];
            #             maxC = a[j];
            #             maxdist = dist;
                    
        #--based on the luminance--
            Y = (R_d + G_d*2 + B_d)*10;
            
            maxL = -1;
            minL =  2048;
            it = np.nditer(Y, flags=['multi_index']);
            while not it.finished:
                if it[0] > maxL:
                    maxL = it[0];
                    maxC = block[it.multi_index];
                    
                if it[0] < minL:
                    minL = it[0];
                    minC = block[it.multi_index];
                    
                it.iternext();
            
        #--base on extents of the bounding box
            # maxR = 0;
            # minR = 255;
            # maxG = 0;
            # minG = 255;
            # maxB = 0;
            # minB = 255;
            
            bound_x, bound_y = R.shape;
            
            
            # for i in my_range(0, bound_x - 1, 1):
            #     for j in my_range(0, bound_y - 1, 1):
            #         if R[i][j] <= minR:
            #             minR = R[i][j];
            #         if R[i][j] > maxR:
            #             maxR = R[i][j];
            #             
            #         if G[i][j] <= minG:
            #             minG = G[i][j];
            #         if G[i][j] > maxG:
            #             maxG = G[i][j];
            #             
            #         if B[i][j] <= minB:
            #             minB = B[i][j];
            #         if B[i][j] > maxB:
            #             maxB = B[i][j];
            #             
            # insetR = (maxR - minR)>>4;
            # insetG = (maxG - minG)>>4;
            # insetB = (maxB - minB)>>4;
            # 
            # if (minR + insetR) <= 255:
            #     minR = minR + insetR;
            # else:
            #     minR = 255;
            # if (minG + insetG) <= 255:
            #     minG = minG + insetG;
            # else:
            #     minG = 255;
            # if (minB + insetB) <= 255:
            #     minB = minB + insetB;
            # else:
            #     minB = 255;
            # 
            # if maxR >= insetR:
            #     maxR = maxR - insetR;
            # else:
            #     maxR =  0;
            # if maxG >= insetG:
            #     maxG = maxG - insetG;
            # else:
            #     maxG =  0;
            # if maxB >= insetB:
            #     maxB = maxB - insetB;
            # else:
            #     maxB =  0;
            #             
            # minC = np.array((minR, minG, minB));
            # maxC = np.array((maxR, maxG, maxB));
            
        #--decode
            if to565(maxC) < to565(minC):
                maxC, minC = minC, maxC;
            
            c0 = minC/10;
            c1 = maxC/10;
            c2 = (2*c0 + 1*c1) / 3;
            c3 = (1*c0 + 2*c1) / 3;
            c_array = np.array((c0*10, c1*10, c2*10, c3*10));
            
            
    #---Finding Matching Points On The Line Through Color Space---#
            for i in my_range(0, bound_x - 1, 1):
                for j in my_range(0, bound_y - 1, 1):
                    mindist = 255;
                    for z in range(0, 3, 1):
                        dist = ColorDistance(c_array[z], block[i, j]);
                        if dist < mindist:
                            mindist = dist;
                            block[i, j] = c_array[z];
                            
            IMG2[y:y + BSIZE_y, x:x + BSIZE_x] = block;
                    
    # img = Image.merge('RGB', (r, g, b));
    img = Image.fromarray(IMG2);
    img.save("D:/len.png");
    img.close;

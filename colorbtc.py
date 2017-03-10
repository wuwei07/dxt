from numpy import *
import numpy as np

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

def BTC(IMG, BSIZE_x, BSIZE_y):
    (height, width) = IMG.size;
    # IMG2 = np.array(IMG.convert("RGB"));
    r, g, b = IMG.convert("RGB").split();
    r_array = np.array(r);
    g_array = np.array(g);
    b_array = np.array(b);
    pnum = BSIZE_x * BSIZE_y;
    
    if width < height:
        height, width = width, height;
    
    #encode
    for y in my_range(0, height-1, BSIZE_y):
        for x in my_range(0, width-1, BSIZE_x):
            
            #計算luminance bit-map
            R = r_array[y:y + BSIZE_y, x:x + BSIZE_x];
            G = g_array[y:y + BSIZE_y, x:x + BSIZE_x];
            B = b_array[y:y + BSIZE_y, x:x + BSIZE_x];
            # v = np.array([1, 2, 1]);
            Y = 299/1000*R + 587/1000*G + 114/1000*B;
            m = mean(Y);
            B_Y = (Y >= m).astype(int);
            q = sum(B_Y);
            
            # 建R, G, B representative value matrix
            if sum(R) == 0:
                ar = br = 0;
            elif pnum == q:
                ar = 0;
                br = (sum(R*B_Y) / q);
            else:
                ar = (sum(R*((B_Y-1)*(-1))) / (pnum - q));
                br = (sum(R*B_Y) / q);
                
            if sum(G) == 0:
                ag = bg = 0;
            elif pnum == q:
                ag = 0;
                bg = (sum(G*B_Y) / q);
            else:                
                ag = (sum(G*((B_Y-1)*(-1))) / (pnum - q));
                bg = (sum(G*B_Y) / q);

            if sum(B) == 0:
                ab = bb = 0;
            elif pnum == q:
                ab = 0;
                bb = (sum(B*B_Y) / q);
            else:
                ab = (sum(B*((B_Y-1)*(-1))) / (pnum - q));
                bb = (sum(B*B_Y) / q);
                
            Cr = (B_Y)*br + (B_Y-1)*(-1)*(ar);
            Cg = (B_Y)*bg + (B_Y-1)*(-1)*(ag);
            Cb = (B_Y)*bb + (B_Y-1)*(-1)*(ab);
            
            r_array[y:y + BSIZE_y, x:x + BSIZE_x] = Cr;
            g_array[y:y + BSIZE_y, x:x + BSIZE_x] = Cg;
            b_array[y:y + BSIZE_y, x:x + BSIZE_x] = Cb;
            
    r = Image.fromarray(r_array);
    g = Image.fromarray(g_array);
    b = Image.fromarray(b_array);
    
    img = Image.merge('RGB', (r, g, b));
    img.save("D:/btc.png");
    img.close;

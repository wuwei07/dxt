from PIL import Image
from numpy import *
import numpy as np

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

def BTC(IMG, BSIZE):
    (height, width) = IMG.size;
    # IMG2 = pad(IMG, (BSIZE, BSIZE), 'edge');
    IMG2 = np.array(IMG.convert("L"));
    # IMG2 = np.array(IMG);
    pnum = BSIZE * BSIZE;
    
    for y in my_range(0, height-1, BSIZE):
        for x in my_range(0, width-1, BSIZE):
            A = IMG2[y:y + BSIZE, x:x + BSIZE];
            m = mean(A);
            B = (A >= m).astype(int);
            q = sum(B);
            
            # print(q);
            
            if q == pnum:
                b = m;
                a = 0;
            else:
                s = std(A);
                a = ceil(m - s * sqrt(q / (pnum - q)));
                b = ceil(m + s * sqrt((pnum - q)/ q));
            C = (B)*b + (B-1)*(-1)*(a);
            IMG2[y:y + BSIZE, x:x + BSIZE] = C;
            # print(C);
        
    # rescaled = (255.0 / IMG2.max() * (IMG2 - IMG2.min())).astype(uint8);
    # IMG2 = 128 - IMG2;
    img = Image.fromarray(IMG2);
    img.save("D:/lenna.png")
    img.close;

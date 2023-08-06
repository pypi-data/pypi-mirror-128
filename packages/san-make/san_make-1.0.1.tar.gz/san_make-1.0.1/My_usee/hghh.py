import cv2
from PIL import ImageGrab
import os
class Img_mai:
    def __init__(self):
        self.path=os.path.abspath('.\\imgs')
    def return_pos(self,name):
        ImageGrab.grab().save(self.path+'\\big.jpg')
        # print(self.path+'/big.png')
        s=cv2.imread(self.path+f'\\{name}')
        b=cv2.imread(self.path+'\\big.jpg')
        result=cv2.matchTemplate(b,s,cv2.TM_CCOEFF_NORMED)
        # print(result)
        pos=cv2.minMaxLoc(result)
        # print(pos)
        x=pos[3][0] + int(s.shape[1]/2)
        y=pos[3][1] + int(s.shape[0]/2)
        if pos[1]>0.8:
            # print(x,y)
            return x,y
        else:
            return -1,-1
if __name__ == '__main__':
    t=Img_mai()
    x,y=t.return_pos('user.png')
    print(x,y)


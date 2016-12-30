'''
Created on Dec 26, 2016

@author: taavi
'''
import cv2  # @UnresolvedImport
#import numpy as np
class DrawableButton():
    
    def __init__(self,letter,font):
        self.letter=letter
        self.color=(200,255,155)
        self.font=font
        self.isSelected=False
        self.backgroundFill=1
        self.fontSize=0.7
        self.pixelsPerCharacter=15
        self.width=len(self.letter)*self.pixelsPerCharacter+self.pixelsPerCharacter
        self.height=self.pixelsPerCharacter
        self.boundingBox=((0,0),(0,0))
        
    def drawButton(self,img,x=200,y=200):
        height, width, channels = img.shape
        self.x=x
        self.y=y
        if self.isSelected:
            self.backgroundFill=cv2.FILLED
        else:
            self.backgroundFill=1
        
        
        cv2.rectangle(img, (self.x-self.pixelsPerCharacter, self.y+self.pixelsPerCharacter), (self.x+round((self.width)*self.fontSize), self.y-self.height), (0,0,0), thickness=self.backgroundFill)
        cv2.putText(img=img,text=self.letter,org=(x,y), fontFace = self.font, fontScale=self.fontSize, color=self.color, thickness= 1,lineType= cv2.LINE_AA)
        self.boundingBox=(x-self.pixelsPerCharacter, y+self.pixelsPerCharacter), (x+round((self.width)*self.fontSize), y-self.height)
    #===========================================================================
    # def select(self):
    #     self.isSelected=True
    #     self.backgroundFill=cv2.FILLED
    #     print("button selected: ", self.letter)
    #    
    #     
    # def deselect(self,img):
    #     self.backgroundFill=1
    #     self.drawButton(img, self.x, self.y)
    #     
    #===========================================================================
        
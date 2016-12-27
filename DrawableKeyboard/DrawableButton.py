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
    def drawButton(self,img,x=40,y=40):
        height, width, channels = img.shape
        
        cv2.rectangle(img, (x-self.pixelsPerCharacter, y+self.pixelsPerCharacter), (x+round((self.width)*self.fontSize), y-self.height), (0,0,0), thickness=self.backgroundFill)
         
        cv2.putText(img=img,text=self.letter,org=(x,y), fontFace = self.font, fontScale=self.fontSize, color=self.color, thickness= 1,lineType= cv2.LINE_AA)
        
    def select(self):
        self.backgroundFill=cv2.FILLED
        
    def deselect(self):
        self.backgroundFill=1
        
        
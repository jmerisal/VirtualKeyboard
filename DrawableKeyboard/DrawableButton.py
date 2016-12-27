'''
Created on Dec 26, 2016

@author: taavi
'''
import cv2  # @UnresolvedImport
class DrawableButton():
    
    def __init__(self,letter,size,font):
        self.letter=letter
        
        self.size=size
        self.color=(200,255,155)
        self.font=font
        self.isSelected=False
        self.backgroundFill=1
        self.pixelsPerCharacter=20
        self.width=len(self.letter)*self.pixelsPerCharacter
        self.height=self.pixelsPerCharacter*2
    def drawButton(self,img,x=40,y=40):
        cv2.rectangle(img, (x-self.pixelsPerCharacter, y+self.pixelsPerCharacter), (x+self.width+(self.pixelsPerCharacter), y-self.height), (0,0,0), thickness=self.backgroundFill) 
        cv2.putText(img,self.letter,(x,y), self.font, 1, self.color, 3, cv2.LINE_AA)
        
    def select(self):
        self.backgroundFill=cv2.FILLED
        
    def deselect(self):
        self.backgroundFill=1
        
        
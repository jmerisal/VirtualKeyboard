'''
Created on Dec 26, 2016

@author: taavi
'''
import cv2  # @UnresolvedImport
from DrawableButton import DrawableButton
class DrawableKeyboard:
    def __init__(self):
     
        self.font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        self.buttonGap=15
        
        self.alpha = {
            'row1' : ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p','/'],
            'row2' : ['<<<','a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',',','>>>'],
            'row3' : ['shift','z', 'x', 'c', 'v', 'b', 'n', 'm','.','?','[1,2,3]'],
            'row4' : ['@','#','%','*','[ space ]','+','-','=']
            }
        self.keyboard={}
    
    def drawRow(self,row,rowXCoordinate,rowYCoordinate, img):
        buttonXCoordinate=rowXCoordinate
        buttonYCoordinate=rowYCoordinate                   # for readability and functionality
        
        for k in self.alpha[row]:
            
            button=DrawableButton(letter=k,font=self.font)
            button.drawButton(img, x=buttonXCoordinate, y=buttonYCoordinate)
            self.keyboard[button.boundingBox]=button
            buttonXCoordinate+=button.width+self.buttonGap
    
    def drawKeyboard(self,img):
        #=======================================================================
        # button=DrawableButton('[ space ]',self.font)
        # button.drawButton(img)
         
        #=======================================================================
        #row='row4'
        #self.drawRow(row=row, rowXCoordinate=40, rowYCoordinate=40, img=img)
        
        rowYCoordinate=40
          
        for row in self.alpha.keys():
            #print(row)
          
            self.drawRow(row=row, rowXCoordinate=40, rowYCoordinate=rowYCoordinate, img=img)
            rowYCoordinate+=40+self.buttonGap
          
        print("    ")     
        print("    ")       
    def selectButton(self, xCoordinate,yCoordinate,img):
        for boundingBox in self.keyboard.keys():
            
            if self.isInBounds(xCoordinate, yCoordinate, boundingBox):
                self.keyboard[boundingBox].select()
        
        
    def isInBounds(self,xCoordinate,yCoordinate,boundingBox):
        if boundingBox[0][0]<xCoordinate<boundingBox[1][0] and boundingBox[1][1]<yCoordinate<boundingBox[0][1] :
            return True
        
        return False
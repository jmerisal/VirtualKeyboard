'''
Created on Dec 26, 2016

@author: taavi
'''
import cv2  # @UnresolvedImport
from DrawableButton import DrawableButton
class DrawableKeyboard:
    buttonSize=10
    def __init__(self):
        self.buttonSize=10
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.buttonGap=40
        
        self.alpha = {
            'row1' : ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p','/'],
            'row2' : ['<<<','a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',',','>>>'],
            'row3' : ['shift','z', 'x', 'c', 'v', 'b', 'n', 'm','.','?','[1,2,3]'],
            'row4' : ['@','#','%','*','[ space ]','+','-','=']
            }
        
    
    def drawRow(self,row,rowXCoordinate,rowYCoordinate, img):
        buttonXCoordinate=rowXCoordinate
        buttonYCoordinate=rowYCoordinate                   # for readability and functionality
        
        for k in self.alpha[row]:
            
            button=DrawableButton(letter=k,size=self.buttonSize,font=self.font)
            button.drawButton(img, x=buttonXCoordinate, y=buttonYCoordinate)
            buttonXCoordinate+=button.width+self.buttonGap
    
    def drawKeyboard(self,img):
        #button=DrawableButton('[ space ]',10,self.font)
        #button.drawButton(img)
        #row='row4'
        #self.drawRow(row=row, rowXCoordinate=40, rowYCoordinate=40, img=img)
        
        rowYCoordinate=40
        
        for row in self.alpha.keys():
            print(row)
        
            self.drawRow(row=row, rowXCoordinate=40, rowYCoordinate=rowYCoordinate, img=img)
            rowYCoordinate+=40+self.buttonGap
        
        print("    ")     
        print("    ")       
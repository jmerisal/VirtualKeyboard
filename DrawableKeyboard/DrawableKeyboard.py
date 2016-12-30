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
        self.symbols=[['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p','/'],
                      ['<<<','a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',',','>>>'],
                      ['shift','z', 'x', 'c', 'v', 'b', 'n', 'm','.','?','[1,2,3]'],
                      ['@','#','%','*','[ space ]','+','-','=']
                      ]
        self.alpha = {
            'row1' : ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p','/'],
            'row2' : ['<<<','a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',',','>>>'],
            'row3' : ['shift','z', 'x', 'c', 'v', 'b', 'n', 'm','.','?','[1,2,3]'],
            'row4' : ['@','#','%','*','[ space ]','+','-','=']
            }
        self.keyboard={}
        self.createButtons()
        
    def createButtons(self):
        i=1
        for row in self.symbols:
            buttonRow=[]
            for symbol in row:
                button=DrawableButton(letter=symbol,font=self.font)
                buttonRow.append(button)
            from _ast import Str
            rowIndicator="row"+str(i)
            self.keyboard[rowIndicator]=buttonRow
            i+=1
    
        
    def drawRow(self,row,rowXCoordinate,rowYCoordinate, img):
        buttonXCoordinate=rowXCoordinate
        buttonYCoordinate=rowYCoordinate                   # for readability and functionality
        
        for k in self.alpha[row]:
            
            button=DrawableButton(letter=k,font=self.font)
            button.drawButton(img, x=buttonXCoordinate, y=buttonYCoordinate)
            self.keyboard[button.boundingBox]=button
            buttonXCoordinate+=button.width+self.buttonGap
    
    def drawKeyboard(self,img):
        keyBoardRowLeftXCoordinate=40
        keyBoardRowLeftYCoordinate=40
        buttonYCoordinate=keyBoardRowLeftYCoordinate
        for row in sorted(self.keyboard.keys()):
            buttonXCoordinate=keyBoardRowLeftXCoordinate
            
            for button in self.keyboard[row]:
                
                button.drawButton(img, x=buttonXCoordinate, y=buttonYCoordinate)
                buttonXCoordinate+=button.width+self.buttonGap
            
            buttonYCoordinate+=40+self.buttonGap
        
        
        
    
    def selectButton(self, xCoordinate,yCoordinate,img):
        for row in self.keyboard.keys():
            for button in self.keyboard[row]:
                boundingBox=button.boundingBox
                if boundingBox[0][0]<xCoordinate<boundingBox[1][0] and boundingBox[1][1]<yCoordinate<boundingBox[0][1] :
                    button.isSelected=True
                    print(button.letter)
                else:
                    button.isSelected=False
                    
        #=======================================================================
        # for boundingBox in self.keyboard.keys():
        #     
        #     if self.isInBounds(xCoordinate, yCoordinate, boundingBox):
        #         self.keyboard[boundingBox].select()
        # 
        #=======================================================================
        return 1
 
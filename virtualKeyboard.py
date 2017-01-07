# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 13:57:06 2016
Course project in Digital image processing
VR keyboard
@author: Joonas and Taavi

Progress: Programm works with three middle fingers (starting from index finger)
To do: 
thresholding/ Taavi
contour numbering logic should be overviewed/ Joonas (ideas are welcome)
displayed picture should be resizeable/ Joonas/Taavi

should it work if half of the hand goes out of camera view? (maybe its my cam problem (too low visibility angle) )

"""
import DrawableKeyboard

import tkinter as tk
import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk 
from scipy import *
#from numpy import array
from tkinter import ttk
from tkinter import messagebox
from numpy import sqrt
from operator import itemgetter
from DrawableKeyboard import DrawableKeyboard

class virtualKeyboard(tk.Frame):
    
    def find_largest_contour(self,contours):
        
        max_area = 0
        ci=0
        for i in range(len(contours)): #based on area of contours finding the largest
            cnt=contours[i]
            area = cv2.contourArea(cnt)
            if(area>max_area):
                max_area=area
                ci=i        
        return contours[ci]
    
    def updateFrame(self):
     
       
        
     self.ret, self.frame = self.cap.read()

     if self.flip_image_horizontally.get():
         self.frame=cv2.flip(self.frame,0)
     if self.flip_image_vertically.get():
         self.frame=cv2.flip(self.frame,1)
     #cv2.imshow('ORIGINAL',self.frame)
     self.frame = cv2.medianBlur(self.frame,17)
     # Our operations on the frame come here
     self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
     # define range of skin color in HSV
     hmin=self.h_min.get()
     hmax=self.h_max.get()
     smin=self.s_min.get()
     smax=self.s_max.get()
     vmin=self.v_min.get()
     vmax=self.v_max.get()
     lower_c = np.array([hmin,smin,vmin])
     upper_c = np.array([hmax,smax,vmax])
    
     # Threshold the HSV image to get only skin colors
     mask = cv2.inRange(self.hsv, lower_c, upper_c)
    
     #Morphological "opening and closing"
     mask = cv2.erode(mask,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))) #eroding the image
     mask = cv2.dilate(mask,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))) #dilating the image
     mask = cv2.dilate(mask,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))) #dilating the image
     mask = cv2.erode(mask,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))) #eroding the image
     #smooth it with median filter
     mask = cv2.GaussianBlur(mask,(5,5),0)
     #_, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
     
     #_, self.contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
     #cv2.fillConvexPoly(mask,self.handContour,(255,255,255))
     
     cv2.imshow('mask',mask)
     # Bitwise-AND mask and original image
     #res = cv2.bitwise_and(self.frame,self.frame, mask= mask)
     if self.hand_detected.get():
         _, contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
     else:
         contours=[]
     if len(contours)!=0:    #if there are contours then do sth
        
         #finding largest contour
         cnt=self.find_largest_contour(contours)   
             
         #finding convex hull
         hull = cv2.convexHull(cnt)
         #sorting points from left to right
         left_to_right=sorted(hull, key=lambda h: tuple(h[0])[0])
         
         # ugly way to create empty image of the same size -from some random code :) 
         tempImage = self.frame.copy()
         tempImage = cv2.subtract(tempImage,self.frame)
         tempImage2 = self.frame.copy()
         tempImage2 = cv2.subtract(tempImage,self.frame)
         last = None
         i=0
         for h in left_to_right:
          if last==None:
           if h[0][1]<470:
               cv2.circle(tempImage,tuple(h[0]),5,(255,255,255),-1) #0,255,255 - bgr value for yellow - marks convex hull pts i.e. fingertips
               cv2.circle(tempImage2,tuple(h[0]),30,(255,255,255),-1)
               cv2.putText(self.frame,str(i),tuple(h[0]),cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255))
               i+=1
               last = tuple(h[0])
          else:
           x = last[0]-tuple(h[0])[0]
           y = last[1]-tuple(h[0])[1]
           distance = sqrt(abs(x)**2+abs(y)**2) #distance between prev and current location
           #thumb rule means that index finger is always higher than thumb
           thumb_rule=True
           if i==1 and y<35: #if index finger is not far enough from thumb then its not index finger
              thumb_rule=False
                       
           if distance>50 and y>-120 and thumb_rule : #if points are not too close and new point is not too much "lower"
                   cv2.circle(tempImage,tuple(h[0]),5,(255,255,255),-1) #yellow - marks convex hull pts i.e. fingertips
                   cv2.circle(tempImage2,tuple(h[0]),30,(255,255,255),-1)
                   cv2.putText(self.frame,str(i),tuple(h[0]),cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255))
                   i+=1
                   last = tuple(h[0])
         if i==5:
             self.five_fingers = tempImage
             _,self.five_fingers = cv2.threshold(self.five_fingers,127,255,0)
             self.click_enabled = True # hand in selecting position click allowed
             
         if i==4 and self.click_enabled: #if one finger is missing then its a click, click_enabled assures one click to letter
             self.five_fingers=cv2.subtract(self.five_fingers,tempImage2)
             gray = cv2.cvtColor(self.five_fingers, cv2.COLOR_BGR2GRAY)
             _, cnt, _ = cv2.findContours(gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
             if len(cnt)==1:
                 (x,y),radius = cv2.minEnclosingCircle(cnt[0])
                 center = (int(x),int(y))
                 radius = int(radius)
                 cv2.circle(self.frame,center,radius,(0,255,0),2)
                 self.keyboard.selectButton(xCoordinate=int(x), yCoordinate=int(y),img=tempImage)
                 self.click_enabled = False # one click limited to one letter
                 
         self.frame = cv2.add(self.frame,tempImage)
         #cv2.drawContours(frame,contours,-1,(0,255,0),3) #this would draw the hand contour    
         cv2.drawContours(self.frame,[hull],0,(0,0,255),1) #red color - marks hands
     if self.hand_detected.get():    
         self.keyboard.drawKeyboard(self.frame)
     else:
         #draw handcontour
         cv2.drawContours(self.frame,[self.handContour],-1,(255,255,255),3)
     
     # Display the resulting frame
     cv2.imshow('frame',self.frame)
     
     #cv2.imshow('res',res)
    
     # Display the resulting frame
     
     if cv2.waitKey(1) & 0xFF == ord('q'):
         self.cap.release()
         cv2.destroyAllWindows()
         sliders.destroy()
     sliders.after(2, self.updateFrame) 
     
    def autoThreshold(self): 
        height, width, channels = self.frame.shape
        
        maskimage= np.zeros((height,width,1), np.uint8)
        result, croppedhand = self.cap.retrieve()
        if self.flip_image_horizontally.get():
            croppedhand=cv2.flip(croppedhand,0)
        if self.flip_image_vertically.get():
            croppedhand=cv2.flip(croppedhand,1)
        croppedhand = cv2.medianBlur(croppedhand,17)
        cv2.imshow("retrieved for cropping",croppedhand)
        
        
        cv2.drawContours(maskimage,[self.handContour],0,(255,255,255),cv2.FILLED)
        kernel = np.ones((10,10),np.uint8)
        maskimage = cv2.erode(maskimage,kernel,iterations = 1)
        croppedhand = cv2.bitwise_and(croppedhand, croppedhand, mask=maskimage)
        hsv = cv2.cvtColor(croppedhand, cv2.COLOR_BGR2HSV)
        #print(hsv.shape)
        #testhsv
        #hsv=hsv[270:273,330:333]
        hue=hsv[:,:,0]
        saturation=hsv[:,:,1]
        value=hsv[:,:,2]
        min_hue=hue[hue>0].min()
        max_hue=hue[hue<255].max()
        min_saturation=saturation[saturation>0].min()
        max_saturation=saturation[saturation<255].max()
        min_value=value[value>0].min()
        max_value=value[value<255].max()
        self.h_min.set(min_hue)
        self.h_max.set(max_hue)
        self.s_min.set(min_saturation)
        self.s_max.set(max_saturation)
        self.v_min.set(min_value)
        self.v_max.set(max_value)
        #hsv=[]
        #print(hsv)
        #print("hue: ")
        #print(hue)
        #print("saturation: ")
        #print(saturation)
        #print("Value: ")
        #print(value)
        
        
        
        
        print("Minimum hue: ",hue[hue>0].min())
        print("Maximum hue: ",hue[hue<255].max())
        print("Minimum saturation: ",saturation[saturation>0].min())
        print("Maximum saturation: ",saturation[saturation<255].max())
        print("Minimum value: ",value[value>0].min())
        print("Maximum value: ",value[value<255].max())
        
        
        #cv2.imshow('maskimage', maskimage)
        cv2.imshow('croppedhand', hsv)
        
        
        
    
    
    
    def on_closing(self):
     if messagebox.askokcancel("Quit", "Do you want to quit?"):    
         self.cap.release()
         cv2.destroyAllWindows()
         sliders.destroy()
         
    def saveContour(self):
        
        print(self.contours) 
        print("contours detected: ", len(self.contours))   
    def __init__(self, root):
        
        self.contours = []
        self.handContour=np.asanyarray([[[363,81]],[[362,82]],[[361,82]],[[358,85]],[[356,85]],[[354,87]],[[354,88]],[[353,89]],[[353,92]],[[352,93]],[[352,101]],[[351,102]],[[351,125]],[[350,126]],[[350,133]],[[349,134]],[[349,139]],[[348,140]],[[348,156]],[[349,157]],[[349,164]],[[347,166]],[[346,166]],[[343,163]],[[343,162]],[[342,161]],[[342,159]],[[341,158]],[[341,156]],[[340,155]],[[340,154]],[[339,153]],[[339,150]],[[338,149]],[[338,148]],[[337,147]],[[337,145]],[[336,144]],[[336,142]],[[335,141]],[[335,138]],[[334,137]],[[334,135]],[[333,134]],[[333,131]],[[332,130]],[[332,126]],[[331,125]],[[331,121]],[[330,120]],[[330,118]],[[329,117]],[[329,114]],[[328,113]],[[328,111]],[[327,110]],[[327,109]],[[322,104]],[[319,104]],[[318,103]],[[312,103]],[[306,109]],[[306,110]],[[305,111]],[[305,114]],[[304,115]],[[304,126]],[[305,127]],[[305,133]],[[306,134]],[[306,137]],[[307,138]],[[307,144]],[[308,145]],[[308,151]],[[309,152]],[[309,158]],[[310,159]],[[310,162]],[[311,163]],[[311,166]],[[312,167]],[[312,169]],[[313,170]],[[313,172]],[[314,173]],[[314,176]],[[315,177]],[[315,179]],[[316,180]],[[316,184]],[[317,185]],[[317,190]],[[318,191]],[[318,195]],[[319,196]],[[319,203]],[[320,204]],[[320,208]],[[319,209]],[[319,213]],[[318,214]],[[318,216]],[[317,217]],[[317,218]],[[316,219]],[[316,221]],[[315,222]],[[315,223]],[[314,224]],[[314,225]],[[312,227]],[[312,228]],[[305,235]],[[304,235]],[[303,236]],[[299,236]],[[298,235]],[[297,235]],[[296,234]],[[295,234]],[[293,232]],[[292,232]],[[289,229]],[[288,229]],[[286,227]],[[285,227]],[[283,225]],[[282,225]],[[281,224]],[[280,224]],[[279,223]],[[278,223]],[[277,222]],[[276,222]],[[275,221]],[[274,221]],[[273,220]],[[271,220]],[[270,219]],[[267,219]],[[266,218]],[[262,218]],[[261,217]],[[251,217]],[[250,218]],[[247,218]],[[245,220]],[[244,220]],[[241,223]],[[241,224]],[[239,226]],[[239,232]],[[240,233]],[[240,235]],[[246,241]],[[247,241]],[[248,242]],[[249,242]],[[250,243]],[[251,243]],[[252,244]],[[253,244]],[[255,246]],[[256,246]],[[257,247]],[[258,247]],[[259,248]],[[260,248]],[[261,249]],[[262,249]],[[263,250]],[[264,250]],[[266,252]],[[267,252]],[[268,253]],[[269,253]],[[270,254]],[[271,254]],[[272,255]],[[273,255]],[[274,256]],[[275,256]],[[277,258]],[[278,258]],[[281,261]],[[282,261]],[[287,266]],[[288,266]],[[291,269]],[[292,269]],[[294,271]],[[295,271]],[[296,272]],[[297,272]],[[298,273]],[[299,273]],[[300,274]],[[301,274]],[[302,275]],[[304,275]],[[305,276]],[[306,276]],[[307,277]],[[308,277]],[[309,278]],[[310,278]],[[311,279]],[[312,279]],[[314,281]],[[315,281]],[[317,283]],[[318,283]],[[320,285]],[[321,285]],[[323,287]],[[324,287]],[[326,289]],[[327,289]],[[329,291]],[[331,291]],[[332,292]],[[333,292]],[[334,293]],[[335,293]],[[336,294]],[[338,294]],[[339,295]],[[341,295]],[[342,296]],[[343,296]],[[345,298]],[[346,298]],[[348,300]],[[348,301]],[[350,303]],[[350,304]],[[351,305]],[[351,308]],[[350,309]],[[350,323]],[[351,324]],[[351,325]],[[356,330]],[[357,330]],[[358,331]],[[361,331]],[[362,332]],[[366,332]],[[367,331]],[[372,331]],[[373,330]],[[374,330]],[[375,329]],[[376,329]],[[384,321]],[[384,320]],[[385,319]],[[385,318]],[[386,317]],[[386,315]],[[387,314]],[[387,313]],[[388,312]],[[388,311]],[[389,310]],[[389,309]],[[390,308]],[[390,306]],[[392,304]],[[392,303]],[[394,301]],[[394,300]],[[396,298]],[[396,297]],[[399,294]],[[399,293]],[[402,290]],[[402,289]],[[403,288]],[[403,287]],[[405,285]],[[405,284]],[[406,283]],[[406,282]],[[407,281]],[[407,280]],[[408,279]],[[408,278]],[[409,277]],[[409,276]],[[410,275]],[[410,273]],[[411,272]],[[411,271]],[[412,270]],[[412,268]],[[413,267]],[[413,265]],[[414,264]],[[414,261]],[[415,260]],[[415,257]],[[416,256]],[[416,252]],[[417,251]],[[417,247]],[[418,246]],[[418,241]],[[419,240]],[[419,237]],[[420,236]],[[420,233]],[[421,232]],[[421,230]],[[422,229]],[[422,228]],[[423,227]],[[423,225]],[[424,224]],[[424,223]],[[425,222]],[[425,220]],[[427,218]],[[427,217]],[[428,216]],[[428,215]],[[430,213]],[[430,212]],[[435,207]],[[435,206]],[[441,200]],[[441,199]],[[446,194]],[[446,193]],[[449,190]],[[449,189]],[[452,186]],[[452,185]],[[454,183]],[[454,182]],[[456,180]],[[456,179]],[[458,177]],[[458,176]],[[459,175]],[[459,174]],[[461,172]],[[461,171]],[[462,170]],[[462,169]],[[463,168]],[[463,166]],[[464,165]],[[464,163]],[[465,162]],[[465,155]],[[464,154]],[[464,153]],[[461,150]],[[460,150]],[[459,149]],[[450,149]],[[447,152]],[[446,152]],[[443,155]],[[443,156]],[[440,159]],[[440,160]],[[438,162]],[[438,163]],[[435,166]],[[435,167]],[[419,183]],[[418,183]],[[416,185]],[[415,185]],[[413,187]],[[410,187]],[[405,182]],[[405,178]],[[406,177]],[[406,174]],[[407,173]],[[407,170]],[[408,169]],[[408,166]],[[409,165]],[[409,162]],[[410,161]],[[410,157]],[[411,156]],[[411,152]],[[412,151]],[[412,148]],[[413,147]],[[413,144]],[[414,143]],[[414,140]],[[415,139]],[[415,136]],[[416,135]],[[416,133]],[[417,132]],[[417,129]],[[418,128]],[[418,125]],[[419,124]],[[419,121]],[[420,120]],[[420,114]],[[421,113]],[[421,107]],[[420,106]],[[420,104]],[[415,99]],[[414,99]],[[413,98]],[[407,98]],[[405,100]],[[404,100]],[[400,104]],[[400,105]],[[399,106]],[[399,107]],[[398,108]],[[398,110]],[[397,111]],[[397,114]],[[396,115]],[[396,118]],[[395,119]],[[395,121]],[[394,122]],[[394,124]],[[393,125]],[[393,127]],[[392,128]],[[392,131]],[[391,132]],[[391,133]],[[390,134]],[[390,136]],[[389,137]],[[389,138]],[[388,139]],[[388,141]],[[387,142]],[[387,143]],[[386,144]],[[386,146]],[[385,147]],[[385,148]],[[384,149]],[[384,152]],[[383,153]],[[383,155]],[[381,157]],[[380,157]],[[378,155]],[[378,154]],[[377,153]],[[377,139]],[[376,138]],[[376,133]],[[375,132]],[[375,126]],[[376,125]],[[376,113]],[[377,112]],[[377,94]],[[376,93]],[[376,89]],[[375,88]],[[375,87]],[[370,82]],[[369,82]],[[368,81]]])
        self.keyboard=DrawableKeyboard()
        self.cap = cv2.VideoCapture(0)
        self.ret, self.frame = self.cap.read()
        
        self.five_fingers = self.frame.copy()
        self.five_fingers = cv2.subtract(self.five_fingers,self.frame)
        self.click_enabled = True
        tk.Frame.__init__(self, sliders)
        #Sliders for thresholding input image       
        self.h_min = Scale(sliders,from_=0, to=180,resolution=1,showvalue=1, label='H_min', orient=HORIZONTAL)
        self.h_min.grid(row=0, column=0)
        self.h_min.set(0)
        self.h_max = Scale(sliders,from_=0, to=180,resolution=1,showvalue=1, label='H_max', orient=HORIZONTAL)
        self.h_max.grid(row=1, column=0)
        self.h_max.set(40)
        
        self.s_min = Scale(sliders,from_=0, to=255,resolution=1,showvalue=1, label='S_min', orient=HORIZONTAL)
        self.s_min.grid(row=2, column=0)
        self.s_min.set(80)
        self.s_max = Scale(sliders,from_=0, to=255,resolution=1,showvalue=1, label='S_max', orient=HORIZONTAL)
        self.s_max.grid(row=3, column=0)
        self.s_max.set(255) 
        
        self.v_min = Scale(sliders,from_=0, to=255,resolution=1,showvalue=1, label='V_min', orient=HORIZONTAL)
        self.v_min.grid(row=4, column=0)
        self.v_min.set(90)
        self.v_max = Scale(sliders,from_=0, to=255,resolution=1,showvalue=1, label='V_max', orient=HORIZONTAL)
        self.v_max.grid(row=5, column=0)
        self.v_max.set(255)
        
        #self.saveContourButton= Button(sliders, text="Save Contour",command=self.saveContour).grid(row=6,column=0)
        self.autoThresholdButton=Button(sliders, text="Auto Threshold",command=self.autoThreshold).grid(row=6,column=0)
        
        self.flip_image_horizontally = IntVar()
        self.flip_image_horizontally_checkbutton= Checkbutton(sliders, text="Flip horizontally", variable=self.flip_image_horizontally).grid(row=7,column=0)
        self.flip_image_vertically = IntVar()
        self.flip_image_vertically_checkbutton= Checkbutton(sliders, text="Flip vertically", variable=self.flip_image_vertically).grid(row=8,column=0)
        
        self.hand_detected=IntVar()
        self.hand_detected_checkbutton=Checkbutton(sliders, text="Hand detected", variable=self.hand_detected).grid(row=9,column=0)
        
            
        
        self.canvas = Canvas(sliders, width=100, height=75)
        self.canvas.grid(row=10,columnspan=1)
        
        sliders.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.updateFrame()

if __name__ == "__main__":
    # INITIALIZE
    sliders = tk.Tk()
    sliders.wm_title("HSV")
    # INITIALIZE CLASS
    virtualKeyboard(sliders).grid()
    # LIVE
    
    sliders.mainloop()

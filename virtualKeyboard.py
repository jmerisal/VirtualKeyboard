# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 13:57:06 2016
Course project in Digital image processing
VR keyboard
@author: Joonas
"""
import DrawableKeyboard
"""
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    cv2.imshow('hsv',hsv)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
"""

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
     

     if self.flip_image_upside_down:
         self.frame=cv2.flip(self.frame,0)
     self.frame=cv2.flip(self.frame,-1) #rotating 180deg
     cv2.imshow('ORIGINAL',self.frame)
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
      
     cv2.imshow('mask',mask)
     # Bitwise-AND mask and original image
     res = cv2.bitwise_and(self.frame,self.frame, mask= mask)
     
     _, contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
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
         last = None
         i=0
         for h in left_to_right:
          if last==None:
           cv2.circle(tempImage,tuple(h[0]),5,(0,255,255),2) #0,255,255 - bgr value for yellow - marks convex hull pts i.e. fingertips
           cv2.putText(tempImage,str(i),tuple(h[0]),cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255))
           i+=1
           last = tuple(h[0])
          else:
           x = last[0]-tuple(h[0])[0]
           y = last[1]-tuple(h[0])[1]
           distance = sqrt(abs(x)**2+abs(y)**2) #distance between prev and current location
           #thumb rule means that index finger is always higher than thumb
           thumb_rule=True
           if i==1 and y<30:
              thumb_rule=False
                       
           if distance>50 and y>-120 and thumb_rule : #if points are not too close and new point is not too much "lower"
                   cv2.circle(tempImage,tuple(h[0]),10,(0,255,255),2) #yellow - marks convex hull pts i.e. fingertips
                   cv2.putText(tempImage,str(i),tuple(h[0]),cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255))
                   if i ==1:
                       #print("1st finger position", h[0])
                       self.keyboard.selectButton(xCoordinate=h[0][0], yCoordinate=h[0][1],img=tempImage)
                   i+=1
                   last = tuple(h[0])
          
        
         self.frame = cv2.add(self.frame,tempImage)
         #cv2.drawContours(frame,contours,-1,(0,255,0),3)    
         cv2.drawContours(self.frame,[hull],0,(0,0,255),3) #red color - marks hands
         
     self.keyboard.drawKeyboard(self.frame)
     # Display the resulting frame
     cv2.imshow('frame',self.frame)
     
     cv2.imshow('res',res)
    
     # Display the resulting frame
     
     if cv2.waitKey(1) & 0xFF == ord('q'):
         self.cap.release()
         cv2.destroyAllWindows()
         sliders.destroy()
     sliders.after(2, self.updateFrame)  
    
    def on_closing(self):
     if messagebox.askokcancel("Quit", "Do you want to quit?"):    
         self.cap.release()
         cv2.destroyAllWindows()
         sliders.destroy()
         
        
    def __init__(self, root):
        
        self.keyboard=DrawableKeyboard()
        self.cap = cv2.VideoCapture(0)
        self.ret, self.frame = self.cap.read()
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
        
        self.flip_image_upside_down = IntVar()
        self.flip_image_upside_down_checkbutton= Checkbutton(sliders, text="Flip image upside down", variable=self.flip_image_upside_down).grid(row=6,column=0)
        
        
            
        
        self.canvas = Canvas(sliders, width=100, height=75)
        self.canvas.grid(row=7,columnspan=1)
        
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
"""
from PIL import ImageTk, Image
 
width, height = 800, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
 
root = tk.Tk()
root.bind('q', lambda e: root.quit())
lmain = tk.Label(root)
lmain.pack()
 
def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)
 
show_frame()
root.mainloop()
"""
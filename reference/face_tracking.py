import cv2
import numpy as np
import dlib

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# create an object
cap = cv2.VideoCapture(0)
#Start the window thread for the two windows we are using
cv2.startWindowThread()
#Create the tracker we will use
tracker = dlib.correlation_tracker()
trackingFace = 0
rectangleColor = (0,165,255)
while True:
      #capture frame by frame
      #returns a bool (True/False). If frame is read correctly, it will be True.
      ret,frame = cap.read()
      frame = cv2.flip(frame,1)
      
      if not trackingFace:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(gray, 1.3, 5)
            img = np.zeros((480,640,3),np.uint8)

            maxArea = 0
            x = 0
            y = 0
            w = 0
            h = 0

            for (_x,_y,_w,_h) in faces:
                  if  _w*_h > maxArea:
                        x = int(_x)
                        y = int(_y)
                        w = int(_w)
                        h = int(_h)
                        maxArea = w*h

            if maxArea > 0 :
    
                    #Initialize the tracker
                    tracker.start_track(frame,
                                        dlib.rectangle( x-10,
                                                        y-20,
                                                        x+w+10,
                                                        y+h+20))

                    #Set the indicator variable such that we know the
                    #tracker is tracking a region in the image
                    trackingFace = 1
      
      if trackingFace:
            trackingQuality = tracker.update(frame)
            if trackingQuality >= 8.5:
                  tracked_position =  tracker.get_position()
                  t_x = int(tracked_position.left())
                  t_y = int(tracked_position.top())
                  t_w = int(tracked_position.width())
                  t_h = int(tracked_position.height())
                  cv2.rectangle(frame, (t_x, t_y),(t_x + t_w , t_y + t_h),rectangleColor ,2)
                  
            else:
                  trackingFace = 0

            
      #final = cv2.flip(img,1)
      cv2.imshow('video',frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows() 
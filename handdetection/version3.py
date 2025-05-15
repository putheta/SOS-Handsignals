import cv2
import mediapipe as mp
import os

import datetime

import geocoder
g = geocoder.ip('me')
location = g.city + ", " + g.country if g.ok else "Unknown location"

vid = cv2.VideoCapture(0)
# vid = cv2.VideoCapture(1)
# vid = cv2.VideoCapture(r"C:\Users\puthe\Pictures\Camera Roll\WIN_20250508_12_27_12_Pro.mp4")


os.chdir(os.path.dirname(__file__))
save_path = "static"
check = [0,0]
mphands = mp.solutions.hands
Hands = mphands.Hands(max_num_hands= 1, min_detection_confidence= 0.7, min_tracking_confidence= 0.6 )
mpdraw = mp.solutions.drawing_utils
font = cv2.FONT_HERSHEY_SIMPLEX
count = 0
top = 0
bottom = 0
max_height = 0 

SOS_Count = 0

closed_program = 0

check = [0,0]

min_ = float('inf')
max_ = float('-inf')





while True : 
    _, frame = vid.read()
    # convert from bgr to rgb
    RGBframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = Hands.process(RGBframe)
    
    if result.multi_hand_landmarks:
        #print("hand found")
        for handLm in result.multi_hand_landmarks :
            #print(handLm)
            # mpdraw.draw_landmarks(frame, handLm, mphands.HAND_CONNECTIONS,
            #                      mpdraw.DrawingSpec(color=(0, 0, 255), circle_radius=7,
            #                                         thickness=cv2.FILLED),
            #                      mpdraw.DrawingSpec(color=(0, 255, 0), thickness=5)
            #                      )    
            for id, lm in enumerate(handLm.landmark):
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 12 :
                   Tx_12 , Ty_12 = cx,cy
                   if max_height == 0 :
                        top = Ty_12
                
                if id == 0 :
                    Tx_0 , Ty_0 = cx,cy
                    bottom = Ty_0
                    frame_ready = True
                    
                if id == 8 :
                    Tx_8 , Ty_8 = cx,cy
         
                    try :
                        if check[0] ==1 :
                            if Ty_8 > max_:
                                max_ = Ty_8  
                            if Ty_8 < min_:
                                min_ = Ty_8
              
                            
                            if abs((h2//1.5) -( max_-min_)) <= (0.0016 * h2**2 - 0.459 * h2 + 37.25):
                                # cv2.putText(frame, "SOS" , (Tx_8,Ty_8), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 5) 
                                
                                now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
                                cv2.putText(frame, f"Location: {location}", (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                                cv2.putText(frame, f"Time: {now}", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                                
                                
                                if(SOS_Count == 0) :
                                    print("SOS")
                                    SOS_Count+=1
                                    now2 = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                                    filename = f"{save_path}/capture_{now2}.jpg"
                                    cv2.imwrite(filename,frame)
                                    print(f"บันทึกภาพ {filename}")
                                  
                                # cv2.waitKey(3000)
                                # closed_program = 1
                            else :
                                SOS_Count = 0 
                                
                          
                    except : 
                        pass
                    
                
                if id == 4 :
                    Tx_4 , Ty_4 = cx,cy 
                  
                if id == 13 :
                    Tx_13 , Ty_13 =  cx,cy
                   
                    try :
                        if abs(Tx_4-Tx_13) <= ((h2/8)+5) :
                            check[0] = 1
                        
                        else :
                            max_height =0
                    except :
                        pass
                    
    h, w, _ = frame.shape         
    # print("height" ,h)     
    if check[0] == 1 :
        if top > max_height :
            max_height = top
            top = max_height
 
    try :
        if frame_ready and 0 <= top < bottom <= h :
            cropped = frame[top:bottom, 0:w]
            h2 , w2, _ = cropped.shape
       
            cv2.imshow("Cropped", cropped)
    except:
        cv2.imshow("Cropped", frame)
        
    cv2.imshow("video", frame)

    
    if cv2.waitKey(1) != -1 or closed_program == 1:
        break

vid.release()
cv2.destroyAllWindows()

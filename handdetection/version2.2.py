import cv2
import mediapipe as mp

vid = cv2.VideoCapture(0)
# vid = cv2.VideoCapture(1)
# vid = cv2.VideoCapture(r"C:\Users\puthe\Pictures\Camera Roll\WIN_20250508_12_27_12_Pro.mp4")

check = [0,0]
mphands = mp.solutions.hands
Hands = mphands.Hands(max_num_hands= 1, min_detection_confidence= 0.7, min_tracking_confidence= 0.6 )
mpdraw = mp.solutions.drawing_utils
font = cv2.FONT_HERSHEY_SIMPLEX
count = 0
top = 0
bottom = 0
max_height = 0 

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
            #    print(id, cx, cy)

               # cv2.circle(frame, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
                if id == 12 :
                   Tx_12 , Ty_12 = cx,cy
                   if max_height == 0 :
                        top = Ty_12
                        # print(top)
                if id == 0 :
                    Tx_0 , Ty_0 = cx,cy
                    bottom = Ty_0
                    frame_ready = True
                    
                if id == 8 :
                    Tx_8 , Ty_8 = cx,cy
                    # print(Ty_8)
                    try :
                        if check[0] ==1 :
                            if Ty_8 > max_:
                                max_ = Ty_8  
                            if Ty_8 < min_:
                                min_ = Ty_8
                            cv2.circle(frame, (Tx_8, Ty_8), h2//15, (0, 255, 0), cv2.FILLED)
                            # print("height : ",h2)
                            # print("height/1.5 = ",h2//1.7)
                            # print("min-max = ", max_-min_)
                            # print("error =",(0.0016 * h2**2 - 0.459 * h2 + 37.25)) 
                            
                            if abs((h2//1.5) -( max_-min_)) <= (0.0016 * h2**2 - 0.459 * h2 + 37.25):
                                cv2.putText(frame, "SOS" , (Tx_8,Ty_8), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 5) 
                                # cv2.waitKey(3000)
                                # closed_program = 1
                                
                            # elif abs(Ty_8-min_) <= 10 and check[1]==1 :
                            #     check[0] = 0
                            #     check[1] = 0
                            #     top = 0 
                            #     bottom = h
                            #     cv2.putText(frame, "end" , (Tx_8,Ty_8+20), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 5) 
                    except : 
                        pass
                    
                
                if id == 4 :
                    Tx_4 , Ty_4 = cx,cy 
                    cv2.circle(frame, (Tx_4, Ty_4), 6, (0, 255, 0), cv2.FILLED)
                if id == 13 :
                    Tx_13 , Ty_13 =  cx,cy
                    cv2.circle(frame, (Tx_13, Ty_13), 6, (0, 0, 255), cv2.FILLED)
                    try :
                        if abs(Tx_4-Tx_13) <= ((h2/8)+5) :
                            check[0] = 1
                            # cv2.putText(frame, "SOS" , (Tx_4,Ty_4), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0), 2) 
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
            # print("max height",max_height)
            # print("\n","height",h2)
            # print("id=12",Ty_12)
                            
            #print("Threshold = ",(h2/8)+5)
            # print('\n',"SOS Detected")
            # print("height", h2)
            # print("id = 4",Tx_4,"",Ty_4)
            # print("id = 13",Tx_13,"",Ty_13)
            # print('\n')
    try :
        if frame_ready and 0 <= top < bottom <= h :
            cropped = frame[top:bottom, 0:w]
            h2 , w2, _ = cropped.shape
            # cv2.putText(cropped, f"min = {min_}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            # cv2.putText(cropped, f"max   = {max_}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            # cv2.putText(cropped, f"ty_8 = {Ty_8}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            # print("height", h2)
            # print("id = 4",Tx_4,"",Ty_4)  
            # print("id = 13",Tx_13,"",Ty_13)
            # print('\n')   
            cv2.imshow("Cropped", cropped)
    except:
        cv2.imshow("Cropped", frame)
        
    cv2.imshow("video", frame)

    
    if cv2.waitKey(1) != -1 or closed_program == 1:
        break

vid.release()
cv2.destroyAllWindows()

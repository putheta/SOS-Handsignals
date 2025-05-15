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

min_ = float('inf')
max_ = float('-inf')


def sum_self_n_times(n, rounds=3):
    return [n * i for i in range(1, rounds + 1)]


def check_(height, position):
    bol = False
    n_list = sum_self_n_times((height//2) // 3)
    print(n_list)
    for value in n_list:
        if value - 10<= position <= value + 10:
            bol = True
        else :
            bol = False
    return bol



while True :
    check = [0,0]
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
                    if Tx_8 > max_:
                        max_ = Tx_8
                    if Tx_8 < min_:
                        min_ = Tx_8
                    try :
              
                        print("height :",h2,'\n')
                        # print("id = 8", Tx_8,Ty_8)
                        print(check_(h2,Ty_8))
                        cv2.circle(frame, (Tx_8, Ty_8), h2//15, (0, 255, 0), cv2.FILLED)
                        print('\n',Ty_8,'\n')
                        print("bottom",bottom)
                        print("max",max_)
                        
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
                            cv2.putText(frame, "SOS" , (Tx_4,Ty_4), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0), 2) 
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
            # print("height", h2)
            # print("id = 4",Tx_4,"",Ty_4)
            # print("id = 13",Tx_13,"",Ty_13)
            # print('\n')
            cv2.imshow("Cropped", cropped)
    except:
        cv2.imshow("Cropped", frame)
        
    cv2.imshow("video", frame)

    
    if cv2.waitKey(1) != -1:
        break

vid.release()
cv2.destroyAllWindows()

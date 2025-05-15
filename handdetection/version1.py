import cv2
import mediapipe as mp

vid = cv2.VideoCapture(0)
check = [0,0]
mphands = mp.solutions.hands
Hands = mphands.Hands(max_num_hands= 1, min_detection_confidence= 0.7, min_tracking_confidence= 0.6 )
mpdraw = mp.solutions.drawing_utils
font = cv2.FONT_HERSHEY_SIMPLEX
count = 0

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
            #mpdraw.draw_landmarks(frame, handLm, mphands.HAND_CONNECTIONS,
            #                      mpdraw.DrawingSpec(color=(0, 0, 255), circle_radius=7,
            #                                         thickness=cv2.FILLED),
            #                      mpdraw.DrawingSpec(color=(0, 255, 0), thickness=7)
            #                      )
            for id, lm in enumerate(handLm.landmark):
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
            #    print(id, cx, cy)

               # cv2.circle(frame, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
                if id == 4 :
                    #pass
                    Tx_4, Ty_4 = cx, cy
                    #print(id,Tx,Ty)
                    cv2.circle(frame, (Tx_4, Ty_4), 6, (255, 0, 0), cv2.FILLED)
                if id == 17 :
                    #pass
                    Tx_17, Ty_17 = cx, cy
                    #cv2.circle(frame, (Tx_17, Ty_17), 6, (255, 0, 0), cv2.FILLED)
                    #print(id,Tx,Ty)
                    if abs(Tx_4 - Tx_17) > 0 and abs(Tx_4 - Tx_17) < 50 and abs(Ty_4 - Ty_17) > 0 and abs(Ty_4 - Ty_17) < 50 :
                            #print(abs(Tx_4 - Tx_17),abs(Ty_4 - Ty_17))
                            cv2.circle(frame, (Tx_17, Ty_17), 6, (0, 0, 255), cv2.FILLED)
                            check[0] = 1
                    
                if id == 8 :
                    #pass
                    Tx_8, Ty_8 = cx, cy
                    cv2.circle(frame, (Tx_8, Ty_8), 6, (255, 0, 0), cv2.FILLED)
                    if abs(Tx_1 - Tx_8) > 0 and abs(Tx_1 - Tx_8) < 100 and abs(Ty_1 - Ty_8) > 0 and abs(Ty_1 - Ty_8) < 100 :
                            print(abs(Tx_1 - Tx_8),abs(Ty_1 - Ty_8))
                            cv2.circle(frame, (Tx_1, Ty_1), 6, (0, 0, 255), cv2.FILLED)
                            check[1] = 1
                    else :
                        check[1] = 0
                        check[0] = 0
                    print(id,Tx_8,Ty_8)
                    #cv2.line(frame, (cx, cy), (Tx, Ty), (255, 0, 0), 5 )
                    
                if id == 1 :
                    #pass
                    Tx_1, Ty_1 = cx, cy
                    cv2.circle(frame, (Tx_1, Ty_1), 6, (255, 0, 0), cv2.FILLED)
                    print(id,Tx_1,Ty_1)
                    #cv2.line(frame, (cx, cy), (Tx, Ty), (255, 0, 0), 5 )
    
    
    if check[0] * check[1] == 1 :
        cv2.putText(frame, "SOS" , (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255), 2)
        #if count ==0 :
        #    cv2.imshow("SOS",frame)
        #    count+=1
        
    
    cv2.imshow("video", frame)
    
    if cv2.waitKey(1) != -1:
        break

vid.release()
cv2.destroyAllWindows()

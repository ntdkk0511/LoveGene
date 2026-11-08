import cv2
from deepface import DeepFace
import numpy as np
#import matplotlib.pyplot as plt

ang = 0
dis = 0
fea = 0
hap = 0
sad = 0
sur = 0
neu = 0
sum = 0

# Webカメラを開く
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    try:
        # フレームを分析
        analysis = DeepFace.analyze(frame, 
                                  actions=['emotion'],
                                  detector_backend='opencv',
                                  enforce_detection=False)
        
        if len(analysis) > 0:
            # 結果を表示
            emotion = analysis[0]["dominant_emotion"]
            #print(emotion)
            cv2.putText(frame, emotion, (50,50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            
            #割合表示
            if emotion == "angry":#怒り
                ang += 1
            elif emotion == "disgust":#嫌悪
                dis += 1
            elif emotion == "fear":#恐怖
                fea += 1
            elif emotion == "happy":#喜び
                hap += 1
            elif emotion == "sad":#悲しみ
                sad += 1
            elif emotion == "surprise":#驚き
                sur += 1
            elif emotion == "neutral":#普通
                neu += 1
            sum += 1
        
    except Exception as e:
        pass
        
    cv2.imshow('Real Time Analysis', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        ang_w = ang * 100 / sum
        dis_w = dis * 100 / sum
        fea_w = fea * 100 / sum
        hap_w = hap * 100 / sum
        sad_w = sad * 100 / sum
        sur_w = sur * 100 / sum
        neu_w = neu * 100 / sum
        #label = ["怒り","嫌悪","恐怖","喜び","悲しみ","驚き","普通"]
        #value = [ang_w,dis_w,fea_w,hap_w,sad_w,sur_w,neu_w]
        #plt.pie(value,labels=label,autopct="%1.1f%%",startangle=90)
        #plt.title("Emotion Analysis")
        #plt.axis("equal")
        #plt.savefig("emotion_pie.png")
        print("怒り:",round(ang_w,1),"%")
        print("嫌悪:",round(dis_w,1),"%")
        print("恐怖:",round(fea_w,1),"%")
        print("喜び:",round(hap_w,1),"%")
        print("悲しみ:",round(sad_w,1),"%")
        print("驚き:",round(sur_w,1),"%")
        print("普通:",round(neu_w,1),"%")
        break

cap.release()
cv2.destroyAllWindows()
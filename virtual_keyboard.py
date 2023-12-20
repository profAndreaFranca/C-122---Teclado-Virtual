import cv2
import mediapipe as mp 
from pynput.keyboard import Key, Controller

keyboard = Controller()

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence = 0.8, min_tracking_confidence = 0.5)

vid = cv2.VideoCapture(0)

width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

tipIds = [4,8,12,16,20]

state = None

#função para contar os dedos abertos na mão >=)
def count_fingers(image,hand_landmarks,handNo = 0):
    global state
    if hand_landmarks:
        landmarks = hand_landmarks[handNo].landmark
    #obter os pontos de referência da primeira mão visível 
        fingers = []
        for lm_index in tipIds :
            fingerTipY = landmarks [lm_index].y
            fingerBottomY = landmarks [lm_index -2].y
            thumbTipX = landmarks [4].x
            thumbBottomX = landmarks [2].x
            if lm_index != 4: 
                if fingerTipY < fingerBottomY:
                    fingers.append(1)
                if fingerTipY > fingerBottomY:
                    fingers.append(0)
            else:
                if thumbTipX < thumbBottomX:
                    fingers.append(1)
                if thumbTipX > thumbBottomX:
                    fingers.append(0)


        #contanto o total de dedos abertos
        total_fingers = fingers.count(1)
        # text = f"Dedos: {total_fingers}"
        # cv2.putText(image, text, (50,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 2)
   
        # play e pause
        #se o total de dedos for maior ou igual a 4 vou atualizar o estado para play
        if total_fingers >= 4 :
            state = 'play'
            
        #caso contrário, vou pressionar a tecla de espaço e mudar o estado para pause
        if total_fingers == 0 and state == 'play' :
            state = 'pause'
            keyboard.press(Key.space)
            print("Vídeo pausado")

        #next e previous
        fingertipX = (landmarks[0].x) * width
            
        #se o total de dedos for igual 1
        if total_fingers == 1:
            
        #verificar a posição do dedo indicador pressionar tecla de seta pra direita ou esquerda
            if fingertipX < width - 400:
                keyboard.press(Key.left)
                print("voltando")
        #dependendo da posição do dedo na tela
            if fingertipX > width - 50:
                keyboard.press(Key.right)
                print("avançando")


def drawHandLandmarks(image, hand_landmarks):
    if hand_landmarks:
        for landmarks in hand_landmarks:
            mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)
    #desenhe as conexões entre os pontos de referência

while True:
    success, frame = vid.read()

    frame = cv2.flip(frame,1)

    #Detectando os pontos de referência das mãos
    results = hands.process(frame)

    #Obtendo a posição do ponto de referência 
    hand_landmarks = results.multi_hand_landmarks

    #desenhando os pontos nas mãos
    drawHandLandmarks(frame,hand_landmarks )
    
    #contando os dedos
    count_fingers(frame,hand_landmarks)

    cv2.imshow("Maos",frame)

    key = cv2.waitKey(1)

    # 27 tecla esc
    # 32 tecla espaço
    if key == 27:
        break

cv2.destroAllWindows()
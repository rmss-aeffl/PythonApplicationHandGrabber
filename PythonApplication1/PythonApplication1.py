import cv2
import mediapipe as mp
import random

# Inicializa o MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Captura de vídeo
cap = cv2.VideoCapture(1)

# Configurações do jogo
cookie_radius = 20
cookie_color = (0, 255, 0)
cookie_position = (random.randint(50, 590), random.randint(50, 430))
score = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Inverte a imagem horizontalmente
    frame = cv2.flip(frame, 1)

    # Converte a imagem para RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Processa a imagem e detecta as mãos
    results = hands.process(image)

    # Converte a imagem de volta para BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Desenha as marcações das mãos na imagem
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Obtém a posição do ponto central da palma da mão
            palm_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * frame.shape[1])
            palm_y = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * frame.shape[0])
            
            # Verifica se a palma da mão está sobre o cookie
            if (cookie_position[0] - cookie_radius < palm_x < cookie_position[0] + cookie_radius and
                cookie_position[1] - cookie_radius < palm_y < cookie_position[1] + cookie_radius):
                score += 1
                cookie_position = (random.randint(50, 590), random.randint(50, 430))

    # Desenha o cookie
    cv2.circle(image, cookie_position, cookie_radius, cookie_color, -1)

    # Exibe a pontuação
    cv2.putText(image, f'Score: {score}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Exibe a imagem
    cv2.imshow('Cookie Catcher Game', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

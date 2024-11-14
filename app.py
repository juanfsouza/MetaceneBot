import cv2
import numpy as np
import pyautogui
import time

# Tempo mínimo entre cliques em segundos
min_click_interval = 2
last_click_time = 0

# Intervalo de cor para detectar números vermelhos (ajuste conforme necessário)
lower_red = np.array([0, 150, 150])  # Ajuste para capturar apenas vermelhos fortes
upper_red = np.array([10, 255, 255])

# Define uma região específica da tela para a detecção
region_top_left_x = 300
region_top_left_y = 300
region_width = 800
region_height = 400

# Contador de estabilidade para evitar falsos positivos
stability_counter = 0
stability_threshold = 3  # Número de frames consecutivos necessários para acionar

# Variáveis de controle para o loop de movimento
directions = ['w', 'd', 's', 'a']  # Sequência de teclas para movimento
current_direction_index = 0
movement_duration = 2  # Duração de cada movimento em segundos
rest_duration = 2  # Duração do tempo de descanso em segundos
pause_after_click_duration = 2  # Pausa de 2 segundos após o clique
movement_start_time = time.time()
is_moving = False  # Controle de estado de movimento
paused_after_click = False  # Controle para pausar após clicar

while True:
    # Captura a tela em tempo real, mas apenas a região definida
    screenshot = pyautogui.screenshot(region=(region_top_left_x, region_top_left_y, region_width, region_height))
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Aplicar desfoque para reduzir ruído
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)

    # Converte para HSV e cria uma máscara para a cor vermelha
    hsv_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
    mask_red = cv2.inRange(hsv_frame, lower_red, upper_red)

    # Exibe a máscara vermelha para diagnóstico
    cv2.imshow("Máscara Vermelha", mask_red)

    # Encontra contornos na máscara de cor vermelha
    contours, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    number_detected = False

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 300:  # Aumente o valor para focar apenas em áreas maiores
            x, y, w, h = cv2.boundingRect(contour)

            # Ajuste as proporções para algo mais típico de um número
            if 0.5 < h / w < 3.0:  # Proporção altura/largura mais estrita
                number_detected = True

                # Desenha um retângulo ao redor do número vermelho detectado para visualização
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "Número Vermelho Detectado", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                break  # Sai do loop após encontrar um número

    # Verifica estabilidade e aciona o comando apenas se detectado em múltiplos frames consecutivos
    if number_detected:
        stability_counter += 1
        if stability_counter >= stability_threshold:
            current_time = time.time()
            if current_time - last_click_time >= min_click_interval:
                # Realiza 6 cliques do botão esquerdo do mouse
                for _ in range(6):
                    pyautogui.click()
                print("Clicando 6 vezes com o botão esquerdo do mouse")

                # Solta a tecla atual e ativa a pausa após o clique
                pyautogui.keyUp(directions[current_direction_index])
                paused_after_click = True
                pause_start_time = current_time
                last_click_time = current_time
                stability_counter = 0  # Reseta o contador de estabilidade após acionar
            continue  # Pula o restante do loop se o número for detectado
    else:
        stability_counter = 0  # Reseta o contador se o número não for detectado

    # Controle de pausa após clicar
    if paused_after_click:
        # Verifica se passou o tempo de pausa após o clique
        if time.time() - pause_start_time >= pause_after_click_duration:
            paused_after_click = False  # Sai do estado de pausa após o clique
            movement_start_time = time.time()  # Reinicia o tempo para o próximo movimento
        continue  # Se ainda está pausado, pula para o próximo ciclo do loop

    # Controle de movimento com tempo de descanso
    current_time = time.time()
    if is_moving:
        # Se está se movendo e passou o tempo de movimento, para o movimento
        if current_time - movement_start_time >= movement_duration:
            pyautogui.keyUp(directions[current_direction_index])
            print(f"Soltando {directions[current_direction_index]}")
            is_moving = False  # Define como não está se movendo
            movement_start_time = current_time  # Reinicia o tempo para o descanso
    else:
        # Se não está se movendo e passou o tempo de descanso, inicia o próximo movimento
        if current_time - movement_start_time >= rest_duration:
            current_direction_index = (current_direction_index + 1) % len(directions)  # Passa para a próxima direção
            pyautogui.keyDown(directions[current_direction_index])
            print(f"Pressionando {directions[current_direction_index]}")
            is_moving = True  # Define como está se movendo
            movement_start_time = current_time  # Reinicia o tempo para o movimento

    # Exibe o frame processado em tempo real (opcional)
    cv2.imshow("Detecção de Número Vermelho", frame)

    # Pressione 'ESC' para sair
    if cv2.waitKey(1) & 0xFF == 27:  # 27 é o código ASCII para 'ESC'
        print("Encerrando o programa...")
        pyautogui.keyUp(directions[current_direction_index])  # Solta a tecla ao sair
        break

    # Pausa breve para reduzir o uso da CPU
    time.sleep(0.1)

cv2.destroyAllWindows()

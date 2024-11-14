# Automação de Detecção de Números Vermelhos com Movimento e Cliques Automáticos

Este script Python usa OpenCV e PyAutoGUI para detectar números vermelhos na tela e realizar movimentos e cliques automáticos em resposta. Quando um número vermelho é detectado, o script para o movimento atual, realiza 6 cliques com o botão esquerdo do mouse e pausa por 2 segundos antes de retomar o ciclo de movimento.

## Funcionalidades

- **Detecção de números vermelhos**: Detecta números vermelhos na tela usando detecção de cor.
- **Movimento automático**: Alterna automaticamente entre as teclas `W`, `D`, `S` e `A` em intervalos de 2 segundos, com uma pausa de 2 segundos entre cada movimento.
- **Interrupção com cliques**: Quando um número vermelho é detectado, o script para o movimento, realiza 6 cliques com o botão esquerdo do mouse e aguarda 2 segundos antes de retomar o movimento.

## Requisitos

- Python 3.x
- Bibliotecas Python:
  - `opencv-python`
  - `numpy`
  - `pyautogui`

Instale as dependências com o seguinte comando:


pip install opencv-python numpy pyautogui
Como Usar
Execute o script Python em um ambiente onde você pode capturar a tela.
O script irá alternar automaticamente entre as teclas de movimento W, D, S, A, com uma pausa entre cada tecla.
Se um número vermelho for detectado na tela, o movimento para e o script realiza 6 cliques do mouse. Após 2 segundos de pausa, o ciclo de movimento retoma.

Aqui está uma descrição detalhada de cada parte do código:

Imports e Configurações Iniciais
python
Copiar código
import cv2
import numpy as np
import pyautogui
import time
Esses módulos fornecem:

cv2: Funções para processamento de imagem usando OpenCV.
numpy: Operações matemáticas e manipulação de arrays.
pyautogui: Controle do teclado e do mouse para automação.
time: Controle de temporização para pausas e intervalos.
Variáveis de Tempo e Intervalo

min_click_interval = 2  # Tempo mínimo entre cliques consecutivos
last_click_time = 0  # Armazena o tempo do último clique
Essas variáveis controlam o intervalo mínimo entre as ações de clique do mouse.

Configuração da Cor Vermelha

lower_red = np.array([0, 150, 150])
upper_red = np.array([10, 255, 255])
Definimos o intervalo de cor em HSV para detectar tons fortes de vermelho.

Configuração da Região de Detecção e Controle de Movimento

region_top_left_x = 300
region_top_left_y = 300
region_width = 800
region_height = 400

directions = ['w', 'd', 's', 'a']  # Sequência de teclas de movimento
current_direction_index = 0  # Índice para controlar a tecla de movimento atual
movement_duration = 2  # Duração de cada movimento em segundos
rest_duration = 2  # Tempo de descanso entre movimentos
pause_after_click_duration = 2  # Pausa de 2 segundos após o clique
movement_start_time = time.time()  # Tempo de início do movimento
is_moving = False  # Indicador de estado de movimento
paused_after_click = False  # Indicador de pausa após o clique
Essas variáveis controlam a área da tela onde o script procura números vermelhos e o ciclo de movimento/pausa entre as teclas.

Lógica Principal do Script

while True:
O loop principal que captura a tela, processa a imagem, detecta números vermelhos, realiza cliques e alterna entre movimentos.

Captura de Tela e Conversão de Cor

screenshot = pyautogui.screenshot(region=(region_top_left_x, region_top_left_y, region_width, region_height))
frame = np.array(screenshot)
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
Captura a região definida da tela e converte a imagem para o formato RGB, necessário para a análise de cor.

Detecção de Cor e Máscara

hsv_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
mask_red = cv2.inRange(hsv_frame, lower_red, upper_red)
Cria uma máscara que isola áreas da imagem que estão dentro do intervalo de cor vermelha.

Detecção de Contornos e Verificação de Estabilidade

contours, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
Encontra contornos na máscara vermelha. A área de cada contorno é verificada para garantir que seja suficientemente grande para corresponder a um número vermelho.

Ciclo de Movimento e Pausa

if is_moving:
    # Se está se movendo e passou o tempo de movimento, para o movimento
    if current_time - movement_start_time >= movement_duration:
        pyautogui.keyUp(directions[current_direction_index])
        is_moving = False  # Define como não está se movendo
        movement_start_time = current_time  # Reinicia o tempo para o descanso
else:
    # Se não está se movendo e passou o tempo de descanso, inicia o próximo movimento
    if current_time - movement_start_time >= rest_duration:
        current_direction_index = (current_direction_index + 1) % len(directions)  # Próxima direção
        pyautogui.keyDown(directions[current_direction_index])
        is_moving = True  # Define como está se movendo
        movement_start_time = current_time  # Reinicia o tempo para o movimento
Alterna automaticamente entre as teclas W, D, S e A com 2 segundos de movimento seguidos por 2 segundos de descanso. Se um número vermelho é detectado, o movimento é interrompido.

Saída do Script

if cv2.waitKey(1) & 0xFF == 27:  # Pressione 'ESC' para sair
    pyautogui.keyUp(directions[current_direction_index])  # Solta a tecla ao sair
    break
Pressione ESC para encerrar o script. Isso libera a tecla de movimento atual e fecha todas as janelas.

Exemplo de Uso
Execute o script, que começará a detectar números vermelhos na tela e a realizar movimentos automáticos conforme descrito.


python nome_do_arquivo.py
Observações
Este script foi projetado para uso em um ambiente específico de jogo ou automação onde a detecção de números vermelhos e movimentos automáticos são necessários. Ajuste os parâmetros de cor e de intervalo de tempo conforme necessário para o seu caso.

Licença
Este projeto é distribuído sob a licença MIT.

Essa documentação cobre a estrutura e funcionalidade do script de forma detalhada. Ajuste o título e quaisquer seções adicionais conforme a sua preferência para o GitHub.

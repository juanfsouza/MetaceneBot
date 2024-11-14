import torch
import cv2
import os

# Carrega o modelo YOLOv5 pré-treinado
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Caminho do vídeo de entrada e do diretório para salvar frames e anotações
video_path = 'C:/Users/juan/Desktop/Auto/gravacao_jogo.avi'
output_dir = 'monster_detections'
os.makedirs(output_dir, exist_ok=True)

# Configuração para salvar os frames detectados e anotações
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Erro ao abrir o vídeo. Verifique o caminho.")
    exit()

frame_count = 0

# Dimensões da região central de exclusão (ajuste conforme necessário)
exclusion_center_ratio = 0.2  # Define a largura e altura da região como 20% do total da tela
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
exclusion_x_min = int((frame_width * (1 - exclusion_center_ratio)) / 2)
exclusion_x_max = int((frame_width * (1 + exclusion_center_ratio)) / 2)
exclusion_y_min = int((frame_height * (1 - exclusion_center_ratio)) / 2)
exclusion_y_max = int((frame_height * (1 + exclusion_center_ratio)) / 2)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Fim do vídeo ou erro de leitura do frame.")
        break

    # Converte o frame para o formato esperado pelo YOLO e realiza a detecção
    results = model(frame)

    # Processa as detecções
    detections = results.pandas().xyxy[0]  # Detecções em formato de DataFrame pandas

    # Filtra apenas as classes que você considera "monstros" e que estão fora da região de exclusão
    for idx, row in detections.iterrows():
        if row['confidence'] > 0.5:  # Ajuste a confiança mínima, se necessário
            # Obtém as coordenadas da caixa delimitadora
            x_min, y_min, x_max, y_max = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])

            # Ignora as detecções que estão dentro da região central de exclusão
            if (x_min > exclusion_x_min and x_max < exclusion_x_max and
                y_min > exclusion_y_min and y_max < exclusion_y_max):
                continue  # Ignora esta detecção e passa para a próxima

            # Desenha um retângulo ao redor do "monstro" detectado no frame
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            label = f"{row['name']} {row['confidence']:.2f}"
            cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Salva o frame com o "monstro" detectado
            output_frame_path = os.path.join(output_dir, f"frame_{frame_count}.jpg")
            cv2.imwrite(output_frame_path, frame)

            # Salva a anotação em um formato YOLO (TXT)
            annotation_path = os.path.join(output_dir, f"frame_{frame_count}.txt")
            with open(annotation_path, 'a') as f:
                # Converte as coordenadas para o formato YOLO
                center_x = (x_min + x_max) / 2 / frame.shape[1]
                center_y = (y_min + y_max) / 2 / frame.shape[0]
                width = (x_max - x_min) / frame.shape[1]
                height = (y_max - y_min) / frame.shape[0]
                class_id = 0  # ID da classe (você pode ajustar isso para diferentes tipos de monstros)

                # Salva a anotação no formato: <class_id> <center_x> <center_y> <width> <height>
                f.write(f"{class_id} {center_x} {center_y} {width} {height}\n")

    # Exibe o frame processado (opcional)
    cv2.imshow("Detecção de Monstros", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_count += 1

cap.release()
cv2.destroyAllWindows()

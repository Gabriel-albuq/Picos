import gxipy as gx
import sys
import cv2
import numpy as np
import time

class GxiCapture:
    def __init__(self, index=0):
        self.device_manager = gx.DeviceManager()
        self.dev_num, self.dev_info_list = self.device_manager.update_all_device_list()
        
        if self.dev_num == 0:
            print("Nenhuma câmera encontrada.")
            sys.exit(1)
        
        self.cam = self.device_manager.open_device_by_index(index)
        self.cam.TriggerMode.set(1)  # Colocar no modo Trigger para não sobrecarregar
        self.cam.ExposureTime.set(8000.0)  # Setando exposição
        self.cam.GainAuto.set(1)  # Ganho Automático (mas não contínuo)
        self.cam.DigitalShift.set(1)  # Aumento do brilho sem mudar abertura
        self.cam.SensorShutterMode.set(0)  # Setando como 0: Global para evitar distorção em movimento
        self.cam.BalanceWhiteAuto.set(1)  # Balanço de branco automático (mas não contínuo)

        # Melhorias na imagem
        self.gamma_lut = gx.Utility.get_gamma_lut(self.cam.GammaParam.get()) if self.cam.GammaParam.is_readable() else None
        self.contrast_lut = gx.Utility.get_contrast_lut(self.cam.ContrastParam.get()) if self.cam.ContrastParam.is_readable() else None
        self.color_correction_param = self.cam.ColorCorrectionParam.get() if self.cam.ColorCorrectionParam.is_readable() else 0
        
        self.cam.stream_on()
        self.default_size = (640, 480)  # Tamanho padrão caso não capture imagem

    def read(self):
        self.cam.TriggerSoftware.send_command()
        raw_image = self.cam.data_stream[0].get_image()
        
        if raw_image is None:
            #print("Erro: Nenhum frame recebido (timeout). Retornando imagem preta.")
            return False, np.zeros((self.default_size[1], self.default_size[0], 3), dtype=np.uint8)

        rgb_image = raw_image.convert("RGB")
        if rgb_image is None:
            #print("Erro: Imagem não convertida em RGB. Retornando imagem preta.")
            return False, np.zeros((self.default_size[1], self.default_size[0], 3), dtype=np.uint8)

        try:
            rgb_image.image_improvement(self.color_correction_param, self.contrast_lut, self.gamma_lut)
            numpy_image = rgb_image.get_numpy_array()
            numpy_image_bgr = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
            self.default_size = (numpy_image_bgr.shape[1], numpy_image_bgr.shape[0])  # Atualiza tamanho padrão
        except Exception as e:
            #print(f"Erro no processamento da imagem: {e}. Retornando imagem preta.")
            return False, np.zeros((self.default_size[1], self.default_size[0], 3), dtype=np.uint8)
        
        return True, numpy_image_bgr

    def release(self):
        self.cam.stream_off()
        self.cam.close_device()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    cap = GxiCapture(0)  # Inicializa a câmera no índice 0
    
    while True:
        time.sleep(0.01)
        ret, frame = cap.read()
        
        if ret:
            cv2.imshow("Imagem Capturada", frame)  # Exibe a imagem nas dimensões originais
        else:
            print("Falha ao capturar frame.")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

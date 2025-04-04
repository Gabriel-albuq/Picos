import os
import sys
import torch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.func import (
    device_config,
    device_start,
    device_start_capture,
    load_model,
    rules_detection,
    run_model,
    trigger_frame,
    trigger_test,
    start_application_interface
)


def start_application_without_interface():
    print('\n-------------- PICOS INICIADO --------------')

    linha = input('\nDigite a Linha: ')
    device_name = input('\nDigite o nome da Câmera/Vídeo: ')

    while True:
        device_path = str(
            input(
                'Digite o camninho para a Câmera ou Vídeo, ou digite None caso não tenha: '
            )
        )
        if device_path == 'None':
            device_path = None
            break
        elif device_path.isdigit():
            device_path = int(device_path)
            break
        else:
            break

    # Loop para garantir que a entrada seja 0 ou 1
    while True:
        option_visualize = input(
            'Deseja visualizar as predições? (Digite 0-Não ou 1-Sim): '
        )
        if option_visualize in ['0', '1']:
            break
        else:
            print('Por favor, digite apenas 0 ou 1.')
    option_visualize = int(option_visualize)

    return linha, device_name, device_path, option_visualize

if __name__ == '__main__':
    # Verificar se a GPU está disponível e configurar o dispositivo
    torch_device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'\nDispositivo de processamento utilizado: {torch_device}')

    current_directory = os.path.dirname(os.path.abspath(__file__))   # Diretório atual
    parent_directory = os.path.dirname(current_directory)   # Diretório pai (pasta acima)

    # Carregar modelo
    type_model = 'FRCNN_RN50'
    model = load_model(type_model)

    config_path = r'app\config.txt'

    # Iniciar a aplicação
    #linha, device_name,, device_path, option_visualize = start_application_without_interface()
    linha, device_name, device_path, option_visualize, exposure_value, perc_top, perc_bottom, \
            min_score, limit_center, save_dir, sec_run_model, wait_key = start_application_interface(config_path)

    # Caso seja uma câmera, converter em número
    try:
        device_path = int(device_path)  # Tenta converter para inteiro
    except ValueError:
        pass

    # Inicia o Device
    (
        device,
        device_fps,
        device_width,
        device_height,
        device_exposure,
    ) = device_start(device_name, device_path)

    device = device_config(
        device_name,
        device,
        device_fps,
        device_width,
        device_height,
        device_exposure,
    )

    device_start_capture(
        torch_device,
        device_name,
        device,
        device_fps,
        type_model,
        model,
        option_visualize,
        sec_run_model,
        perc_top,
        perc_bottom,
        wait_key,
        config_path,
        exposure_value,
        min_score,
        limit_center,
        save_dir,
        linha,
    )

﻿import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox

def load_settings(config_path):
    """Função para ler as configurações de um arquivo .txt e atribuir os valores diretamente às variáveis."""
    # Valores padrão para evitar NameError
    exposure_value = 0
    perc_top = 0.4
    perc_bottom = 0.8
    min_score = 0.5
    limit_center = 8
    sec_run_model = 0.4
    wait_key = 16  # Valor padrão
    save_dir = 'data\outputs\capturas'

    arquivo = config_path
    try:
        with open(arquivo, 'r') as file:
            for linha in file:
                # Ignora linhas vazias e comentários
                if linha.strip() and not linha.startswith('#'):
                    chave, valor = linha.split('=', 1)
                    chave = chave.strip()
                    valor = valor.strip()

                    # Atribui o valor diretamente à variável correspondente
                    if chave == 'exposure_value':
                        exposure_value = float(valor)  # Atribui diretamente
                    elif chave == 'perc_top':
                        perc_top = float(valor)
                    elif chave == 'perc_bottom':
                        perc_bottom = float(valor)
                    elif chave == 'min_score':
                        min_score = float(valor)
                    elif chave == 'limit_center':
                        limit_center = int(valor)
                    elif chave == 'sec_run_model':
                        sec_run_model = float(valor)
                    elif chave == 'wait_key':
                        wait_key = int(valor)  # Atribui diretamente
                    elif chave == 'save_dir':
                        save_dir = valor
    except Exception as e:
        print(f'Erro ao ler o arquivo: {e}')

    return (
        exposure_value,
        perc_top,
        perc_bottom,
        min_score,
        limit_center,
        sec_run_model,
        wait_key,
        save_dir,
    )


def save_settings(config_path, exposure_value, perc_top, 
                  perc_bottom, min_score, limit_center, sec_run_model, wait_key, save_dir):
    """Função para salvar as configurações atuais diretamente nas variáveis no arquivo .txt."""
    arquivo = config_path
    try:
        with open(arquivo, 'w') as file:
            file.write(f'exposure_value = {exposure_value}\n')
            file.write(f'perc_top = {perc_top}\n')
            file.write(f'perc_bottom = {perc_bottom}\n')
            file.write(f'min_score = {min_score}\n')
            file.write(f'limit_center = {limit_center}\n')
            file.write(f'sec_run_model = {sec_run_model}\n')
            file.write(f'wait_key = {wait_key}\n')
            
            # Verifica se o save_dir não é None antes de salvar
            if save_dir is not None:
                file.write(f'save_dir = {save_dir}\n')

        print('\nConfigurações salvas com sucesso.\n')
    except Exception as e:
        print(f'\nErro ao salvar as configurações: {e}\n')


def start_application_interface(config_path):
    global linha, device_name, device_path, option_visualize, exposure_value, perc_top, \
                perc_bottom, min_score, limit_center, save_dir, sec_run_model, wait_key
    (
        exposure_value,
        perc_top,
        perc_bottom,
        min_score,
        limit_center,
        sec_run_model,
        wait_key,
        save_dir,
    ) = load_settings(config_path)
    
    def submit():
        global linha, device_name, device_path, option_visualize, exposure_value, perc_top, \
                perc_bottom, min_score, limit_center, save_dir, sec_run_model, wait_key
        
        # Validação dos campos obrigatórios
        if not linha_entry.get():
            messagebox.showerror("Erro", "O campo 'Linha' não pode estar vazio.")
            return
        if not device_name_entry.get():
            messagebox.showerror("Erro", "O campo 'Nome da Câmera/Vídeo' não pode estar vazio.")
            return
        if not device_path_var.get():
            messagebox.showerror("Erro", "O campo 'Câmera/Vídeo' não pode estar vazio.")
            return
        if not exposure_value_entry.get():
            messagebox.showerror("Erro", "O campo 'Valor de exposição' não pode estar vazio.")
            return
        if not perc_top_entry.get():
            messagebox.showerror("Erro", "O campo 'Percentual Mínimo' não pode estar vazio.")
            return
        if not perc_bottom_entry.get():
            messagebox.showerror("Erro", "O campo 'Percentual Máximo' não pode estar vazio.")
            return
        if not min_score_entry.get():
            messagebox.showerror("Erro", "O campo 'Score Mínimo' não pode estar vazio.")
            return
        if not limit_center_entry.get():
            messagebox.showerror("Erro", "O campo 'Limite de centro' não pode estar vazio.")
            return
        if not sec_run_model_entry.get():
            messagebox.showerror("Erro", "O campo 'Segundos para rodar o modelo' não pode estar vazio.")
            return
        if not wait_key_entry.get():
            messagebox.showerror("Erro", "O campo 'Tempo de espera para tecla' não pode estar vazio.")
            return

        # Preenche as variáveis com os valores dos campos
        linha = linha_entry.get()
        device_name = device_name_entry.get()
        device_path = device_path_var.get()
        option_visualize = int(option_var.get())
        exposure_value = float(exposure_value_entry.get())
        perc_top = float(perc_top_entry.get())
        perc_bottom = float(perc_bottom_entry.get())
        min_score = float(min_score_entry.get())
        limit_center = int(limit_center_entry.get())
        sec_run_model = float(sec_run_model_entry.get())
        wait_key = int(wait_key_entry.get())
        
        # Verifica a opção de salvar detecções
        if not save_detection_var.get():  # Caso "Não salvar detecções" esteja marcado
            save_dir = save_dir_var.get()
        else:
            save_dir = None
            
        root.destroy()  # Fecha a janela após obter os valores
    
    def browse_file():
        filename = filedialog.askopenfilename()
        if filename:
            device_path_var.set(filename)
    
    def browse_save_dir():
        directory = filedialog.askdirectory()
        if directory:
            save_dir_var.set(directory)
    
    def toggle_save_dir(*args):
        """Habilita ou desabilita o campo de diretório de salvar baseado no checkbox."""
        if save_detection_var.get():
            save_dir_entry.config(state="disabled")  # Desabilita o campo de diretório
        else:
            save_dir_entry.config(state="normal")  # Habilita o campo de diretório
    
    root = tk.Tk()
    root.title("Configuração do PICOS")
    
    # Configuração do layout
    pad_x = 10
    pad_y = 5
    
    # Entrada para a linha
    tk.Label(root, text="Digite a linha:", anchor='w', width=30).grid(row=0, column=0, padx=pad_x, pady=pad_y, sticky='w')
    linha_entry = tk.Entry(root, width=30)
    linha_entry.grid(row=0, column=1, padx=pad_x, pady=pad_y)
    
    # Entrada para o nome da câmera/vídeo
    tk.Label(root, text="Nome da Câmera/Vídeo:", anchor='w', width=30).grid(row=1, column=0, padx=pad_x, pady=pad_y, sticky='w')
    device_name_entry = tk.Entry(root, width=30)
    device_name_entry.grid(row=1, column=1, padx=pad_x, pady=pad_y)
    
    # Entrada para o caminho do dispositivo
    tk.Label(root, text="Câmera/Vídeo:", anchor='w', width=30).grid(row=2, column=0, padx=pad_x, pady=pad_y, sticky='w')
    device_path_var = tk.StringVar()
    device_path_entry = tk.Entry(root, textvariable=device_path_var, width=30)
    device_path_entry.grid(row=2, column=1, padx=pad_x, pady=pad_y)
    
    # Botão para procurar um arquivo de vídeo
    tk.Button(root, text="Procurar", command=browse_file, width=10).grid(row=2, column=2, padx=pad_x, pady=pad_y)
    
    # Opção de visualização
    tk.Label(root, text="Visualizar predições:", anchor='w', width=30).grid(row=3, column=0, padx=pad_x, pady=pad_y, sticky='w')
    option_var = tk.StringVar(value=1)
    frame_options = tk.Frame(root)
    frame_options.grid(row=3, column=1, padx=pad_x, pady=pad_y, sticky='w')
    tk.Radiobutton(frame_options, text="Sim", variable=option_var, value="1").pack(side='left')
    tk.Radiobutton(frame_options, text="Não", variable=option_var, value="0").pack(side='left')
    
    # Diretório de salvar
    tk.Label(root, text="Salvar detecções em:", anchor='w', width=30).grid(row=4, column=0, padx=pad_x, pady=pad_y, sticky='w')
    save_dir_var = tk.StringVar()
    save_dir_entry = tk.Entry(root, textvariable=save_dir_var, width=30)
    save_dir_entry.grid(row=4, column=1, padx=pad_x, pady=pad_y)

    save_dir_var.set(save_dir)  # Preenche com o valor do config.txt
    tk.Button(root, text="Procurar", command=browse_save_dir, width=10).grid(row=4, column=2, padx=pad_x, pady=pad_y)

    # Caminho padrão abaixo do campo
    tk.Label(root, text="Caminho Padrão: data\\outputs\\capturas", anchor='w', width=30).grid(row=5, column=1, padx=pad_x, pady=pad_y, sticky='w')

    # Opção para "Não salvar detecções"
    save_detection_var = tk.BooleanVar(value=False)  # Inicia como "Não salvar"
    save_detection_checkbox = tk.Checkbutton(root, text="Não salvar detecções", variable=save_detection_var, command=toggle_save_dir)
    save_detection_checkbox.grid(row=6, column=1, padx=pad_x, pady=pad_y, sticky='w')

    # Parâmetros adicionais
    # Exposure value
    tk.Label(root, text="Valor de exposição:", anchor='w', width=30).grid(row=7, column=0, padx=pad_x, pady=pad_y, sticky='w')
    exposure_value_entry = tk.Entry(root, width=30)
    exposure_value_entry.grid(row=7, column=1, padx=pad_x, pady=pad_y)
    exposure_value_entry.insert(0, exposure_value)  # Preenche com o valor do config.txt
    
    # Percentual mínimo
    tk.Label(root, text="Percentual Mínimo:", anchor='w', width=30).grid(row=8, column=0, padx=pad_x, pady=pad_y, sticky='w')
    perc_top_entry = tk.Entry(root, width=30)
    perc_top_entry.grid(row=8, column=1, padx=pad_x, pady=pad_y)
    perc_top_entry.insert(0, perc_top)  # Preenche com o valor do config.txt
    
    # Percentual máximo
    tk.Label(root, text="Percentual Máximo:", anchor='w', width=30).grid(row=9, column=0, padx=pad_x, pady=pad_y, sticky='w')
    perc_bottom_entry = tk.Entry(root, width=30)
    perc_bottom_entry.grid(row=9, column=1, padx=pad_x, pady=pad_y)
    perc_bottom_entry.insert(0, perc_bottom)  # Preenche com o valor do config.txt
    
    # Score mínimo
    tk.Label(root, text="Score Mínimo:", anchor='w', width=30).grid(row=10, column=0, padx=pad_x, pady=pad_y, sticky='w')
    min_score_entry = tk.Entry(root, width=30)
    min_score_entry.grid(row=10, column=1, padx=pad_x, pady=pad_y)
    min_score_entry.insert(0, min_score)  # Preenche com o valor do config.txt
    
    # Limite de centro
    tk.Label(root, text="Limite de centro:", anchor='w', width=30).grid(row=11, column=0, padx=pad_x, pady=pad_y, sticky='w')
    limit_center_entry = tk.Entry(root, width=30)
    limit_center_entry.grid(row=11, column=1, padx=pad_x, pady=pad_y)
    limit_center_entry.insert(0, limit_center)  # Preenche com o valor do config.txt
    
    # Adicionando os novos campos
    # Segundos para rodar o modelo
    tk.Label(root, text="Segundos para rodar o modelo:", anchor='w', width=30).grid(row=12, column=0, padx=pad_x, pady=pad_y, sticky='w')
    sec_run_model_entry = tk.Entry(root, width=30)
    sec_run_model_entry.grid(row=12, column=1, padx=pad_x, pady=pad_y)
    sec_run_model_entry.insert(0, sec_run_model)  # Preenche com o valor do config.txt
    
    # Tempo de espera para tecla
    tk.Label(root, text="Tempo de espera para tecla:", anchor='w', width=30).grid(row=13, column=0, padx=pad_x, pady=pad_y, sticky='w')
    wait_key_entry = tk.Entry(root, width=30)
    wait_key_entry.grid(row=13, column=1, padx=pad_x, pady=pad_y)
    wait_key_entry.insert(0, wait_key)  # Preenche com o valor do config.txt
    
    # Botão de confirmação
    tk.Button(root, text="Confirmar", command=submit, width=20).grid(row=14, column=0, columnspan=4, pady=10)
    
    # Chama a função para ajustar o estado do diretório de salvar
    toggle_save_dir()
    
    root.mainloop()
    print(save_dir)
    save_settings(config_path, exposure_value, perc_top, perc_bottom,
                    min_score, limit_center, sec_run_model, wait_key, save_dir) 
    
    return linha, device_name, device_path or None, option_visualize, exposure_value, perc_top, perc_bottom, \
            min_score, limit_center, save_dir, sec_run_model, wait_key


if __name__ == '__main__':
    # Exemplo de chamada da função
    linha, device_name, device_path, option_visualize, exposure_value, perc_top, perc_bottom, min_score, limit_center, sec_run_model, wait_key, save_dir = start_application_interface()
    # print("Linha:", linha)
    # print("Nome da Câmera/Vídeo:", device_name)
    # print("Caminho do dispositivo:", device_path)
    # print("Visualizar predições:", option_visualize)
    # print("Exposição:", exposure_value)
    # print("Percentual Mínimo:", perc_top)
    # print("Percentual Máximo:", perc_bottom)
    # print("Score Mínimo:", min_score)
    # print("Limite de centro:", limit_center)
    # print("Diretório de salvar:", save_dir if save_dir else "Não salvar detecções")

# 🛠️ Como Usar o PICOS

Este guia descreve como utilizar a **Plataforma Inteligente de Contagem de Objetos Selecionados (PICOS)** para realizar a contagem de biscoitos em imagens.

## 🚀 Passos para Utilização

### 1. Clonando o Repositório

Primeiro, clone o repositório do projeto:

```bash
git clone https://github.com/seu-usuario/picos.git
cd picos
```

### 2. Instalando Dependências
    
Para instalar as dependências necessárias, execute o seguinte comando:

```bash
poetry install
```

### 3. Parâmetros Configuráveis
    
Os parâmetros configuráveis estão no arquivo `app/config.txt`, mas podem ser alterado no inicio da aplicação, seja na interface ou já dentro da própria câmera.
Sempre que a a detecção para de OFF para ON, os parâmetros atuais são salvos no arquivo `app/config.txt`, para que quando o aplicativo seja iniciado, as últimas configurações sejam carregadas.

- **exposure_value** = `0`  
  *Exposição da câmera* (pode ser alterado quando a câmera estiver aberta).

- **perc_min** = `0.4`  
  *Posição da linha superior do trigger* (pode ser alterado quando a câmera estiver aberta).

- **perc_max** = `0.8`  
  *Posição da linha inferior do trigger* (pode ser alterado quando a câmera estiver aberta).

- **min_score** = `0.5`  
  *Mínimo de certeza para considerar um objeto como válido*.

- **limit_center** = `8`  
  *Tamanho do círculo ao redor do centro da marcação onde as sobreposições serão desconsideradas*.

- **save_dir** = `data/outputs/capturas`  
  *Pasta onde as detecções serão salvas*.

### 2. Uso

Para rodar o **PICOS**, execute o seguinte comando:

```bash
python app/run_picos.py
```
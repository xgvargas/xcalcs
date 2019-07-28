# XCalcS

RPN calculator in Python3 and PySide

## Instalando o Pyside no linux

Instalar via `pip` falha miseravelmente. Ele só no 3.4.

O jeito mais facil de fazer isso funcionar e´ instalar o pyside no python3 global com o `apt`, e quando criar o virtualenv do projeto usar a chave `--system-site-packages`.

```bash

# basicao para compilar coisas....
sudo apt install build-essential

# instala o pip caso nao exista
sudo apt install python-pip  python-virtualenv

# se resolver compilar o python do zero instale isso
sudo apt install zlib1g-dev
sudo apt install libssl-dev
sudo apt install cmake

# instala o pyside pre compilado
sudo apt install python3-pyside

# instalar compilador de ui, de recursos e linguagem do pyside
sudo apt install pyside-tools qt4-linguist-tools qt4-dev-tools qt4-designer

# criar o virtual env e instalar coisas nele
virtualenv --system-site-packages -p python3 venv
source venv/bin/activate
pip install -r requirements.txt

#  precisa instalar o helper para gerar os graficos
yarn global add svg-mask2png

# preparar para executar
make images
make

# o comando abaixo atualiza a base de traducao caso edite os textos no fonte
make update

# se for usar o cx_freeze precisa do python.h
sudo apt install python3-dev
```

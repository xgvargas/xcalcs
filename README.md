# XCalcS

RPN calculator in Python3 and PySide

## Instalando o Pyside no linux

Instalar via `pip` falha miseravelmente. Alem disso ele não instala no python3.5 somente no 3.4

O jeito mais facil de fazer isso funcionar e´ instalar o pyside no python3 global com o apt-get, e quando criar o virtualenv do porjeto usar a chave `--system-site-packages`.

```bash

# basicao para compilar coisas....
sudo apt-get install build-essential

# instala o pip caso nao exista
sudo apt-get install python-pip  python-virtualenv

# se resolver compilar o python do zero instale isso
sudo apt-get install zlib1g-dev
sudo apt-get install libssl-dev
sudo apt-get install cmake

# instala o pyside pre compilado
sudo apt-get install python3-pyside

# instalar compilador de ui, de recursos e linguage do pyside
sudo apt-get install pyside-tools

# instala uma versao do designer, mas no mint ele ja estava la com o nome: designer
sudo apt-get install qt4-designer
``` 

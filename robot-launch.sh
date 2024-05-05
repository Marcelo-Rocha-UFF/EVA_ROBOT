#!/bin/bash

# Ativa o ambiente virtual do EVA
source /home/pi/EVA_ROBOT/venv/bin/activate

# Esse comando é necessário para que a interface gráfica (display) do robô possa ser executada via linha de comando.
export DISPLAY=:0.0

# Executa a aplicação Web que permite executar e "matar" os módulos do EVA.
# A aplicação pode ser acessada pelo IP do Raspberry, na porta 5000.
python3 /home/pi/EVA_ROBOT/robot-system-web-run.py
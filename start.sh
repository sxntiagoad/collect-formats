#!/bin/bash

# Iniciar Xvfb
Xvfb :0 -screen 0 1024x768x16 &
sleep 5

# Configurar Wine
export WINEARCH=win64
export WINEPREFIX=/root/.wine
export DISPLAY=:0

# Iniciar wineserver
wineserver -p

# Esperar a que Wine esté listo
sleep 10

# Iniciar la aplicación Flask
exec gunicorn run:app --bind 0.0.0.0:$PORT

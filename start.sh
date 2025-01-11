#!/bin/bash

# Iniciar Xvfb
Xvfb :0 -screen 0 1024x768x16 &

# Esperar a que Xvfb esté listo
sleep 5

# Iniciar la aplicación Flask
gunicorn --bind 0.0.0.0:5000 run:app

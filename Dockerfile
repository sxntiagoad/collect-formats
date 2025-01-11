FROM ubuntu:20.04

# Evitar interacciones durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip \
    wine64 \
    wget \
    unzip \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Configurar Wine
ENV WINEARCH=win64
ENV WINEPREFIX=/root/.wine
ENV DISPLAY=:0

# Instalar Office Runtime (necesario para Excel)
RUN wget https://download.microsoft.com/download/2/7/A/27AF1BE6-DD20-4CB4-B154-EBAB8A7D4A7E/officedeploymenttool_14326-20404.exe \
    && wine officedeploymenttool_14326-20404.exe /quiet /norestart \
    && rm officedeploymenttool_14326-20404.exe

# Configurar el directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Instalar dependencias de Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Exponer el puerto (Railway lo sobreescribirá con PORT)
ENV PORT=5000
EXPOSE $PORT

# Usar el Procfile
CMD gunicorn run:app --bind 0.0.0.0:$PORT

FROM ubuntu:20.04

# Evitar interacciones durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias necesarias
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y \
    python3.9 \
    python3-pip \
    wget \
    xvfb \
    winbind \
    cabextract \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Instalar Wine
RUN wget -nv -O- https://dl.winehq.org/wine-builds/winehq.key | APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1 apt-key add - \
    && add-apt-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ focal main' \
    && apt-get update \
    && apt-get install -y --install-recommends winehq-stable

# Configurar Wine
ENV WINEARCH=win64
ENV WINEPREFIX=/root/.wine
ENV DISPLAY=:0

# Instalar winetricks y configurar .NET Framework
RUN wget https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks \
    && chmod +x winetricks \
    && mv winetricks /usr/local/bin \
    && winetricks -q dotnet48

# Configurar el directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Descargar e instalar Office
RUN mkdir -p /tmp/office && cd /tmp/office \
    && wget https://download.microsoft.com/download/2/7/A/27AF1BE6-DD20-4CB4-B154-EBAB8A7D4A7E/officedeploymenttool_16026-20170.exe \
    && wine officedeploymenttool_16026-20170.exe /quiet /extract:/tmp/office \
    && wine setup.exe /configure /app/configuration.xml \
    && cd / && rm -rf /tmp/office

# Instalar dependencias de Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Exponer el puerto (Railway lo sobreescribirá con PORT)
ENV PORT=5000
EXPOSE $PORT

# Script de inicio personalizado
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]

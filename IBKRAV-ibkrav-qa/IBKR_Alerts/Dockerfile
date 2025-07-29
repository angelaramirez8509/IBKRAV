# Usa imagen oficial de Python 3.10 slim
FROM python:3.10-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar librerías del sistema necesarias para ib_insync y dependencias
RUN apt-get update && \
    apt-get install -y build-essential libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 libxss1 libasound2 libxtst6 libatk1.0-0 libgtk-3-0 wget && \
    rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Exponer puerto si se requiere (opcional)
# EXPOSE 8080

# Comando por defecto para ejecución
CMD ["python", "src/main.py"]

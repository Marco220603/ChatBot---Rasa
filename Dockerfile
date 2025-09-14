# Dockerfile (Rasa Core)
FROM rasa/rasa:3.6.20-full

WORKDIR /app

# Copia SOLO el contenido de la carpeta Chatbot dentro de /app
COPY ./Chatbot/ .

EXPOSE 5005


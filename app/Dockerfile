FROM python:3.11-slim

WORKDIR /app .

COPY requirements.txt .
COPY run-ollama.sh .

RUN pip install --no-cache-dir -r requirements.txt

COPY wizard_bot.py .

# Install Ollama via official script
RUN apt-get update && apt-get install -y curl zstd
RUN curl -fsSL https://ollama.com/install.sh | sh

# Download llm
RUN chmod +x run-ollama.sh && ./run-ollama.sh

# Expose port
EXPOSE 11434

# Set entrypoint to start the server
#ENTRYPOINT ["ollama", "serve"]

CMD ["python", "wizard_bot.py"]
#CMD ["sh", "-c", "python wizard_bot.py && ollama serve &"]

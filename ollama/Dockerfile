FROM ollama/ollama:latest

RUN apt-get update && apt-get install -y curl && apt-get clean

COPY start.sh /start.sh
RUN chmod +x /start.sh

ENTRYPOINT ["/start.sh"]

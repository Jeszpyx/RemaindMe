#!/bin/sh

echo "⏳ Waiting for Ollama server on http://127.0.0.1:11434..."

ollama serve &

# Ждём запуска API
until curl -sSf http://127.0.0.1:11434/api/tags >/dev/null; do
  sleep 1
  echo "⌛ Still waiting for Ollama server..."
done

echo "✅ Ollama is up, pulling model: $OLLAMA_MODEL"
ollama pull "$OLLAMA_MODEL"

wait

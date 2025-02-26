#!/bin/bash

# Переменные по умолчанию
HOST=${HOST:-"127.0.0.1"}
PORT=${PORT:-"8000"}

run() {
    echo "Running application on $HOST:$PORT..."
    poetry run uvicorn main:app --host "$HOST" --port "$PORT" --reload
}



help() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  run                 Run the application using uvicorn"
    echo "  help                Show this help message"
}

# Определение команды
case "$1" in
    run) run ;;
    help|*) help ;;
esac

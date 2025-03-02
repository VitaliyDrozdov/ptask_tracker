#!/bin/bash

# Переменные по умолчанию
HOST=${HOST:-"127.0.0.1"}
PORT=${PORT:-"8000"}
APP_ENV=${APP_ENV:-"dev"}

run() {
    echo "Running application in $APP_ENV mode on $HOST:$PORT..."
    ENV_FILE="$APP_ENV.env"
    if [[ -f "$ENV_FILE" ]]; then
        echo "Loading environment variables from $ENV_FILE"
        export $(grep -v '^#' "$ENV_FILE" | xargs)
    else
        echo "⚠️ Warning: Environment file '$ENV_FILE' not found!"
    fi


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

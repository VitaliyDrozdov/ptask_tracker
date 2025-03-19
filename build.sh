#!/bin/bash

# Переменные по умолчанию
HOST=${HOST:-"127.0.0.1"}
PORT=${PORT:-"8000"}
APP_ENV=${APP_ENV:-"dev"}

run() {
    echo "Running application in $APP_ENV mode on $HOST:$PORT..."
    ENV_FILE=".env.$APP_ENV"
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
    echo "  init_migrations     Create Alembic migrations"
    echo "  migrate             Apply Alembic migrations"
    echo "  help                Show this help message"
}

init_migrations() {
    echo "Initializing migrations for $APP_ENV environment..."

    if [[ "$APP_ENV" == "prod" ]]; then
        echo "Initializing async migrations for production..."
        poetry run alembic init -t async migrations_async
    elif [[ "$APP_ENV" == "dev" ]]; then
        echo "Initializing migrations for development..."
        poetry run alembic init migrations
    else
        echo "⚠️ Unknown environment! Please set APP_ENV to 'dev' or 'prod'."
        exit 1
    fi
}

migrate() {
    echo "Running migrations in $APP_ENV mode..."
    ENV_FILE=".env.$APP_ENV"
    if [[ -f "$ENV_FILE" ]]; then
        echo "Loading environment variables from $ENV_FILE"
        export $(grep -v '^#' "$ENV_FILE" | xargs)
    else
        echo "⚠️ Warning: Environment file '$ENV_FILE' not found!"
    fi

    # Применение миграций Alembic
    echo "Applying Alembic migrations..."
    poetry run alembic upgrade head
}

# Определение команды
case "$1" in
    run) run ;;
    init_migrations) init_migrations ;;
    migrate) migrate ;;
    help|*) help ;;
esac

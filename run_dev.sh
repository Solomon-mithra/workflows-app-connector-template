#!/bin/bash

# Parse command line arguments
REBUILD=false
for arg in "$@"; do
  if [ "$arg" == "--build" ]; then
    REBUILD=true
  fi
done

# Print Stacksync branding
echo -e "\033[1;36m"
echo "  ____  _             _                           "
echo " / ___|| |_ __ _  ___| | _____ _   _ _ __   ___  "
echo " \___ \| __/ _\` |/ __| |/ / __| | | | '_ \ / __| "
echo "  ___) | || (_| | (__|   <\__ \ |_| | | | | (__  "
echo " |____/ \__\__,_|\___|_|\_\___/\__, |_| |_|\___| "
echo "                               |___/             "
echo -e "\033[0m"
echo -e "\033[1;32mApp Connector Public Module\033[0m"
echo -e "\033[0;34mDocumentation: https://docs.stacksync.com/workflows/app-connector\033[0m"
echo ""

# Ensure config directory exists
if [ ! -d "config" ]; then
  echo "Creating config directory..."
  mkdir -p config
fi

# Read port from app_config.yaml
DEFAULT_PORT=2003
if command -v grep >/dev/null && command -v awk >/dev/null && [ -f "app_config.yaml" ]; then
  PORT=$(grep -A10 "local_development_settings:" app_config.yaml | grep "port:" | awk '{print $2}' | tr -d '[:space:]')
  if [ -z "$PORT" ]; then
    PORT=$DEFAULT_PORT
    echo "No port specified in app_config.yaml. Using default port: $PORT"
  else
    echo "Using port from app_config.yaml: $PORT"
  fi
else
  PORT=$DEFAULT_PORT
  echo "Could not read app_config.yaml. Using default port: $PORT"
fi

# Determine the location of Dockerfile.dev
DOCKERFILE_PATH="config/Dockerfile.dev"
if [ ! -f "$DOCKERFILE_PATH" ] && [ -f "Dockerfile.dev" ]; then
  DOCKERFILE_PATH="Dockerfile.dev"
  echo "Using Dockerfile.dev from main directory"
else
  echo "Using Dockerfile.dev from config directory"
fi

# Get the repository name from the current directory
REPO_NAME=$(basename "$PWD")
REPO_NAME=${REPO_NAME#workflows-} # Remove 'workflows-' prefix if present
APP_NAME="workflows-app-${REPO_NAME}"

echo "Preparing ${APP_NAME}..."

# Check if the image exists
IMAGE_EXISTS=$(docker images -q ${APP_NAME} 2> /dev/null)

# Build if image doesn't exist or --rebuild flag is set
if [ -z "$IMAGE_EXISTS" ] || [ "$REBUILD" == "true" ]; then
  if [ "$REBUILD" == "true" ]; then
    echo "Forcing rebuild of Docker image: ${APP_NAME}"
    docker build --no-cache -t ${APP_NAME} -f ${DOCKERFILE_PATH} .
  else
    echo "Docker image not found. Building: ${APP_NAME}"
    docker build -t ${APP_NAME} -f ${DOCKERFILE_PATH} .
  fi
else
  echo "Docker image ${APP_NAME} already exists. Skipping build."
  echo "Use --build flag to force a rebuild."
fi

# Load .env file if it exists
if [ -f .env ]; then
  echo "Loading environment variables from .env file..."
  set -o allexport
  source .env
  set +o allexport
fi

# Determine OS type and run container
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "windows" ]]; then
    # Windows - using Command Prompt or PowerShell
    echo "Detected Windows environment"
    echo "Starting container on port ${PORT}..."
    docker run --rm -p ${PORT}:${PORT} -it -e ENVIRONMENT=dev -e REGION=besg -e GOOGLE_SERVICE_ACCOUNT_JSON -e GOOGLE_SHEETS_API_KEY --name=${APP_NAME} -v ${PWD}:/usr/src/app/ ${APP_NAME}
else
    # Unix/Mac environment
    echo "Detected Unix/Mac environment"
    echo "Starting container on port ${PORT}..."
    docker run --rm -p ${PORT}:${PORT} -it -e ENVIRONMENT=dev -e REGION=besg -e GOOGLE_SERVICE_ACCOUNT_JSON -e GOOGLE_SHEETS_API_KEY --name=${APP_NAME} -v $PWD:/usr/src/app/ ${APP_NAME}
fi
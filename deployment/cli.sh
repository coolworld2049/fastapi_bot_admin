#!/usr/bin/env bash

ENV_FILE_PATH=../src/bot_admin_service/.env
source ${ENV_FILE_PATH}

project_name=${PROJECT_NAME?env PROJECT_NAME required}
compose_file=docker-compose.yml

install() {
  docker-compose -p "$project_name" -f "$compose_file" up -d ngrok
  echo "Please enter ngrok https endpoint url (https://dashboard.ngrok.com/cloud-edge/endpoints):"
  read webhook_endpoint
  docker-compose -p "$project_name" -f "$compose_file" up -d postgresql
  WEBHOOK_ENDPOINT=${webhook_endpoint} docker-compose -p "$project_name" -f "$compose_file" up -d bot_admin_service
  docker-compose -p "$project_name" -f "$compose_file" up -d bot_admin_frontend

}

delete() {
  docker-compose -p "$project_name" -f "$compose_file" down --rmi local --remove-orphans
}

print_usage() {
  echo "Usage: $0 [OPTION]"
  echo "Options:"
  echo "  install           Bring up containers using Docker Compose"
  echo "  delete            Remove containers, images"
  echo "  --help            Display this help message"
}

# Parse command-line options
if [[ $# -eq 0 ]]; then
  print_usage
  exit 1
fi

case $1 in
install)
  install
  ;;
delete)
  delete
  ;;
--help)
  print_usage
  ;;
*)
  echo "Invalid option: $1"
  print_usage
  exit 1
  ;;
esac

#!/usr/bin/env bash

ENV_FILE_PATH=../src/bot_admin_service/.env
source ${ENV_FILE_PATH}

install() {
  docker-compose  up -d ngrok
  echo "Please enter ngrok https endpoint url (https://dashboard.ngrok.com/cloud-edge/endpoints):"
  read webhook_endpoint
  docker-compose  up -d postgresql
  WEBHOOK_ENDPOINT=${webhook_endpoint} docker-compose  up -d bot_admin_service
  docker-compose  up -d bot_admin_frontend

}

delete() {
  docker-compose down --rmi local --remove-orphans
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

#!/bin/bash
# Next.js utility script

# Function to create a new Next.js page
create_page() {
  local page_path=$1
  local page_dir

  if [[ "$page_path" == *"/"* ]]; then
    page_dir=$(dirname "pages/$page_path")
    mkdir -p "$page_dir"
    touch "pages/$page_path.js"
  else
    touch "pages/$page_path.js"
  fi

  echo "Created page: pages/$page_path.js"
}

# Function to create a new API route
create_api_route() {
  local route_path=$1
  local api_dir

  if [[ "$route_path" == *"/"* ]]; then
    api_dir=$(dirname "pages/api/$route_path")
    mkdir -p "$api_dir"
    touch "pages/api/$route_path.js"
  else
    mkdir -p "pages/api"
    touch "pages/api/$route_path.js"
  fi

  echo "Created API route: pages/api/$route_path.js"
}

# Function to check if in a Next.js project
check_nextjs_project() {
  if [[ ! -f "package.json" ]]; then
    echo "Error: Not in a Next.js project (package.json not found)"
    exit 1
  fi

  if ! grep -q "next" package.json; then
    echo "Error: Not in a Next.js project (next not found in package.json)"
    exit 1
  fi
}

# Main script
case $1 in
  "create-page")
    check_nextjs_project
    if [ -z "$2" ]; then
      echo "Usage: $0 create-page <page-name>"
      exit 1
    fi
    create_page "$2"
    ;;
  "create-api")
    check_nextjs_project
    if [ -z "$2" ]; then
      echo "Usage: $0 create-api <api-route-name>"
      exit 1
    fi
    create_api_route "$2"
    ;;
  *)
    echo "Usage: $0 {create-page|create-api} <name>"
    echo "  create-page: Create a new Next.js page"
    echo "  create-api: Create a new API route"
    exit 1
    ;;
esac
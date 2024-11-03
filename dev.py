import subprocess
import os
import json
import getpass
import yaml
import logging
from datetime import datetime

# Constants
OUTPUT_DIR = "/tmp/output"
LOG_DIR = "/tmp/logs"
LOGIN_SCRIPT = "./"
LIST_PRODUCTS_SCRIPT = ".
GET_SWAGGER_SCRIPT = "."
API_PUSH_URL = ""
HEADERS = {
  
}

# Configure logging
os.makedirs(LOG_DIR, exist_ok=True)
log_filename = os.path.join(LOG_DIR, f"swagger_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_filename)
    ]
)

def run_command(command, success_msg, error_msg, capture_output=False):
    """Runs a shell command with optional output capturing."""
    try:
        result = subprocess.run(
            ["sudo"] + command,
            check=True,
            capture_output=capture_output,
            text=True
        )
        if success_msg:
            logging.info(success_msg)
        return result
    except subprocess.CalledProcessError as e:
        logging.error(f"{error_msg}: {e}")
        if capture_output:
            logging.error(e.stderr)
        exit(1)

def setup_output_directory():
    """Ensures the output directory exists."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    logging.info(f"Created output directory at {OUTPUT_DIR}")

def login(env, username, password):
    """Logs into the environment using the login script."""
    run_command(
        [LOGIN_SCRIPT, env, username, password],
        "Login successful.",
        "Error during login"
    )

def list_products(env, catalog, space):
    """Runs the product listing script and generates a product list YAML."""
    run_command(
        [LIST_PRODUCTS_SCRIPT, env, OUTPUT_DIR, "0", catalog, space],
        "Product list downloaded successfully.",
        "Error downloading product list"
    )

def load_product_list():
    """Loads the product list from the latest YAML file in the output directory."""
    yaml_files = sorted(
        [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".yaml")],
        key=lambda x: os.path.getmtime(os.path.join(OUTPUT_DIR, x)),
        reverse=True
    )
    if not yaml_files:
        logging.error("Error: No YAML files found in the output directory.")
        return None

    latest_file = os.path.join(OUTPUT_DIR, yaml_files[0])
    logging.info(f"Using product list file: {latest_file}")

    with open(latest_file, 'r') as f:
        data = yaml.safe_load(f) or {}
        if not data:
            logging.error("Error: Product list is empty or could not be loaded properly.")
            return None
        return data

def download_swagger(env, catalog, product_list):
    """Downloads and saves Swagger files for each API in the product list."""
    for product in product_list.get('results', []):
        product_name = product.get('name')
        for plan in product.get('plans', []):
            plan_name = plan.get('name')
            for api in plan.get('apis', []):
                name = api.get('name')
                version = api.get('version')
                
                if name and version:
                    logging.info(f"Downloading Swagger for {name}:{version} under product {product_name} and plan {plan_name}")

                    get_swagger_command = [GET_SWAGGER_SCRIPT, env, f"{name}:{version}", catalog, OUTPUT_DIR]
                    result = run_command(
                        get_swagger_command,
                        None,
                        f"Error downloading Swagger for {name}:{version}",
                        capture_output=True
                    )

                    if result and result.stdout:
                        save_swagger_file(name, version, result.stdout)
                    else:
                        logging.warning(f"No Swagger content found for {name}:{version}")

def save_swagger_file(name, version, content):
    """Saves Swagger content to a JSON file."""
    swagger_output_file = os.path.join(OUTPUT_DIR, f"{name}_{version}.json")
    try:
        with open(swagger_output_file, 'w') as output_file:
            output_file.write(content)
        logging.info(f"Swagger successfully saved to {swagger_output_file}")
    except Exception as e:
        logging.error(f"Failed to save Swagger for {name}:{version} - {e}")

def main():
    setup_output_directory()

    env = input("Enter environment (e.g., dev, prod): ")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    catalog = input("Enter catalog name: ")
    space = input("Enter space name: ")

    login(env, username, password)
    list_products(env, catalog, space)

    product_list = load_product_list()
    if not product_list:
        logging.error("Exiting due to empty or invalid product list.")
        exit(1)

    download_swagger(env, catalog, product_list)
    logging.info("Completed all operations successfully.")

if __name__ == "__main__":
    main()

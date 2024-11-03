import subprocess
import os
import json
import getpass
import yaml
import logging
from glob import glob
from datetime import datetime

# Constants
OUTPUT_DIR = "/tmp/output"
LOG_DIR = "/tmp/logs"



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

def find_latest_yaml_file():
    """Finds the latest YAML file in the output directory."""
    yaml_files = glob(os.path.join(OUTPUT_DIR, "*.yaml"))
    if not yaml_files:
        logging.error("Error: No YAML files found in the output directory.")
        return None
    latest_file = max(yaml_files, key=os.path.getctime)
    logging.info(f"Using product list file: {latest_file}")
    return latest_file

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
    file_path = find_latest_yaml_file()
    if not file_path:
        logging.error("Exiting due to missing product list file.")
        exit(1)

    with open(file_path, 'r') as f:
        data = yaml.safe_load(f) or {}
        if not data:
            logging.error("Error: Product list is empty or could not be loaded properly.")
            return None
        return data

def download_and_save_swagger(env, catalog, name, version):
    """Downloads and saves Swagger content to a file."""
    logging.info(f"Downloading Swagger for {name}:{version}")
    get_swagger_command = [GET_SWAGGER_SCRIPT, env, f"{name}:{version}", catalog]
    result = run_command(
        get_swagger_command,
        None,
        f"Error downloading Swagger for {name}:{version}",
        capture_output=True
    )

    if result and result.stdout:
        swagger_content = result.stdout.strip()
        swagger_output_file = os.path.join(OUTPUT_DIR, f"{name}_{version}.json")
        
        with open(swagger_output_file, 'w') as output_file:
            output_file.write(swagger_content)
        
        logging.info(f"Swagger saved to {swagger_output_file}")
        return swagger_output_file
    else:
        logging.warning(f"No Swagger content found for {name}:{version}")
        return None

def load_swagger_file(swagger_file):
    """Loads and parses Swagger content from a saved file."""
    try:
        with open(swagger_file, 'r') as f:
            swagger_json = json.load(f)
            basepath = swagger_json.get("basePath", "")
            return swagger_json, basepath
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logging.error(f"Failed to load or parse Swagger file {swagger_file}: {e}")
        return None, None

def push_to_database(product, plan, swagger_content, basepath):
    """Formats data and pushes it to the database using a POST request."""
    data = {
        "prod_name": product['name'],
        "prod_title": product['title'],
        "prod_state": product['state'],
        "prod_version": product['version'],
        "env": product['env'],
        "space": product['space'],
        "org": product['org'],
        "plan_name": plan['name'],
        "plan_title": plan['title'],
        "plan_version": plan['version'],
        "swagger": swagger_content,
        "plan_created_date": plan['created'],
        "plan_updated_date": plan['updated'],
        "basepath": basepath,
        "description": plan.get("description", "")
    }
    json_data = json.dumps(data, indent=4)

    curl_command = [
        "curl", "--insecure", "--request", "POST",
        "--url", API_PUSH_URL,
        "--header", f"Content-Type: {HEADERS['Content-Type']}",
        "--header", f"User-Agent: {HEADERS['User-Agent']}",
        "--header", f"x-api-key: {HEADERS['x-api-key']}",
        "--header", f"x-apigw-api-id: {HEADERS['x-apigw-api-id']}",
        "--header", f"x-app-cat-id: {HEADERS['x-app-cat-id']}",
        "--header", f"x-database-schema: {HEADERS['x-database-schema']}",
        "--header", f"x-fapi-financial-id: {HEADERS['x-fapi-financial-id']}",
        "--header", f"x-request-id: {HEADERS['x-request-id']}",
        "--data", json_data
    ]

    try:
        subprocess.run(curl_command, check=True)
        logging.info(f"POST request successful for product: {product['name']}, plan: {plan['name']}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed POST request for product: {product['name']}, plan: {plan['name']}")
        logging.error(e)

def process_product_list(env, catalog, product_list):
    """Processes each product and plan, downloads Swagger, and pushes to the database."""
    for product in product_list.get('results', []):
        prod_details = {
            "name": product.get('name', ''),
            "title": product.get('title', ''),
            "state": product.get('state', ''),
            "version": product.get('version', ''),
            "env": env,
            "space": product.get('space', ''),
            "org": product.get('org', '')
        }

        for plan in product.get('plans', []):
            plan_details = {
                "name": plan.get('name', ''),
                "title": plan.get('title', ''),
                "version": plan.get('version', ''),
                "created": plan.get('created', ''),
                "updated": plan.get('updated', '')
            }

            for api in plan.get('apis', []):
                api_name = api.get('name', '')
                api_version = api.get('version', '')

                if api_name and api_version:
                    swagger_file = download_and_save_swagger(env, catalog, api_name, api_version)
                    if swagger_file:
                        swagger_content, basepath = load_swagger_file(swagger_file)
                        if swagger_content:
                            push_to_database(prod_details, plan_details, swagger_content, basepath)

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

   

import subprocess
import os
import json
import getpass
import yaml
from glob import glob

# Constants
OUTPUT_DIR = "/tmp/output"
LOGIN_SCRIPT = 
GET_SWAGGER_SCRIPT = 

  

# Utility Functions
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
            print(success_msg)
        return result
    except subprocess.CalledProcessError as e:
        print(f"{error_msg}: {e}")
        if capture_output:
            print(e.stderr)
        exit(1)

def setup_output_directory():
    """Ensures the output directory exists."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Created output directory at {OUTPUT_DIR}")

def find_latest_yaml_file():
    """Finds the latest YAML file in the output directory."""
    yaml_files = glob(os.path.join(OUTPUT_DIR, "*.yaml"))
    if not yaml_files:
        print("Error: No YAML files found in the output directory.")
        return None
    latest_file = max(yaml_files, key=os.path.getctime)
    print(f"Using product list file: {latest_file}")
    return latest_file

# Core Functions
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
        print("Exiting due to missing product list file.")
        exit(1)

    with open(file_path, 'r') as f:
        data = yaml.safe_load(f) or {}
        if not data:
            print("Error: Product list is empty or could not be loaded properly.")
            return None
        return data

def download_swagger(env, catalog, product_list):
    """Downloads Swagger files for each API in the product list."""
    for product in product_list.get('results', []):
        for plan in product.get('plans', []):
            for api in plan.get('apis', []):
                name = api.get('name')
                version = api.get('version')
                if name and version:
                    print(f"Downloading Swagger for {name}:{version}")
                    get_swagger_command = [GET_SWAGGER_SCRIPT, env, f"{name}:{version}", catalog]
                    result = run_command(
                        get_swagger_command,
                        None,
                        f"Error downloading Swagger for {name}:{version}",
                        capture_output=True
                    )
                    if result and result.stdout:
                        save_swagger_file(name, version, result.stdout)
                    else:
                        print(f"No Swagger content found for {name}:{version}")

def save_swagger_file(name, version, content):
    """Saves Swagger content to a JSON file."""
    swagger_output_file = os.path.join(OUTPUT_DIR, f"{name}_{version}.json")
    with open(swagger_output_file, 'w') as output_file:
        output_file.write(content)
    print(f"Swagger downloaded and saved to {swagger_output_file}")

def push_swagger_to_database():
    """Pushes all Swagger files in the output directory to the API endpoint."""
    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith(".json"):
            file_path = os.path.join(OUTPUT_DIR, filename)
            with open(file_path, "r") as f:
                swagger_content = f.read()

            # Prepare the JSON data
            try:
                product_name, product_version = filename.rsplit("_", 1)
                product_version = product_version.replace(".json", "")
                post_data = {
                    "product": product_name,
                    "product_version": product_version,
                    "swagger": swagger_content
                }
                json_data = json.dumps(post_data, indent=4)
                execute_curl(json_data)
            except ValueError:
                print(f"Invalid filename format: {filename}. Skipping...")

def execute_curl(json_data):
    """Executes the curl command to push Swagger data to the database."""
    curl_command = [
        "curl", "--insecure", "--request", "POST",
        "--url", API_PUSH_URL,
        *[f"--header {k}: {v}" for k, v in HEADERS.items()],
        "--data", json_data
    ]
    run_command(curl_command, None, "Error pushing Swagger file")

def main():
    # Setup output directory
    setup_output_directory()

    # Collect user inputs
    env = input("Enter environment (e.g., dev, prod): ")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    catalog = input("Enter catalog name: ")
    space = input("Enter space name: ")

    # Execute steps
    login(env, username, password)
    list_products(env, catalog, space)
    
    product_list = load_product_list()
    if not product_list:
        print("Exiting due to empty or invalid product list.")
        exit(1)

    download_swagger(env, catalog, product_list)
    push_swagger_to_database()

if __name__ == "__main__":
    main()

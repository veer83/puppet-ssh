import yaml
import subprocess
import os

# Path to the product list YAML file
PRODUCT_LIST_FILE = "./output/products.yaml"
# Path to the output directory for Swagger files
OUTPUT_DIR = "./output"
# Path to the shell script for downloading Swagger
GET_SWAGGER_SCRIPT = "./get_swagger_by_name.sh"
# Path to the shell script for downloading product list
GET_PRODUCTS_SCRIPT = "./get_all_products.sh"

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_product_list(env):
    """
    Use the shell script to download the product list.
    """
    try:
        # Construct the command to execute the script
        command = [GET_PRODUCTS_SCRIPT, env, PRODUCT_LIST_FILE, "0", catalog, space]
        # Run the shell command to download the product list
        subprocess.run(command, check=True)
        # Run the shell command to download the product list
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading product list - {e}")

def load_product_list(file_path):
    """
    Load the product list from a YAML file.
    """
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def download_swagger(env, name, version):
    """
    Use the shell script to download the Swagger file for a given API name and version.
    """
    try:
        # Construct the command to execute the script
        command = [GET_SWAGGER_SCRIPT, env, f"{name}:{version}", catalog]
        # Run the shell command to download the Swagger
        subprocess.run(command, check=True)
        # Run the shell command to download the Swagger
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading Swagger for {name}:{version} - {e}")

def main():
    # Environment variable (e.g., dev, prod)
    env = "dev"
catalog = "central"
space = "cs"

    # Download the product list
    download_product_list(env)

    # Load the product list from the YAML file
    product_list = load_product_list(PRODUCT_LIST_FILE)

    # Iterate over each product in the product list
    for product in product_list.get('results', []):
        plans = product.get('plans', [])
        for plan in plans:
            apis = plan.get('apis', [])
            for api in apis:
                # Extract API name and version
                name = api.get('name')
                version = api.get('version')
                if name and version:
                    print(f"Downloading Swagger for {name}:{version}")
                    # Download the Swagger file for this API
                    download_swagger(env, name, version)

if __name__ == "__main__":
    main()

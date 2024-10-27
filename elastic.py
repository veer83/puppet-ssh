import subprocess
import os
import yaml

# Paths to scripts
login_script_path = "./apic_login.sh"
list_products_script_path = "./list_products.sh"
get_swagger_script_path = "./get_swagger_by_name.sh"

# Product list file path
PRODUCT_LIST_FILE = None

# Step 0: Create output directory
def create_output_directory():
    output_dir = "/tmp/output/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory at {output_dir}")

# Step 1: Log in using `apic_login.sh`
def login(env, username, password):
    login_command = [
        login_script_path,
        env,  # Environment (e.g., "dev", "prod", etc.)
        username,  # Username
        password   # Password
    ]
    try:
        subprocess.run(login_command, check=True)
        print("Login successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error during login: {e}")
        exit(1)

# Step 2: Run `list_products.sh` after logging in successfully
def list_products(env, catalog, space):
    # Update PRODUCT_LIST_FILE path after generating the product list
    global PRODUCT_LIST_FILE
    PRODUCT_LIST_FILE = "/private/tmp/output/" + f"ProductList_{env}_{catalog}_{space}.yaml"
    list_products_command = [
        list_products_script_path, env,
        PRODUCT_LIST_FILE, "0", catalog, space
    ]
    try:
        subprocess.run(list_products_command, check=True)
        print("Product list downloaded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading product list: {e}")
        exit(1)

# Step 3: Load the product list and download Swagger files
def load_product_list(file_path):
    """
    Load the product list from a YAML file.
    """
    if not os.path.exists(file_path):
        print(f"Error: Product list file not found at {file_path}.")
        return None

    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
        if not data:
            print("Error: Product list is empty or could not be loaded properly.")
            return None
        return data

def download_swagger(env, catalog, product_list):
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

                    # Step 4: Run the `get_swagger_by_name.sh` script to download the Swagger file
                    get_swagger_command = [
                        get_swagger_script_path,
                        env,  # Environment
                        f"{name}:{version}",
                        catalog  # Catalog name
                    ]

                    try:
                        subprocess.run(get_swagger_command, check=True)
                        print(f"Swagger downloaded for {name}:{version}")
                    except subprocess.CalledProcessError as e:
                        print(f"Error downloading Swagger for {name}:{version} - {e}")

def main():
    # Step 0: Create output directory
    create_output_directory()
    # Collect user input for environment, space, and catalog
    env = input("Enter environment (e.g., dev, prod): ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    catalog = input("Enter catalog name: ")
    space = input("Enter space name: ")

    # Step 1: Log in
    login(env, username, password)

    # Step 2: Download the product list
    list_products(env, catalog, space)

    # Step 3: Load the product list from the YAML file
    product_list = load_product_list(PRODUCT_LIST_FILE)
    if not product_list:
        print("Error: Product list is empty or not loaded properly. Exiting.")
        exit(1)

    # Step 4: Download Swagger files for each API
    download_swagger(env, catalog, product_list)

if __name__ == "__main__":
    main()

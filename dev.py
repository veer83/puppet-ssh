import os
import subprocess
import json
import logging
import shutil
from datetime import datetime

# Configure logging
log_dir = "/tmp/logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler(f"{log_dir}/swagger_download_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    ]
)

# API endpoint and headers
api_url = ""
headers = {
    "Content-Type": "application/json",
    "User-Agent": "",
    "x-api-key": "",
    "x-apigw-api-id": "",
    "x-app-cat-id": "sdsadas",
    "x-database-schema": "",
    "x-fapi-financial-id": "sdsadsadasdsadsa",
    "x-request-id": "abcd"
}

# Paths to shell scripts and output directory

output_dir = "/tmp/output"

# Get user input
env = input("Enter the environment (e.g., dv1, qa, prod): ").strip().lower()
catalog_name = input("Enter the catalog name: ").strip()

def run_login_script():
    """Runs the login shell script to authenticate."""
    try:
        subprocess.run(["sudo", LOGIN_SCRIPT_PATH, env], check=True)
        logging.info("Login script executed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error("Failed to run login script.")
        logging.error(e)
        raise

def run_list_products_script():
    """Runs the script to list products and store the output in the output directory."""
    try:
        subprocess.run(["sudo", LIST_PRODUCTS_SCRIPT_PATH, env, output_dir, catalog_name], check=True)
        logging.info("List products script executed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error("Failed to run list products script.")
        logging.error(e)
        raise

def run_swagger_download_script():
    """Runs the shell script to download Swagger files."""
    try:
        subprocess.run(["sudo", SWAGGER_DOWNLOAD_SCRIPT_PATH, env, output_dir, catalog_name], check=True)
        logging.info("Swagger download script executed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error("Failed to run Swagger download script.")
        logging.error(e)
        raise

def read_swagger_file(file_path):
    """Reads the Swagger file content."""
    with open(file_path, "r") as file:
        content = file.read()
    return content

def send_post_request(data):
    """Sends a POST request to the API with provided Swagger data using sudo curl with --insecure."""
    curl_command = [
        "sudo", "curl", "--insecure", "--request", "POST",
        "--url", api_url,
        "--header", f"Content-Type: {headers['Content-Type']}",
        "--header", f"User-Agent: {headers['User-Agent']}",
        "--header", f"x-api-key: {headers['x-api-key']}",
        "--header", f"x-apigw-api-id: {headers['x-apigw-api-id']}",
        "--header", f"x-app-cat-id: {headers['x-app-cat-id']}",
        "--header", f"x-database-schema: {headers['x-database-schema']}",
        "--header", f"x-fapi-financial-id: {headers['x-fapi-financial-id']}",
        "--header", f"x-request-id: {headers['x-request-id']}",
        "--data", json.dumps(data)
    ]
    try:
        subprocess.run(curl_command, check=True)
        logging.info(f"POST request successful for Swagger file.")
    except subprocess.CalledProcessError as e:
        logging.error("Failed POST request for Swagger file.")
        logging.error(e)

def process_swagger_files():
    """Processes each Swagger file in the output directory."""
    swagger_files = os.listdir(output_dir)
    if not swagger_files:
        logging.error("No Swagger files found in the output directory.")
        return

    for swagger_file in swagger_files:
        file_path = os.path.join(output_dir, swagger_file)
        logging.info(f"Processing Swagger file: {file_path}")

        # Read file content and send POST request
        swagger_content = read_swagger_file(file_path)
        post_data = {
            "product": swagger_file.split("_")[0],
            "product_version": swagger_file.split("_")[1].replace(".yaml", ""),
            "swagger": swagger_content
        }

        # Log data to be sent
        logging.info("Sending Swagger data to API:")
        logging.info(json.dumps(post_data, indent=4))

        # Send POST request
        send_post_request(post_data)

def cleanup_output_directory(directory):
    """Removes all files in the specified directory using sudo."""
    try:
        if os.path.exists(directory):
            subprocess.run(["sudo", "rm", "-rf", directory], check=True)
            logging.info(f"Cleaned up output directory: {directory}")
            os.makedirs(directory, exist_ok=True)  # Recreate directory after cleanup
    except Exception as e:
        logging.error(f"Failed to clean up output directory: {directory}")
        logging.exception(e)

def main():
    # Authenticate using the login script
    run_login_script()

    # List products in the specified catalog
    run_list_products_script()

    # Download Swagger files
    run_swagger_download_script()

    # Process each downloaded Swagger file
    process_swagger_files()

    # Clean up the output directory
    cleanup_output_directory(output_dir)

if __name__ == "__main__":
    main()

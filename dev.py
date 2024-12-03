import os
import json
import subprocess
import logging
from datetime import datetime

# Constants
LOG_DIR = "/tmp/logs"
GET_SWAGGER_SCRIPT = "./ge"
API_PUSH_URL = ""
HEADERS = {
  

# Configure logging
os.makedirs(LOG_DIR, exist_ok=True)
log_filename = os.path.join(LOG_DIR, f"swagger_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_filename)
    ]
)

# Utility Functions
def run_command(command, success_msg, error_msg, capture_output=False):
    """Runs a shell command with optional output capturing."""
    try:
        result = subprocess.run(
            command,
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

def filter_swagger_content(raw_content):
    """Filters the Swagger content and extracts required details."""
    swagger_lines = []
    capture = False
    basepath = None
    info_data = {}

    for line in raw_content.splitlines():
        if 'openapi' in line or 'swagger' in line:
            capture = True  # Start capturing lines when "openapi" or "swagger" is found
        if capture:
            swagger_lines.append(line)
        if 'basePath' in line:
            basepath = line.split(':', 1)[1].strip().strip('"')

    # Extracting additional fields
    swagger_json = json.loads("\n".join(swagger_lines))
    if "info" in swagger_json:
        info = swagger_json["info"]
        info_data = {
            "info_title": info.get("title", ""),
            "info_description": info.get("description", ""),
            "info_version": info.get("version", ""),
            "info_x_ibm_name": info.get("x-ibm-name", ""),
            "info_license_name": info.get("license", {}).get("name", ""),
            "info_contact_name": info.get("contact", {}).get("name", ""),
            "info_contact_email": info.get("contact", {}).get("email", ""),
            "info_contact_url": info.get("contact", {}).get("url", ""),
            "info_x_api_id": info.get("x-api-id", ""),
            "info_bmo_api_type": info.get("x-bmo-api-type", ""),
            "info_bmo_api_provider_id": info.get("x-bmo-api-provider-id", ""),
            "info_bmoservicedomain_name": info.get("x-bmo-service-domain-name", ""),
            "info_x_api_specification_compliant": info.get("x-api-specification-compliant", ""),
            "info_x_bmo_jira": info.get("x-bmo-jira", ""),
            "info_x_template_version": info.get("x-template-version", "")
        }

    return "\n".join(swagger_lines), basepath, info_data

# Database Push Function
def push_to_database(product, plan, api_name, api_version, swagger_content, basepath, env, space, org, created_date, updated_date, info_data):
    """Formats data and pushes it to the database using a POST request."""
    data = {
        "prod_name": product.get("name", ""),
        "prod_title": product.get("title", ""),
        "prod_state": product.get("state", ""),
        "prod_version": product.get("version", ""),
        "env": env,
        "space": space,
        "org": org,
        "plan_name": plan.get("name", ""),
        "plan_title": plan.get("title", ""),
        "plan_version": product.get("version", ""),
        "swagger": swagger_content,
        "prod_created_date": created_date,
        "prod_updated_date": updated_date,
        "basepath": basepath,
        "description": plan.get("description", ""),
        "api_name": api_name,
        "api_version": api_version,
        "verb": "",
        "path": "",
        "dataclassification_code": "",
        "url_variable": "",
        "url_value": "",
        **info_data  # Add the extracted info fields
    }

    json_data = json.dumps(data, indent=4)
    logging.info(f"Payload being sent for product: {product.get('name')} plan: {plan.get('name')}")
    logging.info(f"Payload data: {json.dumps(data, indent=4)}")  # Log the complete payload data

    curl_command = [
        "curl", "--insecure", "--request", "POST",
        "--url", API_PUSH_URL,
        "--header", f"Content-Type: {HEADERS['Content-Type']}",
        "--header", f"User-Agent: {HEADERS['User-Agent']}",
        "--header", f"x-api-key: {HEADERS['x-api-key']}",
        "--header", f"x-apigw-api-id: {HEADERS['x-apigw-api-id']}",
        "--header", f"x-database-schema: {HEADERS['x-database-schema']}",
        "--header", f"x-fapi-financial-id: {HEADERS['x-fapi-financial-id']}",
        "--header", f"x-request-id: {HEADERS['x-request-id']}",
        "--data", json_data
    ]

    try:
        result = subprocess.run(curl_command, check=True, capture_output=True, text=True)
        logging.info(f"POST request successful for product: {product.get('name')} plan: {plan.get('name')}")
        logging.info(f"API Response: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed POST request for product: {product.get('name')} plan: {plan.get('name')}")
        logging.error(f"Error: {e.stderr}")

# Main Processing Functions
def download_swagger(env, catalog, product_list, space, org):
    """Downloads, filters, and pushes Swagger files for each API in the product list."""
    for product in product_list.get('results', []):
        product_name = product.get('name')
        for plan in product.get('plans', []):
            plan_name = plan.get('name')
            created_date = plan.get('created_at', '')
            updated_date = plan.get('updated_at', '')
            logging.info(f"Processing plan: {plan_name} with created_at: {created_date} and updated_at: {updated_date}")

            for api in plan.get('apis', []):
                name = api.get('name')
                version = api.get('version')
                if name and version:
                    logging.info(f"Processing API Name: {name}, version: {version}")

                    get_swagger_command = [GET_SWAGGER_SCRIPT, env, f"{name}:{version}", catalog]
                    result = run_command(
                        get_swagger_command,
                        None,
                        f"Error downloading Swagger for {name}:{version}",
                        capture_output=True
                    )

                    if result and result.stdout:
                        swagger_content, basepath, info_data = filter_swagger_content(result.stdout)
                        if swagger_content:
                            push_to_database(
                                product, plan, name, version,
                                swagger_content, basepath, env, space, org,
                                created_date, updated_date, info_data
                            )
                        else:
                            logging.warning(f"No relevant Swagger content found for {name}:{version}")
                    else:
                        logging.warning(f"No Swagger content found for {name}:{version}")

# Main Script
def main():
    env = os.getenv("ENVIRONMENT", "dev")
    catalog = os.getenv("CATALOG_NAME", "default_catalog")
    space = os.getenv("SPACE_NAME", "default_space")
    org = os.getenv("ORG_NAME", "default_org")

    # Load product list from YAML or any input file
    product_list = load_product_list()  # Ensure you implement this function to read the file
    if not product_list:
        logging.error("Exiting due to empty or invalid product list.")
        exit(1)

    download_swagger(env, catalog, product_list, space, org)

if __name__ == "__main__":
    main()

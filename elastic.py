import subprocess

# Step 1: Log in using `apic_login.sh`
login_command = [
    "./scripts/apic_login.sh", 
    "dev",  # Replace with your environment, e.g., "dev", "prod", etc.
    "your_username",  # Replace with your username
    "your_password"   # Replace with your password
]

try:
    subprocess.run(login_command, check=True)
    print("Login successful.")
except subprocess.CalledProcessError as e:
    print(f"Error during login: {e}")
    exit(1)

# Step 2: Run `list_products.sh` after logging in successfully
list_products_command = [
    "./scripts/list_products.sh", "dev", 
    "/tmp/output/products.yaml", "0", "central", "cs"
]

try:
    subprocess.run(list_products_command, check=True)
    print("Product list downloaded successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error downloading product list: {e}")
    exit(1)

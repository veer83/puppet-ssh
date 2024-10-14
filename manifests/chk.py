import subprocess
import yaml

# Variables
NAMESPACE = "your-namespace"  # Replace with the namespace you want to use
SEARCH_KEYWORD = "ar"


def get_build_configs(namespace):
    """Get all BuildConfigs in the given namespace."""
    try:
        result = subprocess.run(
            ["oc", "get", "bc", "-n", namespace, "--no-headers", "-o", "custom-columns=:metadata.name"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error fetching BuildConfigs: {e.stderr}")
        return []

def get_build_config_yaml(namespace, build_config_name):
    """Get the YAML of a specific BuildConfig."""
    try:
        result = subprocess.run(
            ["oc", "get", "bc", build_config_name, "-n", namespace, "-o", "yaml"],
            capture_output=True,
            text=True,
            check=True,
        )
        return yaml.safe_load(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error fetching BuildConfig {build_config_name}: {e.stderr}")
        return None

def main(namespace):
    build_configs = get_build_configs(namespace)
    
    count = 0
    for build_config_name in build_configs:
        print(f"Processing BuildConfig: {build_config_name}")
        build_config_yaml = get_build_config_yaml(namespace, build_config_name)
        
        if build_config_yaml is None:
            continue

        # Convert YAML to string and check for SEARCH_KEYWORD
        build_config_str = yaml.dump(build_config_yaml)
        if SEARCH_KEYWORD in build_config_str:
            count += 1
            print(f"'{SEARCH_KEYWORD}' found in BuildConfig {build_config_name}.")

    print(f"Total number of BuildConfigs containing '{SEARCH_KEYWORD}' in namespace {namespace}: {count}")

if __name__ == "__main__":
    namespace = input("Enter the namespace: ").strip()
    main(namespace)

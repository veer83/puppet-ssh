import json
import subprocess
import logging
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to execute oc commands and capture output
def run_oc_command(command: list) -> str:
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running command {command}: {e}")
        return None

# Fetch build configs from the project
def get_build_configs(project_name: str):
    logging.info(f"Fetching build configs for project {project_name}")
    output = run_oc_command(["oc", "get", "bc", "-n", project_name, "-o", "json"])
    return json.loads(output) if output else None

# Check if a build config matches the criteria
def matches_criteria(bc: dict) -> bool:
    context_dir = bc["spec"]["source"].get("c", "")
    uri = bc["spec"]["source"]["git"].get("u", "")
    ref = bc["spec"]["source"]["git"].get("r", "")
    
    return (context_dir == "ap" and
            uri == "gp" and
            ref == "cp")

# Function to count and print matching build configs
def count_and_print_matching_build_configs(projects: list) -> None:
    total_count = 0  # To count the total number of matching build configs
    
    for project_name in projects:
        logging.info(f"Processing project: {project_name}")
        build_configs = get_build_configs(project_name)

        if build_configs:
            matching_count = 0  # To count matches within each project
            for bc in build_configs.get("items", []):
                bc_name = bc["metadata"]["name"]

                if matches_criteria(bc):
                    logging.info(f"Matching BuildConfig: {bc_name} in project {project_name}")
                    matching_count += 1
                    total_count += 1
            
            logging.info(f"Found {matching_count} matching build configs in project {project_name}")
        else:
            logging.warning(f"No build configs found for project {project_name}")
    
    logging.info(f"Total matching build configs across all projects: {total_count}")

# Function to load projects dynamically (either from input or config)
def load_projects(project_file: str = None, specific_projects: list = None) -> list:
    # Load from a file if specified
    if project_file:
        with open(project_file, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    # Use projects provided by the user
    elif specific_projects:
        return specific_projects
    else:
        return []

# Entry point with arguments for flexibility
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Count and print matching OpenShift BuildConfigs across projects.')
    parser.add_argument('--projects', nargs='+', help='List of specific projects to update.')
    parser.add_argument('--project-file', help='File containing a list of projects to process (one per line).')
    parser.add_argument('--batch-size', type=int, default=5, help='Number of projects to process in a batch.')
    args = parser.parse_args()

    # Load the projects either from a file or a provided list
    projects = load_projects(args.project_file, args.projects)
    
    if not projects:
        logging.error("No projects provided. Use --projects or --project-file.")
    else:
        # Process in batches to avoid processing too many projects at once
        batch_size = args.batch_size
        for i in range(0, len(projects), batch_size):
            project_batch = projects[i:i + batch_size]
            logging.info(f"Processing batch of {len(project_batch)} projects")
            count_and_print_matching_build_configs(project_batch)

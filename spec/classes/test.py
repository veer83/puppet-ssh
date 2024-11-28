import json
import subprocess
import logging
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Function to execute OC commands and capture output
def run_oc_command(command: list) -> str:
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running command {command}: {e}")
        return None

# Fetch build configs from the project
def get_build_configs(project_name: str) -> list:
    logging.info(f"Fetching build configs for project {project_name}")
    output = run_oc_command(["oc", "get", "bc", "-n", project_name, "-o", "json"])
    return json.loads(output) if output else None

# Check if a build config is missing any of the required criteria
def missing_any_criteria(bc: dict) -> bool:
    source = bc.get("spec", {}).get("source", {})
    context_dir = source.get("contextDir", "")
    git = source.get("git", {})
    uri = git.get("uri", "")
    ref = git.get("ref", "")
    
    # Return True if any of the required pieces of information are missing
    return not (
        
    )

# Function to count and print build configs that are missing any criteria
def count_and_print_missing_criteria_build_configs(projects: list) -> None:
    total_count = 0  # To count the total number of build configs missing criteria

    for project_name in projects:
        logging.info(f"Processing project: {project_name}")
        build_configs = get_build_configs(project_name)
        
        if build_configs:
            missing_count = 0  # To count matches within each project
            for bc in build_configs.get("items", []):
                bc_name = bc.get("metadata", {}).get("name", "")
                if missing_any_criteria(bc):
                    logging.info(f"BuildConfig missing criteria: {bc_name} in project {project_name}")
                    missing_count += 1
                    total_count += 1
            logging.info(f"Found {missing_count} build configs missing criteria in project {project_name}")
        else:
            logging.warning(f"No build configs found for project {project_name}")
    
    logging.info(f"Total build configs missing criteria across all projects: {total_count}")

# Function to load projects dynamically (either from input or config)
def load_projects(project_file: str = None, specific_projects: list = None) -> list:
    if project_file:
        with open(project_file, "r") as file:
            return [line.strip() for line in file if line.strip()]
    elif specific_projects:
        return specific_projects
    else:
        return []

# Entry point with arguments for flexibility
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Count and print build configs missing any required criteria across projects."
    )
    parser.add_argument("--project-file", help="File containing a list of projects to process (one per line).")
    parser.add_argument("--projects", nargs="+", help="List of specific projects to update.")
    parser.add_argument("--batch-size", type=int, default=5, help="Number of projects to process in a batch.")
    args = parser.parse_args()

    # Load the projects either from a file or a provided list
    projects = load_projects(args.project_file, args.projects)

    if not projects:
        logging.error("No projects provided. Use --projects or --project-file.")
    else:
        # Process in batches to avoid processing too many projects at once
        batch_size = args.batch_size
        for i in range(0, len(projects), batch_size):
            project_batch = projects[i : i + batch_size]
            logging.info(f"Processing batch of {len(project_batch)} projects.")
            count_and_print_missing_criteria_build_configs(project_batch)

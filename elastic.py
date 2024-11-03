#!/bin/bash

# Define SonarQube URL for the API endpoint
SONARQUBE_URL=""
AUTH_TOKEN=""  # Replace with actual token

# Project key and branch name
PROJECT_KEY=""
BRANCH_NAME=""

# API endpoint to set the New Code setting
NEW_CODE_API="$SONARQUBE_URL/api/project_settings/set"

# Print debug information
echo "Setting New Code reference branch to 'master' for project '$PROJECT_KEY' on branch '$BRANCH_NAME'..."

# Send the API request to set the reference branch
curl -v -u "$AUTH_TOKEN:" -X POST "$NEW_CODE_API" \
    -d "component=$PROJECT_KEY" \
    -d "key=new_code.period" \
    -d "value=reference_branch:$BRANCH_NAME" \
    -d "branch=$BRANCH_NAME" \
    -o response.json -w "%{http_code}"

# Check the response
if [[ $? -eq 0 ]]; then
  echo "API request sent successfully."
else
  echo "Failed to send API request."
  exit 1
fi

# Parse the response code and display the response
HTTP_STATUS=$(tail -n 1 response.json)
if [[ "$HTTP_STATUS" == "200" ]]; then
  echo "New Code reference branch updated successfully for project $PROJECT_KEY."
else
  echo "Failed to update New Code reference branch. HTTP status code: $HTTP_STATUS"
  echo "Response:"
  cat response.json
fi

# Clean up
rm response.json


or 


#!/bin/bash

# SonarQube API base URL
SONARQUBE_URL=""
AUTH_TOKEN=""  # Replace with actual token

# Project and branch details
PROJECT_KEY="3"
TARGET_BRANCH=""
REFERENCE_BRANCH=""  # Branch to set as reference for New Code

# API endpoint for setting project settings
PROJECT_SETTINGS_API="$SONARQUBE_URL/api/project_settings/set"

# Display information for debugging
echo "Setting New Code period for project '$PROJECT_KEY' on branch '$TARGET_BRANCH' to reference branch '$REFERENCE_BRANCH'."

# Send the API request to set the New Code period based on reference branch
curl -v -u "$AUTH_TOKEN:" -X POST "$PROJECT_SETTINGS_API" \
     -d "component=$PROJECT_KEY" \
     -d "key=new_code.period" \
     -d "value=reference_branch:$REFERENCE_BRANCH" \
     -o response.json -w "%{http_code}"

# Verify if the API call was successful
HTTP_STATUS=$(tail -n 1 response.json)
if [[ "$HTTP_STATUS" == "200" ]]; then
  echo "New Code period set successfully for project $PROJECT_KEY to use '$REFERENCE_BRANCH' as reference branch."
else
  echo "Failed to set New Code period. HTTP status code: $HTTP_STATUS"
  echo "Response:"
  cat response.json
fi

# Clean up
rm response.json


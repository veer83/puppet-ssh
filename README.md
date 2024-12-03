{
  "rclass": "local",
  "key": "my-target-repo",
  "packageType": "generic",
  "description": "This is my target repository",
  "notes": "Repository for storing target artifacts"
}
curl -u <USERNAME>:<PASSWORD> -X PUT "http://<ARTIFACTORY_URL>/artifactory/api/repositories/my-target-repo" -H "Content-Type: application/json" -T repo-config.json

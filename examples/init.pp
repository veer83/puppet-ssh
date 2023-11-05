#!/bin/bash

# Elasticsearch connection settings
ELASTICSEARCH_HOST="your-elasticsearch-host"
ELASTICSEARCH_PORT="9200"
USERNAME="elastic"
PASSWORD="test"
EXCLUDE_PATTERN=".monitoring*"

# Get a list of all data streams
DATA_STREAMS=$(curl -s -u "$USERNAME:$PASSWORD" -X GET "https://${ELASTICSEARCH_HOST}:${ELASTICSEARCH_PORT}/_data_stream" | jq -r 'keys[]')

# Iterate through the data streams and delete them (excluding system data streams)
for DATA_STREAM in $DATA_STREAMS; do
  # Check if the data stream matches the exclude pattern
  if [[ "$DATA_STREAM" != *$EXCLUDE_PATTERN* ]]; then
    # Delete the data stream
    echo "Deleting data stream: $DATA_STREAM"
    curl -X DELETE -u "$USERNAME:$PASSWORD" "https://${ELASTICSEARCH_HOST}:${ELASTICSEARCH_PORT}/_data_stream/$DATA_STREAM"
  else
    echo "Skipping system data stream: $DATA_STREAM"
  fi
done


logging.level: info # Adjust the log level as needed
logging.to_files: true
logging.files:
  path: /var/log/filebeat
  name: filebeat
  keepfiles: 7
  permissions: 0644

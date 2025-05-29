5. Verify Logstash Plugins
Run these commands to check if the plugins are installed:

bin/logstash-plugin list --verbose | grep logstash-input-http
bin/logstash-plugin list --verbose | grep codec-json

6. Check Port Access from Kubernetes Nodes
Run these commands from a Kubernetes node:

nc -zv <LOGSTASH_IP> 5044
# or
telnet <LOGSTASH_IP> 5044
# or (for HTTP input test)
curl -X POST http://<LOGSTASH_IP>:5044/ -d '{"test":"connect"}' -H "Content-Type: application/json"


1. Fluent Bit Image Version
Use the following Fluent Bit image (compatible with Elasticsearch and Logstash 7.17):
cr.fluentbit.io/fluent/fluent-bit:1.9.10

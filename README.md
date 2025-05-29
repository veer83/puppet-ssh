curl -X POST http://<LOGSTASH_IP>:5044/ -d '{"test":"connect"}' -H "Content-Type: application/json"

kubectl run tmp-shell --rm -i -t --image=busybox -- sh
# Inside the pod shell
nc -zv <LOGSTASH_IP> 5044
sudo netstat -plnt | grep 5044

image: cr.fluentbit.io/fluent/fluent-bit:1.9.10


nc -zv <LOGSTASH_IP> 5044
# or
telnet <LOGSTASH_IP> 5044
# or (for HTTP input test)
curl -X POST http://<LOGSTASH_IP>:5044/ -d '{"test":"connect"}' -H "Content-Type: application/json"


1. Fluent Bit Image Version
Use the following Fluent Bit image (compatible with Elasticsearch and Logstash 7.17):
cr.fluentbit.io/fluent/fluent-bit:1.9.10

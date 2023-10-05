I hope this message finds you well. I wanted to provide an update on the status of our Albatross Elasticsearch cluster, which has been in a yellow state for the past 8 hours.

I'm pleased to report that there has been some improvement, and the cluster is nearing recovery. Currently, only 4 indexes remain unassigned out of the initial 615.

We took action by deleting data from both the snap team and old-use cases that are no longer in service. However, despite these efforts, the cluster still contains a substantial number of shards. Notably, our Elastic nodes are currently burdened with more than 850 shards per node. This exceeds the recommended range of 600 to 800 shards per node as suggested by Elastic.

This situation is of concern as we are planning an Elastic upgrade activity scheduled for October 7th at 1 am (UK time). Having over 850 shards per node can impact the smooth execution of the upgrade.

Furthermore, as seen in the snapshot, the resolver component has approximately 4000 C+ shards, and it's crucial that we manage these shards to keep them within a manageable size.

Given the upcoming upgrade and the suboptimal shard count, I urge the team to continue working diligently on this matter to ensure a successful upgrade and maintain the health of our Elasticsearch cluster.

Please reach out if you require any additional information or support in this regard. Your cooperation is greatly appreciated.

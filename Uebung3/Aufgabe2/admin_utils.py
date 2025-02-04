from kafka.admin import KafkaAdminClient
from kafka.errors import KafkaError


# File allows to see the replication of topics in a Kafka cluster and shows which node functions as leader for which topics


def check_topic_replication(
    bootstrap_servers=["localhost:9092", "localhost:9093", "localhost:9094"]
):
    try:
        admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        topics = admin.list_topics()

        # Track which brokers have replicas for each topic
        topic_replica_distribution = {}

        topic_metadata = admin.describe_topics(topics)

        for metadata in topic_metadata:
            print(metadata)
            print("\n")

        for metadata in topic_metadata:
            topic_name = metadata["topic"]
            topic_replica_distribution[topic_name] = set()

            for partition in metadata["partitions"]:
                for replica in partition["replicas"]:
                    topic_replica_distribution[topic_name].add(replica)

        # Print distribution
        print("\nTopic replica distribution:")
        for topic, brokers in topic_replica_distribution.items():
            print(f"\nTopic: {topic}")
            print(f"Replicas on brokers: {sorted(list(brokers))}")

        admin.close()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    check_topic_replication()

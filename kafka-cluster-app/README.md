# Project Title: Kafka Cluster Application

This project is a simple Kafka application that utilizes a cluster of three servers with replication, using `kafka-python` as a dependency. The application consists of a Kafka producer and consumer, along with Docker configurations for easy deployment.

## Project Structure

```
kafka-cluster-app
├── src
│   ├── consumer.py
│   ├── producer.py
│   └── config.py
├── docker
│   └── kafka.dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd kafka-cluster-app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Build and run the Kafka cluster using Docker Compose:**
   ```bash
   docker-compose up --build
   ```

4. **Run the producer and consumer:**
   - Start the producer:
     ```bash
     python src/producer.py
     ```
   - Start the consumer:
     ```bash
     python src/consumer.py
     ```

## Usage Examples

- The producer sends messages to a specified Kafka topic.
- The consumer subscribes to the same topic and processes incoming messages.

## License

This project is licensed under the MIT License.
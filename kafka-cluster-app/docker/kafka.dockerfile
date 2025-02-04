FROM wurstmeister/kafka:latest

ENV KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092
ENV KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092
ENV KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
ENV KAFKA_REPLICATION_FACTOR=3

COPY ./config/server.properties /etc/kafka/server.properties

CMD ["start-kafka.sh"]
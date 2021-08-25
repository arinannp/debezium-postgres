# Capturing Data Changes by Using Debezium

## Prerequisites
* `Docker and Docker Compose`
* `Git (Optional)`

This project contains the following `containers`:

* `postgres`: Postgres database for storing project data.
    * Image: - postgres:13.2
             - debezium/postgres:12
    * Database Port: 5432
    * References: 
        * https://hub.docker.com/_/postgres
        * https://hub.docker.com/r/debezium/postgres

* `airflow`: Schedular and ETL generator.
    * Image: puckel/docker-airflow:1.10.9
    * Port: 8080
    * References: 
        * https://hub.docker.com/r/puckel/docker-airflow
        * https://github.com/puckel/docker-airflow
        
* `zookeeper`: Zookerper kafka cluster manager.
    * Image: debezium/zookeeper:latest
    * Port: 2181
    * References: https://hub.docker.com/r/debezium/zookeeper

* `kafka`: Kafka message broker.
    * Image: debezium/kafka:latest
    * Port: 9092
    * References: https://hub.docker.com/r/debezium/kafka

* `debezium`: Reading data capture from write ahead log (WAL) and produce to kafka.
    * Image: debezium/connect:latest
    * Port: 8083
    * References: https://hub.docker.com/r/debezium/connect

* `spark`: Spark Master as a kafka consumer.
    * Image: bitnami/spark:3.1.2
    * Port: 4040
    * References: 
        * https://hub.docker.com/r/bitnami/spark 
        * https://github.com/bitnami/bitnami-docker-spark        


## Architecture Components
![](./images/project-architecture.png "CDC Debezium Architecture")


## Setup
### Clone project
Clone this repository by using command:

    $ git clone https://github.com/arinannp/debezium-postgres.git

### Build and Start containers
For running containers, we can use following command:
        
    $ docker-compose -f docker-compose.yaml up -d

Note: -d command is using for running docker in background.

### Check containers logs
You can easily check the log of containers that have been built, whether the containers / apps are ready.
        
    $ docker-compose -f docker-compose.yaml logs --tail 10

Note: --tail command will display only the last n logs.
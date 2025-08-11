# Dummy Docker Compose Sample

This repository demonstrates a simple microservices architecture using Docker Compose. It includes an API server, multiple worker services, and an HAProxy load balancer.

## Architecture

```
                +-------------------+
                |    HAProxy        |
                | (Load Balancer)   |
                +--------+----------+
                         |
         +---------------+---------------+
         |                               |
+--------v--------+             +--------v--------+
|   apiserver     |             |     worker(s)   |
| (REST API)      |             | (Background Job)|
+-----------------+             +-----------------+
```

- **apiserver/**: Exposes a REST API on port 3500.
- **worker/**: Processes background jobs or tasks.
- **haproxy/**: Configures HAProxy to load balance requests from the API server to the background worker processes.
- **docker-compose.yaml**: Orchestrates all services.

## Usage

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Running the Application

1. Clone this repository:
    ```sh
    git clone <repo-url>
    cd dummyDockerCompose
    ```

2. Start all services:
    ```sh
    docker-compose up -d --build --scale worker=3
    ```
    That command will take care of building the docker containers, as well as bootstrap the application stack (includes 3 instances of the worker processes.)

3. Access the API via HAProxy at [http://localhost:3500(http://localhost:3500).

```
curl -s -D- http://localhost:3500/api/requests/some_request 
```

### Stopping the Application

```sh
docker-compose down
```

## Details

- **apiserver**: Handles incoming API requests.
- **worker**: Runs background jobs; can be scaled by adjusting `docker-compose.yaml`.
- **haproxy**: Forwards external traffic to the API server, enabling load balancing.

## Customization

- To scale workers:
    ```sh
    docker-compose up --scale worker=3
    ```

- Modify `haproxy/haproxy.cfg` to change load balancing rules.

## License

MIT License.
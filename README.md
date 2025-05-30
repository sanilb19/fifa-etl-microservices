FIFA ETL Pipeline with Dask & PostgreSQL

This project demonstrates a scalable, containerized ETL pipeline using:

    Dask for parallel data processing

    PostgreSQL as the backend database

    Docker Compose for service orchestration

We use historical FIFA player data (2015–2021) and process it through an ETL pipeline that can be extended with microservices.
📁 Project Structure

.
├── data/
│   └── archive/              # Raw FIFA CSVs (players_15.csv to players_21.csv)
├── etl/                      # ETL scripts
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── config.py
├── services/
│   └── api/                  # (optional) API service in FastAPI or Flask
├── main.py                   # Entrypoint for running the ETL
├── requirements.txt
├── .env                      # Environment variables
├── docker-compose.yml        # Docker service config
└── README.md

🚀 Getting Started
1. Clone the Repo

git clone https://github.com/yourname/fifa-etl-dask.git
cd fifa-etl-dask

2. Add Environment Variables

Create a .env file:

DB_CONNECTION_STRING=postgresql://postgres:postgres@db:5432/fifa

    🔥 Make sure not to use host.docker.internal inside containers.

3. Build and Start the Services

docker-compose up --build

This will:

    Start a Postgres database (fifa_postgres)

    Build and run the ETL service (fifa_etl) which reads from /data/archive and loads to Postgres

🧪 Verifying It Works
Check logs:

docker-compose logs etl

Connect to Postgres:

docker exec -it fifa_postgres psql -U postgres -d fifa

Then try:

\dt             -- See tables
SELECT * FROM players LIMIT 10;

🧼 Clean Up

docker-compose down -v  # Stops and removes containers and volumes

🧠 Extending This Project

    Add more ETL transformations (cleaning, feature engineering)

    Create microservices per transformation step

    Add FastAPI service to query enriched data

    Connect Apache Kafka or RabbitMQ for streaming ingest

    Deploy to the cloud (ECS, GKE, or Lambda with DBaaS)

🤝 Why This Project?

This project shows:

    Competency in Python, Docker, and Dask

    Familiarity with containerized microservices

    Ability to work with databases, ETL pipelines, and scalable workflows


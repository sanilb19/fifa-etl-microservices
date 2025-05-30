# FIFA ETL Pipeline with Dask & PostgreSQL

This project demonstrates a scalable, containerized ETL pipeline using:
- **Dask** for parallel data processing
- **PostgreSQL** as the backend database
- **Docker Compose** for service orchestration

We use historical FIFA player data (2015–2021) and process it through an ETL pipeline, now implemented as independent microservices.

---

## 📁 Project Structure

```
.
├── config/                   # Configuration and settings
├── data/
│   ├── archive/              # (Optional) Archive of raw CSVs
│   ├── kagglehub/            # Downloaded Kaggle datasets
│   ├── processed/            # Transformed data (Parquet)
│   └── raw/                  # Raw CSVs for processing
├── docker/                   # Dockerfiles and related scripts
├── services/
│   ├── extract/              # Extraction microservice
│   │   ├── extract.py
│   │   └── main.py
│   ├── transform/            # Transformation microservice
│   │   ├── transform.py
│   │   └── main.py
│   ├── load/                 # Loading microservice
│   │   ├── load.py
│   │   └── main.py
│   └── api/                  # (Optional) API service
├── tests/                    # Test suite
├── requirements.txt
├── requirements-base.txt
├── requirements-optional.txt
├── requirements-dev.txt
├── docker-compose.yml
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repo

```sh
git clone https://github.com/yourname/fifa-etl-dask.git
cd fifa-etl-dask
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root (see `config/settings.py` for defaults):

```
DB_CONNECTION_STRING=postgresql://postgres:postgres@postgres:5432/fifa_db
KAGGLE_DATASET=stefanoleone992/fifa-21-complete-player-dataset
DASK_WORKERS=4
DASK_MEMORY_LIMIT=4GB
```

> **Note:** For Kaggle downloads, place your `kaggle.json` credentials in `~/.kaggle/`.

### 3. Build and Run the Pipeline

```sh
docker-compose up --build
```

This will:
- Start a PostgreSQL database (`postgres`)
- Run the ETL pipeline as three sequential services:
  - `extract`: Downloads and prepares raw data
  - `transform`: Cleans and transforms data, outputs Parquet
  - `load`: Loads transformed data into PostgreSQL

Data is shared between services via the `data/` directory.

---

## 🧪 Verifying the Pipeline

- Check logs for each service:
  ```sh
  docker-compose logs extract
  docker-compose logs transform
  docker-compose logs load
  ```
- Connect to the database:
  ```sh
  docker exec -it <container_id_of_postgres> psql -U postgres -d fifa_db
  ```
  Then try:
  ```
  \dt
  SELECT * FROM fifa_players LIMIT 10;
  ```

---

## 🧼 Clean Up

```sh
docker-compose down -v  # Stops and removes containers and volumes
```

---

## 🧠 Extending This Project

- Add more ETL transformations (cleaning, feature engineering)
- Create additional microservices for new steps
- Add a FastAPI/Flask service to query enriched data
- Integrate with streaming platforms (Kafka, RabbitMQ)
- Deploy to the cloud (ECS, GKE, Lambda, etc.)

---

## 🤝 Why This Project?

- Demonstrates Python, Docker, and Dask proficiency
- Shows experience with containerized microservices
- Covers database, ETL, and scalable workflow best practices


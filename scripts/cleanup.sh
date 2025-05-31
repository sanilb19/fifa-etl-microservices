#!/bin/bash

# Stop any running containers
echo "Stopping containers..."
docker-compose down

# Remove data directories
echo "Cleaning data directories..."
rm -rf data/raw/*
rm -rf data/processed/*
rm -rf data/kaggle/*

# Remove database volume
echo "Removing database volume..."
docker volume rm etl_with_dask_postgres_data

echo "Cleanup complete!" 
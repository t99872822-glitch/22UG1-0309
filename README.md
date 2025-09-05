# CCS3308 Assignment 1 
# 22UG1-0309 - A.A.T.Lakshan 
# Dockerized Flask + MySQL 


## Deployment Requirements
To deploy and run this application,software installed:
- [Docker](https://docs.docker.com/get-docker/) (Docker Engine)
- [Docker Compose](https://docs.docker.com/compose/) 

## Application Description
This application is a simple **Flask web app** connected to a **MySQL database**.  
- Each time the homepage (`/`) is accessed, the app:
  1. Connects to the MySQL database
  2. Creates a `visits` table (if it doesn’t exist)
  3. Inserts a record with the message *"Hello from Flask!"*
  4. Returns the total number of visits recorded so far  
- This demonstrates **multi-container communication**, **persistent storage**, and a working **Flask + MySQL integration**.
  


## Network and Volume Details
Both services are on the same Docker network (**app-net**). The Flask app connects to MySQL using env vars:
`DB_HOST=db`, `DB_USER=root`, `DB_PASSWORD=example`, `DB_NAME=mydb`.

## Container Configuration
1. **db (MySQL 8.0)**
   - Stores application data
   - Configured with:
     - `MYSQL_ROOT_PASSWORD=example`
     - `MYSQL_DATABASE=mydb`
   - Mounted volume: `/var/lib/mysql` → `db-data`
   - Healthcheck ensures the database is ready before `web` starts

2. **web (Flask App)**
   - Built from `web/Dockerfile`
   - Runs `app.py` with Flask on port `5000`
   - Connects to the database using environment variables:
     - `DB_HOST=db`
     - `DB_USER=root`
     - `DB_PASSWORD=example`
     - `DB_NAME=mydb`

## Container List
- **db**: MySQL database server, persistent storage
- **web**: Flask web application, front-facing service

## Instructions

### Prepare (build images, create volume and network)

## How to run
```bash
chmod +x prepare-app.sh start-app.sh stop-app.sh remove-app.sh
./prepare-app.sh
./start-app.sh
# open http://localhost:5000
```

## Stop / remove
```bash
./stop-app.sh        # keeps data
./remove-app.sh      # removes containers, network, and volume
```

## Verify
```bash
docker compose ps
docker volume ls | grep db-data
docker network ls | grep app-net
```

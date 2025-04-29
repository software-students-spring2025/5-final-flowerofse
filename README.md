![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
![CI Tests](https://github.com/software-students-spring2025/4-containers-excalibur-1/actions/workflows/test.yml/badge.svg)

# Final Project

An exercise to put to practice software development teamwork, subsystem communication, containers, deployment, and CI/CD pipelines. See [instructions](./instructions.md) for details.

---

## Team Members
- **Jialiang Tang**: [Jialiang Tang](https://github.com/JialiangTang1)
- **Haohan Fang**: [FrankFangH](https://github.com/FrankFangH)
- **Haoxuan Lin(Steve)**: [Echoudexigaigu](https://github.com/Echoudexigaigu)
- **Peng Jiang(Victor)**: [PengJiang-Victor](https://github.com/PengJiang-Victor)

---

## Project Overview



---

## Project Structure



---

## Setup Instructions

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Python 3.8+
- [Pipenv](https://pipenv.pypa.io/en/latest/)

---

### 1. Clone the Repository

```
git clone 
cd 
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory. Use the provided`.env.example` file as a reference:

```
MONGO_URI=mongodb://localhost:27017
WEB_APP_PORT=3001
ML_CLIENT_PORT=8000
```

### 3. Start All Services (Run with Docker)

```
docker-compose up --build -d
```

You can access the service through the following link:
- The web app: (http://localhost:3001)
- The ML client: (http://localhost:8000)
- MongoDB database: (http://localhost:27017)

### 4. Start Each Service Independently (Run without Docker)

Run web-app
```
cd 
pip install -r requirements.txt
python app.py
```


### 5. Stop and Clean Up Services
To shut down all running services and clean up resources(consider the large size of client, you may want that), use the following commands:

Stop containers (but keep images and volumes):
```
docker-compose down
```

Stop and remove containers, networks, volumes, and images:

```
docker-compose down --volumes --rmi all
```
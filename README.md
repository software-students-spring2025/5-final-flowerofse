![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
![CI Tests](https://github.com/software-students-spring2025/4-containers-excalibur-1/actions/workflows/test.yml/badge.svg)

# # GameShare.io

A web-based platform where users can register, upload HTML5 games in ZIP format, and interact with other users through comments and game browsing. Users can also view cover images, comment on games.

---

## Team Members
- **Jialiang Tang**: [Jialiang Tang](https://github.com/JialiangTang1)
- **Haohan Fang**: [FrankFangH](https://github.com/FrankFangH)
- **Haoxuan Lin(Steve)**: [Echoudexigaigu](https://github.com/Echoudexigaigu)
- **Peng Jiang(Victor)**: [PengJiang-Victor](https://github.com/PengJiang-Victor)

---

## Project Structure
web_app/app.py  # Main application
web_app/static/uploads/ # Eample html games
web_app/test_app.py # Unit and integration tests


---

## Remote Deployment Site
**Live server:** [http://67.207.80.246:3000/](http://67.207.80.246:3000/)

---

## Local Setup Instructions

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Python 3.8+
- [Pipenv](https://pipenv.pypa.io/en/latest/)

---

### 1. Clone the Repository

```
git clone https://github.com/software-students-spring2025/5-final-flowerofse
cd 5-final-flowerofse
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory. Use the provided`.env.example` file as a reference:

```
MONGO_URI=mongodb://localhost:27017
WEB_APP_PORT=3001
```

### 3. Start All Services (Run with Docker)

```
docker-compose up --build -d
```

You can access the service through the following link:
- The web app: (http://localhost:3001)
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

### 5. Test apps and coverage
To set up the environment, install dependencies, and run automated tests for the project, use the following commands:

```
cd 5-final-flowerofse
pip install pytest pytest-cov
docker-compose up -d
```

To do unit and integration tests:

```
pytest web_app/tests/test_app.py
```

To coverage tests:

```
pytest --cov=web_app
```

To stop services and clean Up, see "Stop and Clean Up Services".
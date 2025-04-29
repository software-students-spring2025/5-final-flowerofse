# web-app/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install only necessary dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

EXPOSE 3000

CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]

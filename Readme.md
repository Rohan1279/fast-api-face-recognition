# FastAPI Face Recognition

This project provides a docker image with a FastAPI backend that uses the `face_recognition` library to detect faces in images. The backend is containerized using Docker.

## Prerequisites

- Docker
- Docker Compose (optional)

## Getting Started

### Build the Docker Image

To build the Docker image, run the following command:

```sh
docker build -t fastapi-face-recognition .
```

## Run the Docker Container

To run the Docker container, use the following command:

```sh
docker run -p 8000:8000 fastapi-face-recognition
```

## Using Docker Compose

Alternatively, you can use Docker Compose to build and run the container.

1. Build and start the services:

```sh
docker-compose up --build
```

2.Stop the services:

```sh
docker-compose down
```

## Test the Endpoint

You can test the /detect-faces/ endpoint using tools like curl, httpie, or Postman.

```sh
curl -X POST "http://localhost:8000/detect-faces/" -F "file=@path/to/your/image.jpg"
```

## Using Postman

1. Open Postman and create a new POST request.
2. Set the URL to http://localhost:8000/detect-faces/.
3. In the "Body" tab, select "form-data".
4. Add a key named file and set its type to "File".
5. Choose the image file you want to upload.
6. Click "Send" to send the request.

## Project Structure

- images/: Contains the images used for testing.
- Dockerfile: Contains the instructions to build the Docker image.
- requirements.txt: Lists the Python dependencies.
- index.py: The main FastAPI application file.
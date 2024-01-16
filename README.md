# EnBW FastAPI Application

## Dockerized Deployment

a) To deploy the application using Docker, use the provided `run_now.sh` script:

```bash
./run_now.sh

This script will build the Docker image named enbw-api and run a container named enbw-api on port 8000.

Access the Swagger API documentation at http://localhost:8000/docs to test the endpoints.

b) Local Development without Docker:

To run the application locally without Docker, make the following changes:

   1) In the main.py file, update the import statement on line 7:
 Change this:
         from api.models import Event, SessionLocal, EventCreate, EventResponse
 To this:
         from models import Event, SessionLocal, EventCreate, EventResponse

2) In the tests.py file, update the import statement on line 4:

 Change this:
        from api.main import app
 To this:
        from main import app

 3) After making these changes, navigate to the api directory:

       if you are in enbw directory user command: cd api

 4) Run the application using Uvicorn:

        terminal command: uvicorn main:app --reload

5) Running Tests

    To run the tests, use the following commands:
        Run tests:
            pytest tests.py

        Run tests with coverage:
            pytest --cov=main tests.py






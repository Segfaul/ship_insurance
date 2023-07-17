# `Ship Insurance`

REST API service to calculate the cost of insurance depending on the type of cargo and declared value.

___

## *Project Status*

***Completed &#10003;***
___
## Functionality
- CRUD operations with insurance ratings via [InsuranceRatesService](https://github.com/Segfaul/ship_insurance/blob/e7b626426f1da6380a3e0aa6dd521f18f009bcfd/database/dbapi.py#L9C29-L95)
- [FastAPI application](https://github.com/Segfaul/ship_insurance/blob/e7b626426f1da6380a3e0aa6dd521f18f009bcfd/app.py#L24-L112) for interaction with the database
- Validation/Error handling

## Technologies and Frameworks
- Python 3.11
- FastAPI
- TortoiseORM
- PostgreSQL
- Docker
___

## Installation

1. Clone the repository to the local machine

    ```shell
    git clone https://github.com/Segfaul/ship_insurance.git
    ```

2. Go to the repository directory

    ```shell
    cd ship_insurance
    ```

3. Create and activate a virtual environment

    ```shell
    python -m venv env
    source env/bin/activate
    ```

4. Set project dependencies

    ```shell
    pip install -r requirements.txt
    ```

5. Configure the configuration file .env

    ```shell
    nano .env
    ```

6. Run the FastAPI app in the background

    ```python
    uvicorn app:app --reload --log-level error
    ```

7. In case of a problem, the program will stop automatically or you can stop execution using

    ```shell
    ps aux | grep ".py"
    kill PID
    ```

8. Also you can build a docker app and run the container

    ```shell
    docker-compose up -d --build
    ```

___

## API endpoints
- **[DELETE]** */insurance/rates/delete* - delete a stack of rates by date or id
- **[PUT]** */insurance/rates/change* - change rate by date/cargo_type/rate
- **[POST]** */insurance/rates/create* - create a new rate recording
- **[POST]** */insurance/rates/upload* - create a new stack of rates by providing .json file
- **[GET]** */insurance/rates* - get list of rates or stack of rates by date
- **[GET]** */insurance/calculate* - get rate calculated on the basis of date and cargo_type
___
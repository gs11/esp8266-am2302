import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone

import psycopg2
from fastapi import FastAPI, Response, status
from pydantic import BaseModel, Field, StrictFloat

app = FastAPI()

DB_HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]


class Am2302SensorReading(BaseModel):
    location: str
    temperature: StrictFloat = Field(ge=-40, le=40)
    humidity: StrictFloat = Field(ge=0, le=100)


class ResponseMessage(BaseModel):
    message: str


db_connection = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_connection
    try:
        db_connection = psycopg2.connect(
            f"host={DB_HOST} dbname={DB_NAME} user={DB_USER} password={DB_PASS}"
        )
        yield
    finally:
        try:
            db_connection.close()
        except Exception:
            pass  # Ignore


def _store_sensor_reading(sensor_reading: Am2302SensorReading):
    with psycopg2.connect(
        f"host={DB_HOST} dbname={DB_NAME} user={DB_USER} password={DB_PASS}"
    ) as db_connection:
        with db_connection.cursor() as db_cursor:
            timestamp = datetime.now(tz=timezone.utc)

            db_cursor.execute(
                "INSERT INTO sensor_reading (location, timestamp, type, value) VALUES (%(location)s, %(timestamp)s, 'temperature', %(value)s)",
                {
                    "location": sensor_reading.location,
                    "timestamp": timestamp,
                    "value": sensor_reading.temperature,
                },
            )

            db_cursor.execute(
                "INSERT INTO sensor_reading (location, timestamp, type, value) VALUES (%(location)s, %(timestamp)s, 'humidity', %(value)s)",
                {
                    "location": sensor_reading.location,
                    "timestamp": timestamp,
                    "value": sensor_reading.humidity,
                },
            )


@app.post("/sensor-readings", status_code=201, response_model=ResponseMessage)
def store_sensor_value(sensor_reading: Am2302SensorReading, response: Response):
    try:
        _store_sensor_reading(sensor_reading=sensor_reading)
        return ResponseMessage(message="OK")
    except Exception as e:
        logging.exception(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ResponseMessage(message="Internal server error")

from fastapi import FastAPI
import logging

import src.requests.upload
import src.requests.students

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(src.requests.upload.router)
app.include_router(src.requests.students.router)

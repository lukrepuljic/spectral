FROM python:3.10.7-alpine3.16

WORKDIR /app

RUN python -m venv .venv
ENV PATH=/app/.venv/bin:${PATH}

COPY ./requirements.txt /app/requirements.txt

RUN /app/.venv/bin/pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

RUN /app/.venv/bin/pip install --no-cache-dir --upgrade -r ./tests/test_requirements.txt
RUN /app/.venv/bin/python -m pytest ./tests --cov --cov-report term


CMD ["/app/.venv/bin/uvicorn", "client:app", "--host", "0.0.0.0", "--port", "8000"]

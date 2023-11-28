FROM python:3.11-slim as builder
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --without dev

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /tmp/requirements.txt .
RUN pip install -r requirements.txt
RUN rm requirements.txt
COPY ./ATL /app/ATL
ENTRYPOINT [ "uvicorn", "atl.main:app", "--host", "0.0.0.0", "--port", "8000" ]
EXPOSE 8000

#docker build . -t atl

# docker run -p 8000:8000 -d atl
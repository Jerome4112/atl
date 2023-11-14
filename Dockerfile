FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev
CMD ["poetry", "run", "uvicorn", "ATL.main:app" , "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000

#docker build . -t atl

# docker run -p 8000:8000 -d atl
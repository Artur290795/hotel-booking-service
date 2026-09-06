FROM python:3.13-slim
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root
COPY . .
ENV PYTHONPATH=/app/src
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
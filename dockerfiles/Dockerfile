FROM python:3.12-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code/

# # Install dependencies
# RUN pip install pipenv
# COPY Pipfile Pipfile.lock /code/
# RUN pipenv install --system --dev

# RUN groupadd -g 1001 tobferadmin && \
#     useradd -u 1001 -g 1001 -m tobferadmin
RUN pip install poetry

RUN apt-get update
RUN apt-get install -y apt-utils build-essential
RUN apt-get install -y libexempi-dev libxslt1-dev
RUN apt-get install -y libgraphviz-dev
RUN apt-get install -y libopencv-dev libgdal-dev
RUN apt-get install -y curl unzip
RUN rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

COPY . /code/

RUN poetry config virtualenvs.create false
RUN poetry install -vvv --no-interaction --no-ansi

# CMD ["uvicorn", "api.fast:app", "--host", "0.0.0.0", "--port", "8081"]
EXPOSE 8081

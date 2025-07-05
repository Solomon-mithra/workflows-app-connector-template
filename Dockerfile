FROM python:3.10-slim-buster
ARG ENVIRONMENT

WORKDIR /usr/src/app

# upgrade to latest pip
RUN pip install --upgrade pip

# Install OS libs needed by cryptography and Google Auth
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    git \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install workflows-cdk package
RUN pip install git+https://github.com/stacksyncdata/workflows-cdk.git@prod

# install dependencies
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# copy the scripts
COPY / .

# expose port
EXPOSE 8080

# set environment variable and start gunicorn
CMD exec gunicorn --preload --bind :8080 --workers 1 --threads 1 --timeout 0 main:app

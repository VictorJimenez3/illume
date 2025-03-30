FROM ubuntu:latest

# Set environment variable to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app
COPY . /app

# Update package lists and install required packages
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip

# Install poetry
RUN curl -sSL https://install.python-poetry.org/ | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry && \
    poetry lock

RUN poetry install

EXPOSE 5000
CMD python3 ./api.py
#how to run:
#docker build -t my-flask-app . 
#docker run -p 5000:5000 my-flask-app
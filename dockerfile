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

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Configure Poetry to not create virtual environments inside containers
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry lock
RUN poetry install --no-interaction --no-ansi

EXPOSE 5000
CMD python3 ./api.py
FROM python:3.12-slim-bullseye as prod

ARG USER_ID='1000'
ARG USER_ID=${USER_ID}
ENV USER_ID ${USER_ID}

ARG GROUP_ID='1000'
ARG GROUP_ID=${GROUP_ID}
ENV GROUP_ID ${GROUP_ID}

RUN apt-get update && apt-get install -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*


RUN pip install poetry==1.4.2

# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

# Installing requirements
RUN poetry install --only main
# Removing gcc
RUN apt-get purge -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*

# Copying actuall application
COPY . /app/src/
RUN poetry install --only main

RUN groupmod -o -g ${GROUP_ID} www-data && \
    usermod -o -u ${USER_ID} -g www-data www-data

CMD ["/usr/local/bin/python", "-m", "app"]

FROM prod as dev

RUN poetry install

FROM python:3.11-slim-buster

WORKDIR /tmp

ARG USER_NAME=vscode
ARG USER_UID
ARG USER_GID
ARG DOCKER_GID

RUN groupadd --gid $USER_GID $USER_NAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USER_NAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USER_NAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USER_NAME \
    && chmod 0440 /etc/sudoers.d/$USER_NAME \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /tmp/* /var/tmp/* \
    && rm -rf /var/lib/apt/lists/*


# Install dev dependences & tools
RUN apt update && apt install -y \
    htop \
    vim \
    git-lfs \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    ssh \
    rsync \
    zsh \
    kmod \
    sudo \
    make \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /tmp/* /var/tmp/* \
    && rm -rf /var/lib/apt/lists/*

RUN update-ca-certificates

ENV SHELL=/usr/bin/zsh
RUN chsh $USER_NAME -s $SHELL

RUN chown -R ${USER_NAME} /root

# Poetry config
ARG POETRY_VERSION
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN chown -R ${USER_NAME} ${POETRY_HOME}
RUN mkdir -p ${POETRY_VENV} && \
    chown -R ${USER_NAME} ${POETRY_VENV}

# Tell Poetry where to place its cache and virtual environment
#ENV POETRY_CACHE_DIR=/opt/.cache

# Creating a virtual environment just for poetry and install it with pip
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install -U pip wheel \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add Poetry to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Copy Dependencies
COPY poetry.lock pyproject.toml ./

RUN touch README.md
# [OPTIONAL] Validate the project is properly configured
RUN poetry check

# Install Dependencies
RUN poetry install --no-interaction --no-cache

USER vscode

RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

ENV PATH=$PATH:/home/vscode/.local/bin

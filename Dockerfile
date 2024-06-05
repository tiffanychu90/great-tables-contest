FROM jupyter/datascience-notebook:python-3.11.6

LABEL org.opencontainers.image.source https://github.com/cal-itp/data-infra

USER root
RUN apt-get update
RUN apt-get install -y ca-certificates curl gnupg
RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list
RUN apt update \
    && apt-get install -y keychain nodejs git-lfs libspatialindex-dev graphviz libgraphviz-dev
# GitHub CLI https://github.com/cli/cli/blob/trunk/docs/install_linux.md
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null
RUN apt update \
    && apt install -y gh


# create these ahead of time, then chown to to the notebook user
ENV POETRY_HOME="/poetry"
RUN mkdir $POETRY_HOME \
    && chown $NB_USER $POETRY_HOME 
USER $NB_UID

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN npm install -g --unsafe-perm=true --allow-root netlify-cli vega-cli vega-lite sql-language-server

COPY ./pyproject.toml /reqs/pyproject.toml
COPY ./poetry.lock /reqs/poetry.lock
RUN poetry config virtualenvs.create false
RUN cd /reqs && poetry install --with=shared_utils --with=portfolio
RUN poetry config virtualenvs.create true

COPY ./profile.sh /tmp/profile.sh
COPY ./jupyter_notebook_config.py /tmp/jupyter_notebook_config.py

FROM python:3.10 as prod

ENV PYTHONUNBUFFERED=1 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE="false"

ENV PATH="${POETRY_HOME}/bin:$PATH"

WORKDIR /app

RUN apt update && \
    apt install make

COPY Makefile poetry.lock pyproject.toml /app/

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN make install-prod

COPY support /app/support

CMD make make-migrations && make migrate && make run-app


# FROM prod as test

# COPY tests/ /app/tests

# RUN make install

# # CMD make code-style-checks && make drf-tests
# CMD make drf-tests









# FROM python as poetry
# RUN curl -sSL https://install.python-poetry.org | python3 -
# COPY . ./
# RUN poetry show --tree
# RUN poetry install --no-root


# FROM python as runtime
# ENV PATH="/app/.venv/bin:$PATH"
# COPY --from=poetry /app /app




# WORKDIR /support

# # Install any needed packages specified in requirements.txt
# # RUN /usr/local/bin/python -m pip install --upgrade pip
# RUN pip install -r requirements.txt
# RUN cd support && ls
# # EXPOSE 8080
# CMD python support/manage.py makemigrations && python support/manage.py migrate && python support/manage.py runserver 0.0.0.0:8000
# # # CMD ["%%CMD%%"]

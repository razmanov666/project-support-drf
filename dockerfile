FROM python:latest

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1
COPY . /support
# Get the Real World example app

# Set the working directory to /drf
# NOTE: all the directives that follow in the Dockerfile will be executed in
# that directory.

# WORKDIR /app
# FROM python as poetry
# ENV POETRY_HOME=/opt/poetry
# ENV POETRY_VIRTUALENVS_IN_PROJECT=true
# ENV PATH="$POETRY_HOME/bin:$PATH"
# RUN curl -sSL https://install.python-poetry.org | python3 -
# COPY . ./
# RUN poetry show --tree
# RUN poetry install


# FROM python as runtime
# ENV PATH="/app/.venv/bin:$PATH"
# COPY --from=poetry /app /app




WORKDIR /support

# Install any needed packages specified in requirements.txt
# RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN cd support && ls
# EXPOSE 8080
CMD python support/manage.py makemigrations && python support/manage.py migrate && python support/manage.py runserver 0.0.0.0:8000
# # CMD ["%%CMD%%"]

FROM python:3.7

# set the working directory in the container
WORKDIR /code

RUN pip install pipenv
COPY Pipfile Pipfile
RUN pipenv install
RUN pipenv install gunicorn

COPY . ./

ARG data=./data/export.csv

COPY ${data} ./data/export.csv

EXPOSE 5000

CMD ["pipenv", "run", "gunicorn", "-w 4", "-b", "0.0.0.0:5000", "api:app"]
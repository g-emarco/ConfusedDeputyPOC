FROM python:3.10-slim
RUN pip install pipenv
WORKDIR /app
COPY Pipfile* /app/
RUN pipenv install --system
COPY . .
# CMD ["python", "app/app.py"]
EXPOSE 8080
CMD flask run -h '0.0.0.0' -p 8080
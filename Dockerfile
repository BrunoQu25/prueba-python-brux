# Se more info here: https://docs.docker.com/language/python/build-images/

# Import Python
FROM python:latest

# Copy application code
COPY . .

# Run main script
CMD [ "python", "./main.py" ]
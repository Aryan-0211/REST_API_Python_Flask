# CONTIBUTING

## How to run Dockerfile locally

docker run -dp 5001:5001 -w /app -v "$(pwd):/app" flask-smorest-api  sh -c "flask run --host 0.0.0.0"

docker build --no-cache -t enbw-api .

docker run -p 8000:8000 enbw-api

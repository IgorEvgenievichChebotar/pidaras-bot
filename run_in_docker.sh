docker build -t pidaras-bot .
docker container rm --force pidaras-bot
docker run -d --restart unless-stopped --name pidaras-bot pidaras-bot
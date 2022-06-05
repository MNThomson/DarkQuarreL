.PHONY: all

PYTHON = python3.10
SNAKE_DIR = src
SNAKE_1 = --name Snake1 --url http://localhost:8080
SNAKE_2 = --name Snake1 --url http://localhost:8000

dev:
	docker run -u 1000:1000 --net=host --gpus=all -e HOME=/project -it --rm -v $$(pwd):/project -w /project tensorman:trainsnattle python3 src/main.py

rngDev:
	$(PYTHON) $(SNAKE_DIR)/snakeGym/rngSnake/server.py

train:
	docker run -u 1000:1000 --net=host --gpus=all -e HOME=/project -it --rm -v $$(pwd):/project -w /project tensorman:trainsnattle python3 src/train.py
	# tensorman ="trainsnattle" run --gpu python3 -- src/train.py

ciTrain:
	docker run --net=host -e HOME=/project -e PORT=8000 -d -v $$(pwd):/project -w /project tensorman:trainsnattle python3 src/snakeGym/rngSnake/server.py
	timeout -k 10 5.25m docker run --net=host -e HOME=/project -i --rm -v $$(pwd):/project -w /project tensorman:trainsnattle python3 src/train.py
	fuser -k 8000/tcp


buildTrainImage:
	docker build -t tensorman:trainsnattle .

cf:
	cloudflared tunnel run

sim:
	battlesnake play $(SNAKE_1) --viewmap -g solo --delay 500 -W 11 -H 11

battle:
	battlesnake play $(SNAKE_1) $(SNAKE_2) --viewmap --delay 50 -W 11 -H 11

demo:
	make dev >/dev/null 2>&1 &

	PORT=8000 make rngDev >/dev/null 2>&1 &

	sleep 2

	make battle
	make killall

killall:
	fuser -k 8080/tcp
	fuser -k 8000/tcp

lint:
	black .
	isort .

cleanlogs:
	rm game/*.json

clean:
	rm -rf .cache .config .keras .nv
	find . -type d -name __pycache__ -exec rm -rf {} \;

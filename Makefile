.PHONY: all

PYTHON = python3.10
SNAKE_DIR = src
SNAKE_1 = --name Snake1 --url http://localhost:8080
SNAKE_2 = --name Snake1 --url http://localhost:8000

dev:
	$(PYTHON) $(SNAKE_DIR)/main.py

cf:
	cloudflared tunnel run

sim:
	battlesnake play $(SNAKE_1) --viewmap -g solo --delay 50 -W 5 -H 5

battle:
	battlesnake play $(SNAKE_1) $(SNAKE_2) --viewmap --delay 50 -W 10 -H 10

initial-setup:
	pip3 install --upgrade pip setuptools
	pip3 install poetry
	poetry init -n
	mkdir .vscode
	touch .vscode/launch.json
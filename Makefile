venv:
	python3 -m venv venv

deps:
	source venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

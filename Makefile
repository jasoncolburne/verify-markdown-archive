venv:
	@python3 -m venv venv

deps: venv
	@pip show keri > /dev/null || (source venv/bin/activate && pip --require-virtualenv install --upgrade pip && pip --require-virtualenv install -r requirements.txt)

verify: deps
	@source venv/bin/activate && ./verify.py ${archive}
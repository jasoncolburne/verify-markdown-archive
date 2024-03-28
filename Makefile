venv:
	@python3 -m venv venv

deps: venv
	@source venv/bin/activate && pip show keri > /dev/null || (pip --require-virtualenv install --upgrade pip && pip --require-virtualenv install -r requirements.txt)

verify: deps
	@source venv/bin/activate && ./verify.py ${archive}
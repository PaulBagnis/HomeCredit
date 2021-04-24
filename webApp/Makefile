requirements:
	venv/bin/pip install -r requirements.txt

db-init:
	rm -rf migrations/
	flask db init
	echo "delete from alembic_version;"

db-push:
	flask db migrate && flask db upgrade

run-dev:
	export FLASK_ENV=development
	flask run
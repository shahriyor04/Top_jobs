mig:
	python manage.py makemigrations
	python manage.py migrate

pull:
	git pull
	mirpolatov
	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

user:
		python manage.py createsuperuser


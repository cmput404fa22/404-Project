### To run in a virtual environment:

1. `virtualenv venv --python=python3`
1. `source venv/bin/activate`
1. `pip install -r requirements.txt`
1. rename `.env.dev -> .env`
1. `python ./social_distribution/manage.py runserver`

### To run in docker:

1. `docker-compose up --build`
1. get a shell in container: `docker compose run --rm web bash`

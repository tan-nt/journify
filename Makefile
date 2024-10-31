env:
	python3 -m venv .venv

activate:
	echo "source env/bin/activate" && echo ". Please copy the line to active the env"

install:
	pip3 install -r requirements.txt

run:
	streamlit run app.py
clear_and_run: clear_generated run diff

run:
	poetry run python xls_converter/main.py "https://assets.beda.software/AU%20Core%20Test%20Data_copy.xlsx" ../../../csiro/au-fhir-test-data/testdata-csv/

clear_generated:
	rm -rf ./testdata-csv

install_dev:
	poetry install

install_prod:
	poetry install --without dev

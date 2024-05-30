install_env:
	pip install -r requirements.txt

quarto_report:
	#quarto render report.ipynb --execute
	quarto convert report.ipynb

install_env:
	pip install -r requirements.txt

process_data:
	#cd scripts/ && python download_data.py
	cd scripts/ && python aggregate.py
    
quarto_report:
	#quarto render report.ipynb --execute
	quarto convert report.ipynb

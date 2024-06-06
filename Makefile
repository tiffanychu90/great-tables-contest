install_env:
	pip install -r requirements.txt

process_data:
	#cd scripts/ && python download_data.py
	cd scripts/ && python aggregate.py
    
quarto_report:
    # this renders as html
	#quarto render report.ipynb --execute 
    # to convert ipynb to qmd
	quarto convert report.ipynb 
    #https://quarto.org/docs/computations/parameters.html#jupyter
	quarto render report.qmd --execute-params params.yml

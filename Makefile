install_env:
	pip install -r requirements.txt

process_data:
	#cd scripts/ && python download_data.py
	cd scripts/ && python aggregate.py
    
quarto_report:
    # this renders as html
	#quarto render hourly_transit_service.ipynb --execute 
    # to convert ipynb to qmd
	quarto convert hourly_transit_service.ipynb 
    #https://quarto.org/docs/computations/parameters.html#jupyter couldn't get this to work
	quarto render report.qmd --execute-params params.yml

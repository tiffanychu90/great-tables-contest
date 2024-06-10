install_env:
	pip install -r requirements.txt
	#quarto add mcanouil/quarto-iconify

process_data:
	#cd scripts/ && python download_data.py
	cd scripts/ && python aggregate.py
    
quarto_report:
    # this renders as html
	#quarto render hourly_transit_service.ipynb --execute 
    # to convert ipynb to qmd
	quarto convert hourly_transit_service.ipynb 
    # to convert qmd to ipynb
	quarto convert hourly_transit_service.qmd     
    #https://quarto.org/docs/computations/parameters.html#jupyter couldn't get this to work
	#quarto render report.qmd --execute-params params.yml
	quarto publish hourly_transit_service.qmd

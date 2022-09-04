a:
	docker container stop mortgage
	
	docker container rm mortgage
	
	docker build --file=Dockerfile --tag mortgage .
	
	docker run -it -p 8888:8888 \
	--name=mortgage \
	mortgage \
	jupyter notebook
	#	python3 pull_data.py

build:
	docker build --file=Dockerfile \
	--tag mortgage .

run:
	docker run -it -p 8888:8888 \
	--name=mortgage \
	mortgage \
	python3 pull_data.py
	# jupyter notebook --ip 0.0.0.0 --port=8888 --no-browser --allow-root

save:
	docker cp <container-id>:explore/Untitled.ipynb ./Untitled.ipynb

stop:
	docker container stop mortgage
	docker container rm mortgage

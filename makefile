a:
	docker container stop mortgage

	docker container rm mortgage

	docker build --file=Dockerfile --tag mortgage .

	docker run -it \
	--name=mortgage \
	mortgage
	# python3 testme.py

build:
	docker build --file=Dockerfile \
	--tag mortgage .

run:
	docker run -it \
	--name=mortgage \
	mortgage
	# python3 testme.py

save:
	docker cp <insert docker image here>:explore/mortgage.ipynb ./mortgage.ipynb

stop:
	docker container stop mortgage
	docker container rm mortgage

notebook:
	docker run -it -p 8888:8888 \
	--name=mortgage \
	mortgage \
	jupyter notebook --ip 0.0.0.0 --port=8888 --no-browser --allow-root
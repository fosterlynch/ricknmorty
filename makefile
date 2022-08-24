build:
	docker build --file=Dockerfile \
	--tag mortgage .

run:
	docker run -it -p 8888:8888 \
	--name=mortgage \
	mortgage \
	jupyter notebook --ip 0.0.0.0 --port=8888 --no-browser --allow-root
save:
	docker cp
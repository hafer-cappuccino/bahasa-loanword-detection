.PHONY: build
build:
	docker build -t loanwords .

.PHONY: run
run:
	docker container run --rm -p 8888:8888 \
    --name loanwords \
    --mount type=bind,source="$(shell pwd)",target=/project loanwords

.PHONY: stop
stop:
	docker container stop loanwords

.PHONY: csv
csv:
	docker container exec -it loanwords bonobo run src/data/etl.py

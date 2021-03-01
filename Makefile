.PHONY: build
build:
	docker build -t loanwords .

.PHONY: run
run:
	docker container run --init --rm -p 8888:8888 \
    --name loanwords \
    --mount type=bind,source="$(shell pwd)",target=/project loanwords

.PHONY: stop
stop:
	docker container stop loanwords

.PHONY: csv
csv:
	docker container exec -it loanwords bonobo run src/data/etl.py

.PHONY: shell
shell:
	docker container run --init --rm \
	--mount type=bind,source="$(shell pwd)",target=/project \
	-i -t loanwords bash

.PHONY: analysis
analysis:
	bonobo run src/data/etl.py && python src/cli/cli.py all

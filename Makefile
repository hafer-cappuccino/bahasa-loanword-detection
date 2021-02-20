.PHONY: build
build:
	docker build -t loanwords .

.PHONY: run
run:
	docker run --rm -p 8888:8888 \
    --name loanwords \
    --mount type=bind,source="$(shell pwd)",target=/project loanwords

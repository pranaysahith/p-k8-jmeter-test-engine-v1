image-name="ggrig/jmeter-c-icap:1.0"

build:
	docker build -t $(image-name) .

run:
	docker run -d $(image-name)

tag:
	docker tag ggrig/jmeter-c-icap ggrig/jmeter-c-icap:1.0	

push:
	docker push ggrig/jmeter-c-icap:1.0

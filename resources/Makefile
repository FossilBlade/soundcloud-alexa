clean:
	rm -rf build

make-build: clean
	mkdir -p build

copy-src:
	cp requirements.txt build/requirements.txt
	cp src/skill.py build/skill.py
	cp src/ssml_builder.py build/ssml_builder.py
	cp src/session_handler.py build/session_handler.py
	cp src/queue_manager.py build/queue_manager.py
	cp src/__init__.py build/__init__.py || touch __init__.py

install-dep:
	pip install -r requirements.txt -t build/.

zip-lambda:
	cd build && rm skill.zip ; zip skill . -r

update-lambda-zip: copy-src zip-lambda

push-to-lm:
	aws lambda --profile lm update-function-code --function-name soundcloud-alexa --zip-file fileb://build/skill.zip

build: make-build copy-src install-dep zip-lambda

update: update-lambda-zip;

deploy-updated: update push-to-lm


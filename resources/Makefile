lambdazip:
	rm -rf build
	mkdir build
	cp lambda/requirements.txt build/requirements.txt
	cp lambda/skill.py build/skill.py
	cp lambda/ssml_builder.py build/ssml_builder.py
	cp lambda/queue_manager.py build/queue_manager.py
	pip install -r lambda/requirements.txt -t build/.
	cd build && zip skill . -r


lambdaupdate:
	rm build/skill.zip
	cp lambda/skill.py build/skill.py
	cp lambda/ssml_builder.py build/ssml_builder.py
	cp lambda/queue_manager.py build/queue_manager.py
	cd build && zip skill . -r
	aws lambda --profile lm update-function-code --function-name alexa-soundcloud --zip-file fileb://build/skill.zip

push-to-lm:
	aws lambda --profile lm update-function-code --function-name alexa-soundcloud --zip-file fileb://build/skill.zip

clean:
	rm -rf build

deploy: lambdazip push-to-lm

update: lambdaupdate
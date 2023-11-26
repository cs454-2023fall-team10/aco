init_submodule:
	git submodule update --init --remote
	cd fitness && git submodule update --init --remote && pip install -r requirements.txt



clean_submodule:
	git submodule deinit --all -f
	rm -rf ./.git/modules
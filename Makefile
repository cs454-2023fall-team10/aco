init_submodule:
	git submodule update --init
	cd fitness && git submodule update --init


clean_submodule:
	git submodule deinit --all -f
	rm -rf ./.git/modules
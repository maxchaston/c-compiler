1:
	./nora-tests/test_compiler compiler_driver.py --chapter 1

2lex:
	./nora-tests/test_compiler compiler_driver.py --chapter 2 --stage lex

2parse:
	./nora-tests/test_compiler compiler_driver.py --chapter 2 --stage lex

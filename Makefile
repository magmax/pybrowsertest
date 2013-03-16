all: tests

tests: tests_remote_firefox tests_remote_chrome

tests_firefox:
	@echo
	@echo ==================== FIREFOX ====================
	./run_tests.py firefox

tests_remote_firefox:
	@echo
	@echo ==================== REMOTE FIREFOX ====================
	./run_tests.py remote firefox

tests_remote_chrome:
	@echo
	@echo ==================== REMOTE CHROME ====================
	./run_tests.py remote chrome


clean:
	${RM} browsertest.cfg

vclean: clean
	find -name "*~" -exec ${RM} {} \;

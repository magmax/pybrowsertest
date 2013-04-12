SELENIUM_SERVER=selenium-server-standalone-2.31.0.jar
CHROME_DRIVER=chromedriver_linux32_26.0.1383.0.zip

all: tests

tests: tests_firefox tests_chrome tests_remote_firefox tests_remote_chrome

tests_firefox:
	@echo
	@echo ==================== FIREFOX ====================
	./run_tests.py firefox

tests_chrome: chromedriver
	@echo
	@echo ==================== CHROME ====================
	PATH=${PATH}:. ./run_tests.py chrome

tests_remote_firefox: ${SELENIUM_SERVER}
	@echo
	@echo ==================== REMOTE FIREFOX ====================
	./run_tests.py remote firefox

tests_remote_chrome: ${SELENIUM_SERVER} chromedriver
	@echo
	@echo ==================== REMOTE CHROME ====================
	PATH=${PATH}:. ./run_tests.py remote chrome

selenium_server_start: ${SELENIUM_SERVER}
	java -jar $< &
	sleep 3

selenium_server_stop:
	pkill -f ${SELENIUM_SERVER}

${SELENIUM_SERVER}:
	wget https://selenium.googlecode.com/files/${SELENIUM_SERVER}

chromedriver:
	wget https://chromedriver.googlecode.com/files/${CHROME_DRIVER}
	unzip ${CHROME_DRIVER}

tests_server:
	python -m SimpleHTTPServer &

clean:
	${RM} browsertest.cfg
	${RM} *.png

vclean: clean
	${RM} ${CHROME_DRIVER} ${SELENIUM_SERVER} chromedriver
	find -name "*~" -exec ${RM} {} \;
	find -name "*.pyc" -exec ${RM} {} \;

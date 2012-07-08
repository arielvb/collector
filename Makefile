UI_DIR='./ui/designer'
BUILD_DIR='./ui/gen'

all: ui2py

run: all
	./bin/gameboard

mac: all
	python setup.py py2app
	bin/macdeployqt dist/main.app

macdebug: all
	#Creates an alias, doesn't copy all the libraries
	python setup.py py2app -A

# create dmg
dmg: mac
	hdiutil create -imagekey zlib-level=9 -srcfolder dist/ -volname collection.dmg

ui2py:
	echo '#' > ${BUILD_DIR}/__init__.py
	pyuic4 -x ${UI_DIR}/mainWindow.ui -o ${BUILD_DIR}/mainWindow.py
	pyuic4 -x ${UI_DIR}/dashboard.ui -o ${BUILD_DIR}/dashboard.py
	pyuic4 -x ${UI_DIR}/fitxa.ui -o ${BUILD_DIR}/fitxa.py
	pyuic4 -x ${UI_DIR}/search_results.ui -o ${BUILD_DIR}/search_results.py
	pyuic4 -x ${UI_DIR}/search_quick.ui -o ${BUILD_DIR}/search_quick.py
	pyrcc4 -o ${BUILD_DIR}/resources_rc.py ${UI_DIR}/resources.qrc

.PHONY: clean
clean:
	find . -name \*.pyc -exec rm {\} \;
	rm $(BUILD_DIR)/*
	rm dist/*

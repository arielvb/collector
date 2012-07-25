UI_DIR='./ui/designer'
BUILD_DIR='./ui/gen'

all: ui2py

run: all
	./collector.py

test:
	python -m unittest discover tests

mac: all
	python setup.py py2app
	bin/macdeployqt dist/Collector.app
	# Remove _debug binaries inside frameworks
	find dist/Collector.app/Contents/Frameworks/ -name *_debug -exec rm {\} \;

macdebug: all
	#Creates an alias, doesn't copy all the libraries
	python setup.py py2app -A

# create dmg
dmg:
	hdiutil create -imagekey zlib-level=9 -srcfolder dist/Collector.app dist/Collector.dmg

# Copiar a la carpeta compartida amb la maquina virtual de windows
copy2win:
	rm -rf ~/Desktop/mv/app
	cp -r ../app ~/Desktop/mv/

ui2py:
	echo '#' > ${BUILD_DIR}/__init__.py
	pyuic4 -x ${UI_DIR}/mainWindow.ui -o ${BUILD_DIR}/mainWindow.py
	pyuic4 -x ${UI_DIR}/dashboard.ui -o ${BUILD_DIR}/dashboard.py
	pyuic4 -x ${UI_DIR}/fitxa.ui -o ${BUILD_DIR}/fitxa.py
	pyuic4 -x ${UI_DIR}/fitxa_edit.ui -o ${BUILD_DIR}/fitxa_edit.py
	pyuic4 -x ${UI_DIR}/search_results.ui -o ${BUILD_DIR}/search_results.py
	pyuic4 -x ${UI_DIR}/search_quick.ui -o ${BUILD_DIR}/search_quick.py
	pyuic4 -x ${UI_DIR}/collection_items.ui -o ${BUILD_DIR}/collection_items.py
	pyrcc4 -o ${BUILD_DIR}/resources_rc.py ${UI_DIR}/resources.qrc

i18n:
	pylupdate4 ui/designer/*.ui -ts translations.ts

.PHONY: clean
clean:
	find . -name \*.pyc -exec rm {\} \;
	rm $(BUILD_DIR)/*
	rm -r dist/*

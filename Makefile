UI_DIR='./ui/designer'
BUILD_DIR='./ui/gen'
EXPORT='./export/'
VM_SHARED=~/Desktop/mv/collector

.PHONY: clean

all: ui2py

run: all
	./collector.py

test:
	clear
	python -m unittest discover tests

mac: all
	python setup.py py2app
	bin/macdeployqt dist/Collector.app
	# Remove _debug binaries inside frameworks
	find dist/Collector.app/Contents/Frameworks/ -name *_debug -exec rm {\} \;

macdebug: all
	#Creates an alias, doesn't copy all the libraries, source changes affects the app
	python setup.py py2app -A

# create dmg
dmg: mac
	hdiutil create -imagekey zlib-level=9 -srcfolder dist/Collector.app dist/Collector.dmg

# Copiar a la carpeta compartida amb la maquina virtual de windows
copy2win: clean
	mkdir -p ${VM_SHARED}
	rm -rf ${VM_SHARED}/
	cp -r ./ ${VM_SHARED}

ui2py: resources
	pyuic4 -x ${UI_DIR}/mainWindow.ui -o ${BUILD_DIR}/mainWindow.py
	pyuic4 -x ${UI_DIR}/dashboard.ui -o ${BUILD_DIR}/dashboard.py
	pyuic4 -x ${UI_DIR}/fitxa.ui -o ${BUILD_DIR}/fitxa.py
	pyuic4 -x ${UI_DIR}/fitxa_edit.ui -o ${BUILD_DIR}/fitxa_edit.py
	pyuic4 -x ${UI_DIR}/search_results.ui -o ${BUILD_DIR}/search_results.py
	pyuic4 -x ${UI_DIR}/search_quick.ui -o ${BUILD_DIR}/search_quick.py
	pyuic4 -x ${UI_DIR}/collection_items.ui -o ${BUILD_DIR}/collection_items.py
	pyuic4 -x ${UI_DIR}/plugins.ui -o ${BUILD_DIR}/plugins.py
	pyuic4 -x ${UI_DIR}/toolbar.ui -o ${BUILD_DIR}/toolbar.py
	pyuic4 -x ${UI_DIR}/topbar.ui -o ${BUILD_DIR}/topbar.py
	pyuic4 -x ${UI_DIR}/properties.ui -o ${BUILD_DIR}/properties.py

resources:
	mkdir -p ${BUILD_DIR}
	echo '#' > ${BUILD_DIR}/__init__.py
	pyrcc4 -o ${BUILD_DIR}/resources_rc.py ${UI_DIR}/resources.qrc
	pyrcc4 -o ${BUILD_DIR}/lang_rc.py ${UI_DIR}/lang.qrc


i18n:
	# Use of the verbose option to see the changes
	pylupdate4 -verbose ui/designer/*.ui ui/views/*.py -ts ${UI_DIR}/lang/es_ES.ts
	pylupdate4 -verbose ui/designer/*.ui ui/views/*.py -ts ${UI_DIR}/lang/ca_ES.ts

release_i18n:
	/Applications/QtSDK/Desktop/Qt/4.8.1/gcc/bin/lrelease ${UI_DIR}/lang/es_ES.ts ${UI_DIR}/lang/ca_ES.ts

gitexport:
	rm -rf ${EXPORT}
	git checkout-index --prefix=${EXPORT} -a
	cd engine; git checkout-index --prefix=../${EXPORT}/engine/ -a


clean:
	find . -name \*.pyc -exec rm {\} \;
	find . -name \*.pyo -exec rm {\} \;
	rm -f $(BUILD_DIR)/*
	rm -rf dist build
	rm -rf ${EXPORT}

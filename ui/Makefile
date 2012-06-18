all: ui2py rc2py

ui2py:
	pyuic4 -x mainWindow.ui -o mainWindow.pyw 
	pyuic4 -x main.ui -o main.pyw
rc2py:
	pyrcc4 -o resources_rc.py resources.qrc

clean:  cleanui cleanrc cleanpyc

cleanpyc:
	rm *.pyc

cleanrc:
	rm resources_rc.py

cleanui: 
	rm *.pyw


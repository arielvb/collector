from PyQt4 import QtCore, QtGui
from ui.gen.toolbar import Ui_Form as CustomToolbarUi, _fromUtf8
from ui.gen.topbar import Ui_Form as TopbarUi


class CustomToolbar(CustomToolbarUi):
    """A custom toolbar with image, text and a URI based callback system"""

    # Template for the link item of the toolbar
    template = (
        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\""
        "\"http://www.w3.org/TR/REC-html40/strict.dtd\">"
        "<html><head><meta name=\"qrichtext\" content=\"1\" />"
        "<style type=\"text/css\">"
        "p, li { white-space: pre-wrap; }"
        "a {text-decoration:none;}"
        "span {text-decoration: none; color:#000000;}"
        "</style></head>"
        "<body style=\"font-family:'Lucida Grande';\""
        "font-size:13pt; font-weight:400; font-style:normal;\">"
        "<p align=\"center\" style=\" margin-top:0px;"
        "margin-bottom:0px; margin-left:0px;"
        "margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
        "<a href=\"collector://%(path)s\"><img src=\"%(image)s\" /><br/>"
        "<span style=\"\">%(title)s</span>"
        "</a></p></body>"
        "</html>")

    def __init__(self, widget, items, callback):
        """ Creates a new toolbar in the QWidget Form and add the items defined
         in the parameter items (array).
         Foreach item in items calls the function self.createItem(item,
                callback)
         """
        super(CustomToolbar, self).__init__()
        self.links = []
        self.widget = widget
        self.setupUi(widget)
        # TODO background or not background?
        # Form.setStyleSheet(
        #    "background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
        #                           stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\
        #                           stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);")
        for i in items:
            self.create_item(i, callback)

    def create_item(self, config, callback):
        """createItem adds a new item to the toolbar, the allowed items are:

            - *link*: a clicable element formed with an image,
                text and uri or path
            - *spacer*: a QSpacer to separete/pull the others items
            - *line*: a vertical line for a visual separation.

        The parameters are config and callback. Callback is the funcition
         called when a toolbar item has been activated, the config parameter
         is a dict and defines the kind of item to add to the toolbar and for
         the link items its params:
            - path: is the value that will be passed to the callback function.
            - name: the text that will appear under the image
            - image: image that will be used for the toolbar item.

        .. note::
            The items spacer/line doesn't have any parameter
        """
        widget = self.widget

        # Link
        if config['class'] == 'link':
            content = self.template % {
                'path': config['path'],
                'title': config['name'],
                'image': config['image']
            }
            item = QtGui.QLabel(widget)
            item.setText(content)
            item.connect(
                item,
                QtCore.SIGNAL(_fromUtf8("linkActivated(QString)")),
                lambda s: callback(s))
        # Spacer
        elif config['class'] == 'spacer':
            item = QtGui.QSpacerItem(
                40,
                20,
                QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum
            )
        # Line
        elif config['class'] == 'line':
            item = QtGui.QFrame(widget)
            item.setFrameShape(QtGui.QFrame.VLine)
            item.setFrameShadow(QtGui.QFrame.Sunken)

        # Store a ref of the item inside the toolbar
        self.links.append(item)

        # Add the item to the container
        if isinstance(item, QtGui.QWidget):
            self.toolbarLinks.addWidget(item)
        else:
            self.toolbarLinks.addItem(item)


class Topbar(TopbarUi):
    """Topbar renders the view header, formed by a icon, title and optionaly
     a description."""

    def __init__(self, widget, icon, title, description=None):
        super(Topbar, self).__init__()
        self.setupUi(widget)
        self.icon.setPixmap(QtGui.QPixmap(_fromUtf8(icon)))
        self.title.setText(title)
        if description is None:
            self.description.hide()
        else:
            self.description.setText(description)

    @QtCore.pyqtSlot(QtCore.QString)
    def set_title(self, text):
        """Sets the topbar title"""
        self.title.setText(text)


class ToolBarManager():
    """ToolBarManager is a wrapper to the default QT toolbar. Isn't used."""
    #TODO what to do whit this class?
    def __init__(self, parent):
        self.parent = parent
        toolbars = {}
        self.parent.setUnifiedTitleAndToolBarOnMac(True)
        toolbar = QtGui.QToolBar("Navigation")
        self.parent.addToolBar(toolbar)
        # Notify unified title and toolbar on mac (displays collapse button at
        #  the right corner)
        toolbars['navigation'] = toolbar
        self.dashToolbarAction = QtGui.QAction(
            QtGui.QIcon(':/dashboard.png'),
            "&Dashboard", self.parent, shortcut="Ctrl+D",
            statusTip="View dashboard",
            triggered=lambda: self.parent.displatView('dashboard'))
        toolbar.addAction(self.dashToolbarAction)
        toolbar = QtGui.QToolBar("Edition")
        toolbars['edition'] = toolbar
        self.editToolbarAction = QtGui.QAction(
            QtGui.QIcon(':/edit.png'),
            "&Edit", self.parent, shortcut="Ctrl+E",
            statusTip="Edit",
            triggered=lambda: self.parent.editFitxa())
        # self.editToolbarAction.setEnabled(False)
        toolbar.addAction(self.editToolbarAction)
        self.toolbars = toolbars

    def hiddeToolBar(self, toolbar):
        self.parent.setUnifiedTitleAndToolBarOnMac(False)
        self.parent.removeToolBar(self.toolbars[toolbar])
        self.parent.setUnifiedTitleAndToolBarOnMac(True)

    def showToolBar(self, toolbar):
        self.parent.setUnifiedTitleAndToolBarOnMac(False)
        # TODO why once deleted the toolbar it is destroyed and it's impossiblo
        #  to show again?
        self.parent.addToolBar(self.toolbars[toolbar])
        self.parent.setUnifiedTitleAndToolBarOnMac(True)

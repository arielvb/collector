# -*- coding: utf-8 -*-
# pylint: disable-msg=E1101,E0611
# E0611: No name 'QtCore' in module 'PyQt4'
# E1101: Module ___ has no ___ member
from collector.ui.gen.collection_items import Ui_Form, _fromUtf8
from PyQt4 import QtCore, QtGui
from collector.ui.helpers.customtoolbar import CustomToolbar, Topbar
from collector.ui.views import Page
from collector.ui.helpers.items import FitxaTableItem, FitxaTableImage


class Ui_Collection(QtGui.QWidget, Ui_Form):

    _table_headers = 0
    _table_items = 0

    def __init__(self, parent, collection, filters=None, flags=None):
        """ Creates a new dashboard view"""
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_Collection, self).__init__(parent, flags)
        self.setupUi(self)
        self.collection = self.parent().collection.get_collection(collection)
        self.schema = self.collection.schema
        if filters is None:
            self.objects = self.collection.get_all()
            self.filters = None
        else:
            self.filters = filters
            self.objects = self.collection.filter(filters)
        self.customize()

    def customize(self):
        """After setup the Ui customize some elements"""
        #Topbar
        icon = self.collection.schema.ico
        if icon is None:
            icon = ':ico/folder.png'
        title = self.collection.get_name().upper()
        if self.filters is not None:
            title += ' ' + self.tr('(filtered)')
        Topbar(widget=self.topbar, icon=icon,
               title=title)

        # Toolbar
        items = [
            {'class':'link', 'name': self.tr('Dashboard'),
             'path': 'view/dashboard', 'image': ':/dashboard.png'},
            {'class': 'spacer'},
            {'class': 'line'},
            {'class':'link', 'name':
             self.tr('Filter'),
             'path': 'view/filters/collection/' + self.collection.get_id(),
             'image': ':/filter.png'},
            {'class':'link', 'name':
             unicode(self.tr('New <b>%s</b>')) % self.collection.get_name(),
             'path': 'view/add/collection/' + self.collection.get_id(),
             'image': ':/add.png'},
        ]
        if self.filters is not None:
            items.insert(
                1,
                {
                    'class': 'link',
                    'name': self.tr('Unfilter'),
                    'path': 'action/unfilter',
                    'image': ':/unfilter.png'
                }
            )
        CustomToolbar(self.toolbar, items, self.uritoaction)
        # +1 (id field)
        order = [i for i, k in self.schema.file.iteritems() if
                 k.class_ != 'ref' and not k.is_multivalue()]
        order = sorted(
            order,
            cmp=lambda x, y: self.schema.order.index(x) >
            self.schema.order.index(y))
        self.tableWidget.setColumnCount(len(order))
        self.tableWidget.setRowCount(len(self.objects))
        if 'image' in order:
            order.remove('image')
            order.insert(0, 'image')
        for item in order:
            field = self.schema.get_field(item)
            self.createHeaderItem(field.name)
        for item in self.objects:
            self.createTableRow(item, self.schema, order)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

        # Connections
        QtCore.QObject.connect(
            self.tableWidget,
            QtCore.SIGNAL("itemDoubleClicked(QTableWidgetItem*)"),
            self._itemSelected)

    def uritoaction(self, uri):
        """Extends the collector uri call adding extra options"""
        params = self.parent().collector_uri_call(uri)

        if params is not None:
            action = params.get('action', None)
            if action == 'unfilter':
                self.parent().display_view('collection', {
                    'collection': self.collection.get_id()
                })

    def createHeaderItem(self, text):
        item = QtGui.QTableWidgetItem()
        item.setText(text)
        self.tableWidget.setHorizontalHeaderItem(self._table_headers, item)
        self._table_headers += 1

    def createTableRow(self, file_, schema, order):
        """ items is a list, and each item of the list can be a string or
        a list """
        row = self._table_items
        column = 0
        items = file_
        for key in order:
            # items = self.collection.load_references(items)
            #TODO allow list elements
            #TODO render images as an image, using
            #  self.tableWidget.setCellWidget
            value = None
            field = schema.get_field(key)
            item = None
            if field.class_ != 'ref' and not field.is_multivalue():
                if key in items:
                    value = items[key]
                field.set_value(value)
                value = field.get_value()
                if value is None:
                    value = ''
                if field.class_ != 'image':
                    item = FitxaTableItem(items['id'])
                    if isinstance(value, (unicode, str)):
                        item.setText(_fromUtf8(value))
                    elif isinstance(value, list):
                        count = len(value)
                        if count > 0:
                            more = count - 1
                            more_text = ''
                            if more > 0:
                                more_text = (
                                    " " +
                                    unicode(self.tr("( %d more)")) %
                                    more)
                            item.setText(unicode(value[0]) + more_text)
                    else:
                        if value is None:
                            value = ''
                        item.setText(_fromUtf8(unicode(value)))
                    self.tableWidget.setItem(row, column, item)

                else:
                    item = FitxaTableImage(items['id'])
                    # item.set_image(value, 64, 64)
                    self.tableWidget.setCellWidget(row, column, item)
            column += 1
        self._table_items += 1

    def _itemSelected(self, tableItem):
        self.parent().display_view(
            'fitxa',
            {'item': tableItem.getObjectId(),
             'collection': self.collection.get_id()})


class CollectionView(Page):

    def get_widget(self, params):
        filters = params.get('filter', None)
        return Ui_Collection(self.parent, collection=params['collection'],
                             filters=filters)

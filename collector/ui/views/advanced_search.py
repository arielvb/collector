# -*- coding: utf-8 -*-
# pylint: disable-msg=E1101,E0611,C0103
# E0611: No name 'QtCore' in module 'PyQt4'
# E1101: Module ___ has no ___ member
"""
Advanced search - Widget and View
=================================

Adavances search is a widget, and a view, that allows build a filter query
to fetch the elements of a collection.

The results are passed to the view *collection*.
"""
from PyQt4 import QtCore, QtGui
from collector.ui.gen.advanced_search import Ui_Form, _fromUtf8
from collector.ui.gen.widget_filter import Ui_Form as Ui_Filter
from collector.ui.helpers.customtoolbar import CustomToolbar, Topbar
from collector.ui.widgetprovider import WidgetProvider


class FilterWidget(QtGui.QWidget, Ui_Filter):
    """Widget for fitlers"""

    def __init__(self, fields, filters, value=None, parent=None):
        super(FilterWidget, self).__init__(parent)
        self.fields = fields
        self.filter = None
        self.filters = filters
        self.value = value
        self.setupUi(self)

    def setupUi(self, form):
        super(FilterWidget, self).setupUi(form)
        self.value_combo.hide()
        self.union_combo.hide()
        for i in self.fields:
            self.field_combo.addItem(i.name)
        for i in self.filters:
            self.filter_combo.addItem(i.get_name())


class AdvancedSearchWidget(QtGui.QWidget, Ui_Form):
    """The Adavanced Search Widget"""

    def __init__(self, query, parent, collection=None, flags=None):
        if flags is None:
            super(AdvancedSearchWidget, self).__init__(parent)
        else:
            super(AdvancedSearchWidget, self).__init__(parent, flags)
        self.query = query
        self.filters = None
        self.fields = None
        self.filters_w = []
        self.collection = collection
        self.setupUi()

    def setupUi(self):
        super(AdvancedSearchWidget, self).setupUi(self)
        collections = self.parent().collection.collections
        if len(collections) > 0:
            # If the constructor has set a collection, it will be the id
            #  otherwise we use the first collection
            if self.collection is None:
                self.collection = collections.itervalues().next()
            else:
                self.collection = collections[self.collection]
        i = 0
        for col in collections.values():
            self.collections_combo.addItem(_fromUtf8(col.get_name()))
            if col == self.collection:
                self.collections_combo.setCurrentIndex(i)
            i += 1

        fields = self.collection.schema.file.values()
        fields.sort(cmp=lambda x, y: cmp(x.name, y.name))
        self.fields = fields
        self.filters = self.collection.persistence.get_filters().values()
        filter_ = FilterWidget(self.fields, self.filters)
        self.filters_w.append(filter_)
        self.filters_layout.addWidget(filter_)
        Topbar(widget=self.topbar, icon=':ico/search.png',
               title=self.tr("Advanced Search"))
        # Toolbar
        items = [
            {'class':'link', 'name': self.tr('Dashboard'),
             'path': 'view/dashboard', 'image': ':/dashboard.png'},
            {'class': 'spacer'},
            {'class': 'line'},
            {'class':'link', 'name':
             str(self.tr('Filter')),
             'path': 'action/dofilter',
             'image': ':/done.png'},
        ]
        CustomToolbar(self.toolbar, items, self._toolbar_callback)

        self.add_button.clicked.connect(self.addfilter)

    def _toolbar_callback(self, uri):
        """Toolbar actions callback"""
        params = self.parent().collector_uri_call(uri)
        if params is not None:
            action = params.get('action', None)
            if action == 'dofilter':
                query = []
                for i in self.filters_w:
                    index = i.filter_combo.currentIndex()
                    index2 = i.field_combo.currentIndex()

                    query.append({
                        self.filters[index].get_id(): [
                            self.fields[index2].get_id(),
                            unicode(i.value_text.text().toUtf8())
                        ]
                    })
                self.parent().display_view(
                    'collection',
                    params={
                    'collection': self.collection.get_id(),
                    'filter': query
                    }
                )

    @QtCore.pyqtSlot()
    def addfilter(self):
        """Adds a empty filter to de filter query"""
        # TODO whe need to store the filters...
        filterw = FilterWidget(self.fields, self.filters)
        self.filters_w.append(filterw)
        self.filters_layout.addWidget(filterw)


class AdvancedSearch(WidgetProvider):
    """AdvancedSearch view, is a centralwidget view"""

    def get_widget(self, params):
        query = None
        collection = None
        if params is not None:
            query = params.get('query', None)
            collection = params.get('collection', None)
        widget = AdvancedSearchWidget(query, self.parent, collection)
        return widget

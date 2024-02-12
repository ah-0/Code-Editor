import os
from PySide import QtCore, QtGui
# display a root directory QFileSystemModel

class FileProxyModel(QtGui.QSortFilterProxyModel):
    def setIndexPath(self, index):
        self._index_path = index
        self.invalidateFilter()

    def filterAcceptsRow(self, sourceRow, sourceParent):
        if hasattr(self, "_index_path"):
            ix = self.sourceModel().index(sourceRow, 0, sourceParent)
            if self._index_path.parent() == sourceParent and self._index_path != ix:
                return False
        return super(FileProxyModel, self).filterAcceptsRow(sourceRow, sourceParent)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    path = # ...
    parent_dir = os.path.abspath(os.path.join(path, os.pardir))
    treeview = QtGui.QTreeView()
    model = QtGui.QFileSystemModel(treeview)
    model.setRootPath(QtCore.QDir.rootPath())
    proxy = FileProxyModel(treeview)
    proxy.setSourceModel(model)
    proxy.setIndexPath(QtCore.QPersistentModelIndex(model.index(path)))
    treeview.setModel(proxy)
    treeview.setRootIndex(proxy.mapFromSource(model.index(parent_dir)))
    treeview.expandAll()
    treeview.show()
    sys.exit(app.exec_()

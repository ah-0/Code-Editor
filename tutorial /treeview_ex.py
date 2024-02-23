import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# display a root directory QFileSystemModel

class FileProxyModel(QSortFilterProxyModel):
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
    app = QApplication(sys.argv)
    path = os.getcwd()
    parent_dir = os.path.abspath(os.path.join(path, os.pardir))
    treeview = QTreeView()
    model = QFileSystemModel(treeview)
    model.setRootPath(path)
    proxy = FileProxyModel(treeview)
    proxy.setSourceModel(model)
    proxy.setIndexPath(QPersistentModelIndex(model.index(path)))
    treeview.setModel(proxy)
    treeview.setRootIndex(proxy.mapFromSource(model.index(parent_dir)))
    treeview.expandAll()
    treeview.show()
    sys.exit(app.exec_())
    
    
    QModelIndex index2=proxymodel->mapToSource(index); 
//Returns the source model index (In my case it was QFileSystemModel)
QString selectedrow=filemodel->fileInfo(index2).absoluteFilePath();
//

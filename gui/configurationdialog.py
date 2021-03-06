#-----------------------------------------------------------
#
# Big Search is a QGIS plugin to perform text-search over
# all intended layers and using QGIS expressions to allow advanced
# search. This is comparable to what is done in web-mapping clients.
#
# Copyright    : (C) 2014 Denis Rouzaud
# Email        : denis.rouzaud@gmail.com
#
#-----------------------------------------------------------
#
# licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this progsram; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#---------------------------------------------------------------------

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QTableWidgetItem, QTableWidgetSelectionRange
from qgis.gui import QgsOptionsDialogBase

from ..core.layerentriesregistry import LayerEntriesRegistry
from layerentrydialog import LayerEntryDialog
from ..ui.ui_configuration import Ui_Configuration


class ConfigurationDialog(QgsOptionsDialogBase, Ui_Configuration):
    def __init__(self, iface):
        QgsOptionsDialogBase.__init__(self, "BigSearch", iface.mainWindow())
        self.setupUi(self)
        self.initOptionsBase(False)
        self.restoreOptionsBaseUi()
        self.layerEntryRegistry = LayerEntriesRegistry()
        self.layerEntries = LayerEntriesRegistry.read()
        self.showLines()

    def accept(self):
        self.layerEntryRegistry.save(self.layerEntries)
        QgsOptionsDialogBase.accept(self)

    @pyqtSlot(name="on_layerAddButton_pressed")
    def addLayer(self):
        self.layerEntryDlg = LayerEntryDialog()
        if not self.layerEntryDlg.exec_():
            return
        layerEntry = self.layerEntryDlg.getEntry()
        if layerEntry is not None:
            self.layerEntries.append(layerEntry)
        self.showLines()

    @pyqtSlot(name="on_layerRemoveButton_pressed")
    def removeLayer(self):
        selItems = self.tableWidget.selectedItems()
        if len(selItems) == 0:
            return
        row = selItems[0].row()
        self.layerEntries.pop(row)
        self.showLines()

    @pyqtSlot(name="on_layerEditButton_pressed")
    def editLayer(self):
        selItems = self.tableWidget.selectedItems()
        if len(selItems) == 0:
            return
        row = selItems[0].row()
        self.layerEntryDlg = LayerEntryDialog(self.layerEntries[row])
        if not self.layerEntryDlg.exec_():
            return
        self.layerEntries.pop(row)
        layerEntry = self.layerEntryDlg.getEntry()
        if layerEntry is not None:
            self.layerEntries.insert(row, layerEntry)
        self.showLines()

    @pyqtSlot(name="on_layerUpButton_pressed")
    def layerUp(self):
        selItems = self.tableWidget.selectedItems()
        if len(selItems) == 0:
            return
        row = selItems[0].row()
        if row == 0:
            return
        self.layerEntries[row-1], self.layerEntries[row] = self.layerEntries[row], self.layerEntries[row-1]
        self.showLines()
        self.tableWidget.setRangeSelected(QTableWidgetSelectionRange(row-1, 0, row-1, 3), True)

    @pyqtSlot(name="on_layerDownButton_pressed")
    def layerDown(self):
        selItems = self.tableWidget.selectedItems()
        if len(selItems) == 0:
            return
        row = selItems[0].row()
        if row == len(self.layerEntries)-1:
            return
        self.layerEntries[row+1], self.layerEntries[row] = self.layerEntries[row], self.layerEntries[row+1]
        self.showLines()
        self.tableWidget.setRangeSelected(QTableWidgetSelectionRange(row+1, 0, row+1, 3), True)

    def showLines(self):
        self.tableWidget.clearContents()
        for r in range(self.tableWidget.rowCount() - 1, -1, -1):
            self.tableWidget.removeRow(r)
        for layerEntry in self.layerEntries:
            layer = layerEntry.layer()
            if layer is None:
                continue
            r = self.tableWidget.rowCount()
            self.tableWidget.insertRow(r)

            self.tableWidget.setItem(r, 0, QTableWidgetItem(layer.name()))
            self.tableWidget.setItem(r, 1, QTableWidgetItem(layerEntry.expression))
            if layerEntry.useFeatureGeom:
                self.tableWidget.setItem(r, 2, QTableWidgetItem("feature"))
            else:
                self.tableWidget.setItem(r, 2, QTableWidgetItem("expression"))













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


from PyQt4.QtGui import QDialog, QDialogButtonBox

from ..qgiscombomanager import VectorLayerCombo, ExpressionFieldCombo
from ..core.layerentry import LayerEntry
from ..ui.ui_layerentry import Ui_LayerEntry


class LayerEntryDialog(QDialog, Ui_LayerEntry):
    def __init__(self, layerEntry=None):
        QDialog.__init__(self)
        self.setupUi(self)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        self.layerComboManager = VectorLayerCombo(self.layerCombobox)
        self.searchComboManager = ExpressionFieldCombo(self.searchCombobox, self.searchExpressionButton, self.layerComboManager)
        self.xComboManager = ExpressionFieldCombo(self.xCombobox, self.xExpressionButton, self.layerComboManager)
        self.yComboManager = ExpressionFieldCombo(self.yCombobox, self.yExpressionButton, self.layerComboManager)

        self.layerCombobox.currentIndexChanged.connect(self.enableOkButton)
        self.searchCombobox.currentIndexChanged.connect(self.enableOkButton)
        self.xCombobox.currentIndexChanged.connect(self.enableOkButton)
        self.yCombobox.currentIndexChanged.connect(self.enableOkButton)
        self.zoomToFeatureRadio.clicked.connect(self.enableOkButton)
        self.zoomToExpressionRadio.clicked.connect(self.enableOkButton)

        if layerEntry is not None:
            self.layerComboManager.setLayer(layerEntry.layer())
            self.searchComboManager.setExpression(layerEntry.expression)
            self.zoomToFeatureRadio.setChecked(layerEntry.useFeatureGeom)
            self.zoomToExpressionRadio.setChecked(not layerEntry.useFeatureGeom)
            self.xComboManager.setExpression(layerEntry.xExpression)
            self.yComboManager.setExpression(layerEntry.yExpression)

    def enableOkButton(self, *args):
        isValid, layerEntry = self.checkEntry()
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(isValid)

    def checkEntry(self):
        layer = self.layerComboManager.getLayer()
        if layer is None:
            return False, None
        expr = self.searchComboManager.getExpression()
        if expr == "":
            return False, None
        useFeatureGeom = self.zoomToFeatureRadio.isChecked()
        if useFeatureGeom:
            return True, LayerEntry(layer.id(), expr, True)
        else:
            xExpr = self.xComboManager.getExpression()
            yExpr = self.yComboManager.getExpression()
            if xExpr == "" or yExpr == "":
                return False, None
            return True, LayerEntry(layer.id(), expr, False, xExpr, yExpr)

    def getEntry(self):
        isValid, layerEntry = self.checkEntry()
        return layerEntry

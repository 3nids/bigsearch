#-----------------------------------------------------------
#
# Global Finder is a QGIS plugin to perform text-search over
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

from PyQt4.QtCore import pyqtSignal
from qgis.core import QgsFindFeaturesByExpressionThread, QgsFeature, QgsVectorLayer, QgsExpression

from layerentriesregistry import LayerEntriesRegistry


class SearchProcess():
    featureFound = pyqtSignal(QgsVectorLayer, QgsFeature)

    def __init__(self):
        self.trheads = []

    def newSearch(self, searchText):
        self.stopCurrentSearch()

        for layerEntry in LayerEntriesRegistry.read():
            thread = QgsFindFeaturesByExpressionThread(layerEntry.layer(), searchText, QgsExpression(layerEntry.expression))
            thread.featureFound.connect(self.featureFound2)
            self.trheads.append(thread)
            thread.start()

    def featureFound2(self, layer, feature):
        print layer.id(), feature.id()
        self.featureFound.emit(layer, feature)

    def stopCurrentSearch(self):
        for thread in self.trheads:
            thread.stop()
        self.trheads = []


layer = QgsMapLayerRegistry.instance().mapLayer("district20140108113728427")
expr = QgsExpression("id")
from __future__ import print_function
slot = lambda vl, f : print(vl.id(), f.id())
thread = QgsFindFeaturesByExpressionThread(layer, "1", expr)
thread.featureFound.connect()
thread.start()

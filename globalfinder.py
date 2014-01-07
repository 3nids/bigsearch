#-----------------------------------------------------------
#
# Intersect It is a QGIS plugin to place observations (distance or orientation)
# with their corresponding precision, intersect them using a least-squares solution
# and save dimensions in a dedicated layer to produce maps.
#
# Copyright    : (C) 2013 Denis Rouzaud
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


from PyQt4.QtCore import QUrl, QCoreApplication, QFileInfo, QSettings, QTranslator
from PyQt4.QtGui import QAction, QIcon, QDesktopServices
from qgis.core import QgsApplication

from core.memorylayers import MemoryLayers

from gui.mysettingsdialog import MySettingsDialog
from gui.dimensioneditmaptool import DimensionEditMapTool
from gui.distancemaptool import DistanceMapTool
from gui.orientationmaptool import OrientationMapTool
from gui.advancedintersectionmaptool import AdvancedIntersectionMapTool
from gui.simpleintersectionmaptool import SimpleIntersectionMapTool

import resources


class GlobalFinder ():
    def __init__(self, iface):
        self.iface = iface

        # Initialise the translation environment.
        userPluginPath = QFileInfo(QgsApplication.qgisUserDbFilePath()).path()+"/python/plugins/globalfinder"
        systemPluginPath = QgsApplication.prefixPath()+"/share/qgis/python/plugins/globalfinder"
        locale = QSettings().value("locale/userLocale")
        myLocale = locale[0:2]
        if QFileInfo(userPluginPath).exists():
            pluginPath = userPluginPath+"/i18n/globalfinder_"+myLocale+".qm"
        elif QFileInfo(systemPluginPath).exists():
            pluginPath = systemPluginPath+"/i18n/globalfinder_"+myLocale+".qm"
        self.localePath = pluginPath
        if QFileInfo(self.localePath).exists():
            self.translator = QTranslator()
            self.translator.load(self.localePath)
            QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        # dock
        self.dockAction = QAction(QIcon(":/plugins/globalfinder/icons/globalfinder.svg"), "Global Finder",
                                  self.iface.mainWindow())
        self.dockAction.setCheckable(True)
        self.dockAction.triggered.connect(self.dock.setVisible)
        self.iface.addPluginToMenu("&Global Finder", self.dockAction)
        self.iface.addToolBarIcon(self.dockAction)
        self.dock.visibilityChanged.connect(self.dockAction.setChecked)
        # settings
        self.settingsAction = QAction(QIcon(":/plugins/globalfinder/icons/settings.svg"), "Settings",
                                      self.iface.mainWindow())
        self.settingsAction.triggered.connect(self.showSettings)
        self.iface.addPluginToMenu("&Global Finder", self.settingsAction)
        # help
        self.helpAction = QAction(QIcon(":/plugins/globalfinder/icons/help.svg"), "Help", self.iface.mainWindow())
        self.helpAction.triggered.connect(lambda: QDesktopServices().openUrl(QUrl("http://io.github.com/3nids/globalfinder/")))
        self.iface.addPluginToMenu("&Global Finder", self.helpAction)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("&Global Finder", self.dockAction)
        self.iface.removePluginMenu("&Global Finder", self.helpAction)
        self.iface.removePluginMenu("&Global Finder", self.settingsAction)
        self.iface.removeToolBarIcon(self.dockAction)

    def showSettings(self):
        MySettingsDialog().exec_()
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

from qgis.core import QgsProject

from layerentry import LayerEntry

class LayerEntriesRegistry():

    @staticmethod
    def save(entries):
        project = QgsProject.instance()
        # delete previous version
        projectEntries = project.entryList("bigsearch", "")
        i = 0
        while True:
            varName = "layerEntry_%u" % i
            if varName not in projectEntries:
                break
            project.removeEntry("bigsearch", varName)
            i += 1
        # save lines
        i = 0
        for entry in entries:
            entryData = [entry.layerid, entry.expression,
                         str(entry.useFeatureGeom), entry.xExpression, entry.yExpression]
            project.writeEntry("bigsearch", "layerEntry_%u" % i, entryData)
            i += 1

    @staticmethod
    def read():
        project = QgsProject.instance()
        projectEntries = project.entryList("bigsearch", "")
        i = 0
        entries = []
        while True:
            varName = "layerEntry_%u" % i
            if varName not in projectEntries:
                break
            entryData = project.readListEntry("bigsearch", varName)[0]
            entry = LayerEntry(entryData[0], entryData[1], bool(entryData[2]), entryData[3], entryData[4])
            entries.append(entry)
            i += 1
        return entries










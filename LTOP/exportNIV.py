from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QListWidgetItem, 
    QPushButton, QHBoxLayout, QLabel
)
from qgis.PyQt.QtCore import Qt
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterFileDestination,
    QgsProcessingException,
    QgsProcessing
)
import math
import pandas as pd
import os

def right_pad(text: str, width: int) -> str:
    if len(text) > width: return text[:width]
    return text + " "*(width - len(text))

def number_pad(number: float, int_width: int, float_width: int) -> str:
    total_width = int_width + 1 + float_width
    return f"{number:>{total_width}.{float_width}f}"

def epoch() -> str:
    return " "*4

class MultiSelectDialog(QDialog):
    """Simple dialog with check boxes for point selection."""
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Points of Interest")
        self.resize(400, 500)
        
        # Layouts
        layout = QVBoxLayout(self)
        
        # Label
        self.label = QLabel("Select Points of Interest:", self)
        layout.addWidget(self.label)
        
        # List with check boxes
        self.list_widget = QListWidget(self)
        for item in items:
            list_item = QListWidgetItem(item, self.list_widget)
            list_item.setFlags(list_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            list_item.setCheckState(Qt.CheckState.Unchecked)
            self.list_widget.addItem(list_item)
        layout.addWidget(self.list_widget)
        
        # Buttons for quick selection (Alle / Keine)
        btn_layout_select = QHBoxLayout()
        self.btn_all = QPushButton("Select all", self)
        self.btn_none = QPushButton("Select none", self)
        self.btn_all.clicked.connect(self.select_all)
        self.btn_none.clicked.connect(self.select_none)
        btn_layout_select.addWidget(self.btn_all)
        btn_layout_select.addWidget(self.btn_none)
        layout.addLayout(btn_layout_select)
        
        # standard OK / Cancel buttons
        btn_layout_action = QHBoxLayout()
        self.btn_ok = QPushButton("OK", self)
        self.btn_cancel = QPushButton("Cancel", self)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        btn_layout_action.addWidget(self.btn_ok)
        btn_layout_action.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout_action)

    def select_all(self):
        for i in range(self.list_widget.count()):
            self.list_widget.item(i).setCheckState(Qt.CheckState.Checked)

    def select_none(self):
        for i in range(self.list_widget.count()):
            self.list_widget.item(i).setCheckState(Qt.CheckState.Unchecked)

    def get_checked_items(self):
        checked = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                checked.append(item.text())
        return checked


class SelectFromPtAlgorithm(QgsProcessingAlgorithm):
    INPUT_LAYER = 'INPUT_LAYER'
    OUTPUT_FILE = 'OUTPUT_FILE'
    
    def name(self):
        return 'export_LTOP_NIV'

    def displayName(self):
        return 'LTOP-MES LEVEL Exporter'

    def group(self):
        return 'LTOP Formate'

    def groupId(self):
        return 'swiss_formats'

    def createInstance(self):
        return SelectFromPtAlgorithm()

    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.FlagNoThreading

    def shortHelpString(self):
        return '''Dieses Skript exportiert Nivellement-Messungen aus einem Layer direkt in das von LTOP lesbare *.mes-Format.
        
        Als Input wird ein Layer erwartet, welcher die Attribute ```FromPt```, ```ToPt```, ```DeltaH``` und ```StdDH``` enthält. Nach dem Ausführen werden Sie aufgefordert, ```Points of Interest``` auszuwählen - wählen Sie hier alle Punkte, welche nicht einfache ```Umsteller``` sind.
        Eine detailliertere Beschreibung des Algorithmus finden Sie hier: https://github.com/FabianRuefenacht/QGeoProcessing#-ltop-niv-exporter-exportnivpy'''

    def initAlgorithm(self, config=None):
        # (merged) Niv-lines
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_LAYER,
                'Select Input Layer',
                [QgsProcessing.TypeVector]
            )
        )

        # output file
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT_FILE,
                'Output MES File',
                'MES-Dateien (*.mes)'
            )
        )
        
    def icon(self):
        svg_data = '''
        <svg width="500" height="500" xmlns="http://www.w3.org/2000/svg">
         <g id="Layer_1">
          <title>Layer 1</title>
          <text transform="matrix(1 0 0 1 0 0)" font-weight="bold" xml:space="preserve" text-anchor="start" font-family="'Assistant'" font-size="200" stroke-width="0" id="svg_4" y="323.50001" x="62.39844" stroke="#00ff11" fill="#ff0011">MES</text>
         </g>
        </svg>'''
        
        from qgis.PyQt.QtGui import QPixmap, QIcon
        pixmap = QPixmap()
        pixmap.loadFromData(svg_data.encode('utf-8'), 'SVG')
        return QIcon(pixmap)
    
        
    def processAlgorithm(self, parameters, context, feedback):
            # in layer
            layer = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)
            if not layer:
                raise QgsProcessingException('Invalid Input Layer.')
            
            # out path
            output_path = self.parameterAsFileOutput(parameters, self.OUTPUT_FILE, context)
            if not output_path:
                raise QgsProcessingException('No output file path specified.')
            
            from_idx = layer.fields().indexOf('FromPt')
            to_idx = layer.fields().indexOf('ToPt')
            
            if from_idx == -1 or to_idx == -1:
                raise QgsProcessingException('Layer must contain the columns "FromPt" and "ToPt"!')
                
            unique_from = layer.uniqueValues(from_idx)
            unique_to = layer.uniqueValues(to_idx)
            
            all_unique_values = set(unique_from).union(set(unique_to))
            sorted_values = sorted([str(val) for val in all_unique_values if val is not None])
            
            if not sorted_values:
                raise QgsProcessingException('Neither "FromPt" nor "ToPt" contain entries.')

            # Open point selection dialog
            dialog = MultiSelectDialog(sorted_values)
            if dialog.exec():
                poi = dialog.get_checked_items()
            else:
                raise QgsProcessingException('Selection aborted by user.')
                
            if not poi:
                raise QgsProcessingException('No points have been selected.')

            feedback.pushInfo(f"Selected ({len(poi)} Points): {', '.join(poi)}")
            
            # layer attributes to df
            field_names = [field.name() for field in layer.fields()]
            data = [feat.attributes() for feat in layer.getFeatures()]
            
            df = pd.DataFrame(data, columns=field_names)
            
            # create the *.MES-file
            linestart = None
            obsstart = None
            dh = 0
            behind_one_dh = 0
            var = 0
            last_var = 0
            current_line = None

            mes = "$$MENIV Converted with 'LTOP-MES LEVEL Exporter' (Ruefenacht, 2026)\n"
            mes += "**Rüfenacht, F. (2026). QGeoProcessing: QGIS Processing Tools for Geodetic Networks\n"
            mes += "**(Version 1.0.0) [Computer software]. https://github.com/FabianRuefenacht/QGeoProcessing\n"

            for idx, row in df.iterrows():
                start = row["FromPt"]
                end = row["ToPt"]
                delta = row["DeltaH"]
                std = row["StdDH"]
                
                try:
                    comment = row["Comment"]
                except:
                    comment = "Not named"
                    
                if not current_line == comment:
                    mes += "**Line " + str(comment) + "\n"
                    current_line = comment
                    dh = 0
                    var = 0
                    linestart = None
                    obsstart = None
                
                if start in poi:
                    linestart = start
                    dh = 0
                    var = 0
                    behind_one_dh = 0
                    last_var = 0
                    
                if linestart is None:
                    linestart = start
                    obsstart = start
                    dh += delta
                    var += std**2
                    
                elif obsstart == start:
                    dh = behind_one_dh + delta
                    var = last_var + std**2
                    
                elif obsstart != start:
                    obsstart = start
                    behind_one_dh = dh
                    dh += delta
                    last_var = var
                    var += std**2

                if end in poi:
                    mes += "ST" + right_pad(str(linestart), 10) + "\n"
                    mes += "DH" + right_pad(str(end), 10) + epoch() + number_pad(dh, 14, 5) + number_pad(var**0.5*1000, 2, 3) + "\n"

            # write out file
            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(mes)
                feedback.pushInfo(f"Successfully saved file to: {output_path}")
            except Exception as e:
                raise QgsProcessingException(f"Failed to write file: {str(e)}")

            return {'OUTPUT_FILE': output_path, 'SELECTED_VALUES': poi}
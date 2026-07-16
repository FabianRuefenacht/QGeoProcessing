from qgis.core import (QgsProcessingAlgorithm, QgsProcessingParameterFile, 
                       QgsFields, QgsField, QgsFeature, QgsGeometry, 
                       QgsPointXY, QgsVectorLayer, QgsProject)
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtGui import QIcon, QPixmap
import os
import csv

class ImportLtopKoo(QgsProcessingAlgorithm):
    FILE_INPUT = 'INPUT'

    def tr(self, string):
        return string

    def createInstance(self):
        return ImportLtopKoo()

    def name(self):
        return 'import_infinity_niv'

    def displayName(self):
        return self.tr('Infinity-NIV Importer')

    def group(self):
        return self.tr('Infinity Formate')

    def groupId(self):
        return 'infinity_formats'

    def mainMenuCommand(self):
        return 'QGeoProcessing'

    def shortHelpString(self):
        return 'Dieses Skript importiert Nivellement-Messungen aus einer CSV-Datei und zeichnet Linien zwischen den Punkten.'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFile(
                self.FILE_INPUT,
                self.tr('Infinity CSV-Datei (.csv)'),
                extension='csv'
            )
        )
        
    def icon(self):
        svg_data = '''
        <svg width="500" height="500" xmlns="http://www.w3.org/2000/svg">
         <g id="Layer_1">
          <title>Layer 1</title>
          <text transform="matrix(1 0 0 1 0 0)" font-weight="bold" xml:space="preserve" text-anchor="start" font-family="'Assistant'" font-size="200" stroke-width="0" id="svg_5" y="323.33334" x="106.77499" stroke="#00ff00" fill="#7fff00">NIV</text>
         </g>
        </svg>'''
        
        pixmap = QPixmap()
        pixmap.loadFromData(svg_data.encode('utf-8'), 'SVG')
        
        return QIcon(pixmap)

    def processAlgorithm(self, parameters, context, feedback):
        file_path = self.parameterAsFile(parameters, self.FILE_INPUT, context)
        
        # Attributes for table
        fields = QgsFields()
        fields.append(QgsField("FromPt", QVariant.String))
        fields.append(QgsField("ToPt", QVariant.String))
        fields.append(QgsField("DeltaH", QVariant.Double))
        fields.append(QgsField("StdDH", QVariant.Double))
        
        # Init LineString Layer
        vl = QgsVectorLayer("LineString?crs=EPSG:2056", os.path.basename(file_path), "memory")
        provider = vl.dataProvider()
        provider.addAttributes(fields)
        vl.updateFields()
        
        features = []
        
        def to_float(x: str) -> float:
            """
            Helper function to convert str to float.
            ValueError Exception converts "-" to 0.0.
            """
            try: return float(x)
            except ValueError: return 0.0

        def make_line(start_name: str, end_name: str, delta_h: float, std_dh: float, start_e: float, start_n: float, end_e: float, end_n: float) -> QgsFeature:
            """
            Creates LineString features from attributes.
            """
            if start_e != 0.0 and start_n != 0.0 and end_e != 0.0 and end_n != 0.0:
                start_point = QgsPointXY(start_e, start_n)
                end_point = QgsPointXY(end_e, end_n)
                
                geom = QgsGeometry.fromPolylineXY([start_point, end_point])
                
                # Create features and set attributes
                feature = QgsFeature()
                feature.setGeometry(geom)
                feature.setAttributes([start_name, end_name, delta_h, std_dh])
                return feature
        
        # main loop
        with open(file_path, "r", encoding="utf-16") as f:
            reader = csv.reader(f, delimiter=";")
            sep = next(reader)
            header = next(reader)
            
            start = None
            start_e = 0
            start_n = 0
            start_h = 0
            end = None
            end_e = 0
            end_n = 0
            end_h = 0
            dh = 0
            var = 0

            for row in reader:
                point, tpe, bs, ins, fs, offset, dist, e, n, h, stdline = row
                if tpe == "":
                    if start is None:
                        start = point
                        start_e = to_float(e)
                        start_n = to_float(n)
                        start_h = to_float(h)
                    else:
                        end = point
                        end_e = to_float(e)
                        end_n = to_float(n)
                        end_h = to_float(h)
                        
                        feature = make_line(start, end, dh, var**0.5, start_e, start_n, end_e, end_n)
                        features.append(feature)
                        dh = 0
                        var = 0
                        start = point
                        start_e = to_float(e)
                        start_n = to_float(n)
                        start_h = to_float(h)
                        end = None
                elif tpe == "BS1":
                    dh += to_float(bs) + to_float(offset)
                    var += to_float(stdline)**2
                elif tpe == "FS1":
                    dh -= to_float(fs) - to_float(offset)
                    var += to_float(stdline)**2
                elif tpe == "IS":
                    dhi = dh - to_float(ins) - to_float(offset)
                    vari = var + to_float(stdline)**2
                    
                    end = point
                    end_e = to_float(e)
                    end_n = to_float(n)
                    end_h = to_float(h)
                    
                    feature = make_line(start, end, dhi, vari**0.5, start_e, start_n, end_e, end_n)
                    features.append(feature)
                    end = None
                    
        
        # Add features to layer
        provider.addFeatures(features)
        vl.updateExtents()
        
        # Add layer to drawing
        QgsProject.instance().addMapLayer(vl)
        return {}
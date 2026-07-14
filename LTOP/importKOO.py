from qgis.core import (QgsProcessingAlgorithm, QgsProcessingParameterFile, 
                       QgsFields, QgsField, QgsFeature, QgsGeometry, 
                       QgsPointXY, QgsVectorLayer, QgsProject)
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtGui import QIcon, QPixmap
import base64
import os

class ImportLtopKoo(QgsProcessingAlgorithm):
    FILE_INPUT = 'INPUT'

    def tr(self, string):
        return string

    def createInstance(self):
        return ImportLtopKoo()

    def name(self):
        return 'import_ltop_koo'

    def displayName(self):
        return self.tr('LTOP-KOO Importieren')

    def group(self):
        return self.tr('LTOP Formate')

    def groupId(self):
        return 'swiss_formats'

    # Add Tool to Toolbar
    def mainMenuCommand(self):
        return 'QGeoProcessing' # in menu "QGeoProcessing"

    def shortHelpString(self):
        return 'Dieses Skript importiert Swisstopo LTOP-KOO Dateien (.koo) als LV95-Punktlayer.'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFile(
                self.FILE_INPUT,
                self.tr('LTOP-KOO Datei (.koo)'),
                extension='koo'
            )
        )
        
    def icon(self):
        svg_data = '''
        <svg width="500" height="500" xmlns="http://www.w3.org/2000/svg">
         <g id="Layer_1">
          <title>Layer 1</title>
          <text transform="matrix(1 0 0 1 0 0)" font-weight="bold" xml:space="preserve" text-anchor="start" font-family="'Assistant'" font-size="200" stroke-width="0" id="svg_4" y="323.50001" x="62.39844" stroke="#00ff11" fill="#00ff11">KOO</text>
         </g>
        </svg>'''
        
        from qgis.PyQt.QtGui import QPixmap, QIcon
        
        # Das SVG wird direkt als Datenstrom in ein Pixmap geladen
        pixmap = QPixmap()
        pixmap.loadFromData(svg_data.encode('utf-8'), 'SVG')
        
        return QIcon(pixmap)

    def processAlgorithm(self, parameters, context, feedback):
        file_path = self.parameterAsFile(parameters, self.FILE_INPUT, context)
        
        # Define Fields (Attribute Table)
        fields = QgsFields()
        fields.append(QgsField("PntID", QVariant.String))
        fields.append(QgsField("East", QVariant.Double))
        fields.append(QgsField("North", QVariant.Double))
        fields.append(QgsField("Height", QVariant.Double))
        fields.append(QgsField("Epoch", QVariant.String))
        fields.append(QgsField("Date", QVariant.String))
        fields.append(QgsField("Order", QVariant.String))
        fields.append(QgsField("Map", QVariant.String))
        fields.append(QgsField("OriginPos", QVariant.String))
        fields.append(QgsField("HeightSystem", QVariant.String))
        fields.append(QgsField("CoordinateCode", QVariant.String))
        fields.append(QgsField("GeoidSep", QVariant.Double))
        fields.append(QgsField("Geoid", QVariant.String))
        fields.append(QgsField("Ellipsoid", QVariant.String))
        fields.append(QgsField("Eta", QVariant.Double))
        fields.append(QgsField("Xi", QVariant.Double))
        fields.append(QgsField("DoVCode", QVariant.String))
        fields.append(QgsField("Eta0", QVariant.Double))
        fields.append(QgsField("Xi0", QVariant.Double))
        fields.append(QgsField("DoVCode0", QVariant.String))
        fields.append(QgsField("RTRI", QVariant.String))
        fields.append(QgsField("Comment", QVariant.String))
        
        vl = QgsVectorLayer("Point?crs=EPSG:2056", os.path.basename(file_path), "memory")
        provider = vl.dataProvider()
        provider.addAttributes(fields)
        vl.updateFields()
        
        features = []
        
        # Helper Function to convert str to float
        def parse_float(val_string):
            cleaned = val_string.strip()
            if not cleaned:
                return 0.0
            try:
                return float(cleaned)
            except ValueError:
                return 0.0

        with open(file_path, 'r', encoding='utf-8') as f:
            for line_idx, line in enumerate(f, 1):
                if line.startswith('$$') or not line.strip():
                    continue
                
                # ensure coords are defined (line must contain at least 56 entries)
                if len(line) < 56:
                    continue
                
                try:
                    # strings
                    pnt_id = line[:10].strip()
                    epoch = line[10:14].strip()
                    date = line[14:22].strip()
                    order = line[22:26].strip()
                    map_val = line[26:32].strip()
                    
                    # coords
                    east_val = parse_float(line[32:44])
                    north_val = parse_float(line[44:56])
                    
                    # additional fields
                    pos = line[56:60].strip() if len(line) > 56 else ""
                    height_val = parse_float(line[60:70]) if len(line) > 60 else 0.0
                    height_sys = line[70:74].strip() if len(line) > 70 else ""
                    coord_code = line[74:76].strip() if len(line) > 74 else ""
                    geoid_sep_val = parse_float(line[76:84]) if len(line) > 76 else 0.0
                    geoid = line[84:88].strip() if len(line) > 84 else ""
                    ellipsoid = line[88:90].strip() if len(line) > 88 else ""
                    eta_val = parse_float(line[90:96]) if len(line) > 90 else 0.0
                    xi_val = parse_float(line[96:102]) if len(line) > 96 else 0.0
                    dov = line[102:106].strip() if len(line) > 102 else ""
                    eta0_val = parse_float(line[106:112]) if len(line) > 106 else 0.0
                    xi0_val = parse_float(line[112:118]) if len(line) > 112 else 0.0
                    dov0 = line[118:122].strip() if len(line) > 118 else ""
                    rtri = line[122:126].strip() if len(line) > 122 else ""
                    comment = line[138:].strip() if len(line) > 138 else ""
                    
                    # create features
                    fet = QgsFeature(vl.fields())
                    fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(east_val, north_val)))
                    
                    # append attributes in correct order
                    fet.setAttributes([
                        pnt_id, east_val, north_val, height_val, epoch, date, order, 
                        map_val, pos, height_sys, coord_code, geoid_sep_val, geoid, 
                        ellipsoid, eta_val, xi_val, dov, eta0_val, xi0_val, dov0, 
                        rtri, comment
                    ])
                    features.append(fet)
                    
                except Exception as e:
                    feedback.reportError(f"Fehler in Zeile {line_idx}: {str(e)}")
                    continue
                        
        provider.addFeatures(features)
        vl.updateExtents()
        
        QgsProject.instance().addMapLayer(vl)
        return {}

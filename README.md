# 🌍 QGeoProcessing

**QGeoProcessing** is a collection of QGIS Processing Tools designed to simplify the handling, analysis, and visualization of geodetic network data.

---

## 🚀 Featured Tools

### 📍 LTOP-KOO Importer (`importKOO.py`)
Easily import Swisstopo LTOP coordinate files (`.koo`) as point layers into QGIS. Only coordinates in the Swiss LV95 system (EPSG:2056) are supported.

*   **Rich Attributes:** Imports and structures all additional geodetic attributes (epochs, heights, map sheets, geoid separations, etc.) into the attribute table.
*   **Menu Integration:** Once activated, the tool is fully integrated into the QGIS interface.

| Category | Location in QGIS |
| :--- | :--- |
| **Processing Toolbox** | `Scripts` ➡️ `LTOP Formate` ➡️ `LTOP-KOO Importer` |
| **Main Menu** | `QGeoProcessing` [Extended Installation](#️-extended-installation-optional) |
| **Quick Access** | Can be added directly to the `Processing Toolbar` [Extended Installation](#️-extended-installation-optional) |

---

### 📍 Infinity-NIV Importer (`importNIV.py`)
Quickly import CSV-files containing Levelling data, for example exported from Leica Infinity.

*   **Direct Computation of Height differences:** Height differences from levelling data are directly computed from backsights, foresights, and interim-sights.
*   **Incorporated Standard Deviation:** The standard deviation of an observation, if provided, are kept for further processing.
*   **Graphical Representation of Levelling Lines:** Levelling lines are drawn in the QGIS map canvas.

The CSV-File must be provided in the following format. The two introductory lines are mandatory, allthough they are ignored. The columns must be separated with a semicolon (```;```), and the order of the columns is given. Additional columns can be vorhanden after the standard deviation ```std```, however, they are ignored.

```CSV
sep=;
"PointId";"Type";"BS";"IS";"FS";"Staff Offset";"Dist";"Easting";"Northing";"Height";"SD"
"45A";"";"-";"-";"-";"-";"-";"2681650.52000";"1224638.10000";"420.79600";"-"
"45A";"BS1";"0.92254";"-";"-";"-";"11.34130";"-";"-";"-";"0.00004"
"U1";"FS1";"-";"-";"2.06174";"-";"12.03484";"-";"-";"-";"0.00004"
"U1";"";"-";"-";"-";"-";"-";"2681635.18578";"1224649.57560";"419.65680";"-"
"U1";"BS1";"0.40326";"-";"-";"-";"18.84574";"-";"-";"-";"0.00003"
"U2";"FS1";"-";"-";"2.14019";"-";"17.66021";"-";"-";"-";"0.00004"
"U2";"";"-";"-";"-";"-";"-";"2681611.48371";"1224631.94181";"417.91987";"-"
"U2";"BS1";"1.11651";"-";"-";"-";"25.78282";"-";"-";"-";"0.00007"
"U3";"FS1";"-";"-";"1.50962";"-";"23.94459";"-";"-";"-";"0.00003"
"U3";"";"-";"-";"-";"-";"-";"2681585.16342";"1224589.76000";"417.52675";"-"
"U3";"BS1";"1.61620";"-";"-";"-";"30.79060";"-";"-";"-";"0.00003"
"U4";"FS1";"-";"-";"2.01276";"-";"25.33027";"-";"-";"-";"0.00006"
"U4";"";"-";"-";"-";"-";"-";"2681562.82575";"1224539.39140";"417.13019";"-"
"U4";"BS1";"0.14897";"-";"-";"-";"12.03547";"-";"-";"-";"0.00005"
"B401";"IS";"-";"2.45514";"-";"-";"19.74568";"2681546.56959";"1224517.85532";"414.82402";"0.00003"
"U6";"FS1";"-";"-";"2.45676";"-";"14.80791";"-";"-";"-";"0.00004"
"U6";"";"-";"-";"-";"-";"-";"2681538.88147";"1224528.60145";"414.82240";"-"
"U6";"BS1";"1.56181";"-";"-";"-";"12.67299";"-";"-";"-";"0.00002"
"B401";"IS";"-";"1.56019";"-";"-";"24.68856";"2681545.62663";"1224517.76335";"414.82402";"0.00005"
"U7";"FS1";"-";"-";"1.33503";"-";"18.18165";"-";"-";"-";"0.00003"
"U7";"";"-";"-";"-";"-";"-";"2681533.29169";"1224558.80569";"415.04917";"-"
```

| Category | Location in QGIS |
| :--- | :--- |
| **Processing Toolbox** | `Scripts` ➡️ `Infinity Formate` ➡️ `Infinity-KOO Importer` |
| **Main Menu** | `QGeoProcessing` [Extended Installation](#️-extended-installation-optional) |
| **Quick Access** | Can be added directly to the `Processing Toolbar` [Extended Installation](#️-extended-installation-optional) |

---

## ⚙️ Installation

Adding the scripts to QGIS is quick and straightforward:

1. **Open QGIS** and ensure the **Processing Toolbox** is visible (if not, press `Ctrl + Alt + T` or go to *Processing* ➡️ *Toolbox*).
2. Click on the **Python Symbol** (Scripts) at the top of the Processing Toolbox panel.
3. Select ➡️ **`Add Script to Toolbox...`** from the dropdown menu.
4. Select the respective Python file (e.g., `ImportLTOPKOO.py`) from your local directory.
5. **Done!** The tool is now registered and ready to run.

> 💡 **Tip:** The tools come with custom embedded vector icons, making them easy to spot in your QGIS Processing panel!

## ⚙️ Extended Installation (Optional)
To quickly access the processing plugins in the main menu and the ```Processing Algorithms``` section, follow these steps:
1. Navigate: ```Settings``` ➡️ ```Options``` ➡️ ```Menus``` ➡️ ```Scripts``` ➡️ ```[Algorithm-Name]```
2. Under ```Menu path``` enter ```QGeoProcessing``` which results in a new Menu in the Menu Bar
3. Enable the option ```Add button in toolbar``` to show the algorithm in the processing toolbar
4. Store the [icon](./icons/) under ```C:/Users/[user]/AppData/Roaming/QGIS/QGIS3/profiles/default/processing/scripts/icons/[algorithm].png```
5. Under ```Icon``` set the path to the icon (Step 4.)
6. Restart the application for the changes to appear
---

## 🛠️ Requirements

* **QGIS** 3.x or 4.x
* **Python** 3.x (included with your QGIS installation)

---

## 🎓 Citation

If you use **QGeoProcessing** or any of its tools (like `importKOO.py`) in an academic publication, thesis, or report, please cite it as follows:

### BibTeX
```bibtex
@software{qgeoprocessing2026,
  author       = {Rüfenacht, Fabian},
  title        = {QGeoProcessing: QGIS Processing Tools for Geodetic Networks},
  year         = {2026},
  version      = {1.0.0},
  publisher    = {GitHub},
  journal      = {GitHub repository},
  howpublished = {\url{[https://github.com/FabianRuefenacht/QGeoProcessing](https://github.com/FabianRuefenacht/QGeoProcessing)}}
}

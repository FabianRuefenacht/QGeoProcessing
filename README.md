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

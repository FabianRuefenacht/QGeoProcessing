# 🌍 QGeoProcessing

**QGeoProcessing** is a collection of QGIS Processing Tools designed to simplify the handling, analysis, and visualization of geodetic network data.

---

## 🚀 Featured Tools

### 📍 LTOP-KOO Importer (`importKOO.py`)
Easily import Swisstopo LTOP coordinate files (`.koo`) as high-precision point layers into QGIS.

*   **Automatic CRS Support:** Automatically handles coordinates in the Swiss LV95 system (EPSG:2056).
*   **Rich Attributes:** Imports and structures all additional geodetic attributes (epochs, heights, map sheets, geoid separations, etc.) into the attribute table.
*   **Menu Integration:** Once activated, the tool is fully integrated into the QGIS interface.

| Category | Location in QGIS |
| :--- | :--- |
| **Processing Toolbox** | `Scripts` ➡️ `LTOP Formate` ➡️ `LTOP-KOO Importieren` |
| **Main Menu** | `Vector` (Vektor) |
| **Quick Access** | Can be added directly to the `Processing Toolbar` |

---

## ⚙️ Installation

Adding the scripts to QGIS is quick and straightforward:

1. **Open QGIS** and ensure the **Processing Toolbox** is visible (if not, press `Ctrl + Alt + T` or go to *Processing* ➡️ *Toolbox*).
2. Click on the **Python Symbol** (Scripts) at the top of the Processing Toolbox panel.
3. Select ➡️ **`Add Script to Toolbox...`** from the dropdown menu.
4. Select the respective Python file (e.g., `ImportLTOPKOO.py`) from your local directory.
5. **Done!** The tool is now registered and ready to run.

> 💡 **Tip:** The tools come with custom embedded vector icons, making them easy to spot in your QGIS Processing panel!

---

## 🛠️ Requirements

* **QGIS** 3.x or 4.x
* **Python** 3.x (included with your QGIS installation)

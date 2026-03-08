# Node-Based Machine Learning Editor

This project is a visual, node-based editor for building machine learning pipelines using **Python**, **Dear PyGui**, and **scikit-learn**. It allows users to load datasets, perform data manipulation (encoding, scaling, imprinting), train models, and visualize results without writing code in the editor itself.

---

## Features

- **Visual Workflow** — Connect nodes to define the flow of data from input to evaluation.
- **Machine Learning Integration** — Built-in support for popular classifiers like Random Forest, KNN, and HistGradientBoosting.
- **Data Processing** — Nodes for handling missing values, encoding categorical data, and feature scaling.
- **Persistence** — Save and load your node configurations as `.json` files.
- **Real-time Visualization** — View tables, correlation matrices, and confusion matrices directly within the editor.

---

## Getting Started

### Prerequisites

Ensure you have **Python 3.10+** installed. Install the required libraries:
```bash
pip install -r requirements.txt
```

### Installation

1. Clone or download this repository.
2. Navigate to the project root directory.

### Running the Application
```bash
python main.py
```

| Shortcut | Action |
|---|---|
| `F5` | Run the current pipeline |
| `Delete` | Remove selected nodes or links |
| `Right Click` | Open context menu (delete / duplicate) |

---

## How to Create Your Own Nodes

All nodes must inherit from the `Node` abstract base class found in `base.py`. The application automatically discovers new nodes placed in subdirectories within the `nodes/` folder.

### Step 1 — Create a New Python File

Create a new file in one of the subdirectories under `nodes/`:
```
nodes/MyCategory/my_node.py
```

### Step 2 — Define Your Node Class

Inherit from `Node` and implement the `design()` and `calculate()` methods:
```python
import dearpygui.dearpygui as dpg
from base import Node
import pandas as pd

class MyCustomNode(Node):
    name = "My Custom Node"  # The display name in the UI

    def design(self):
        # 1. Define Input Attributes
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.DataFrame}) as self.df_in:
            dpg.add_text("Input Data")

        # 2. Define Static Attributes (Settings)
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.param = dpg.add_input_float(label="Multiplier", default_value=1.0)

        # 3. Define Output Attributes
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": pd.DataFrame}) as self.df_out:
            dpg.add_text("Output Data")

    def calculate(self):
        df = self.get_value(self.df_in)
        multiplier = dpg.get_value(self.param)

        if df is not None:
            result_df = df * multiplier
            return result_df

        return None
```

### Step 3 — Key Methods & Concepts

| Concept | Description |
|---|---|
| `design()` | Uses `dearpygui` to draw the node's UI. Must define `dpg.node_attribute` here. |
| `calculate()` | Called when the pipeline runs. Use `self.get_value(pin_tag)` to retrieve upstream data. |
| `user_data={"data_type": ...}` | Enables type checking — prevents incompatible pins from connecting. |
| Auto-discovery | `main.py` scans `nodes/`. Each subfolder becomes a category in the left-hand panel. |

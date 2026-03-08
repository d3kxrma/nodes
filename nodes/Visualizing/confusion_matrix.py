import pandas as pd
import dearpygui.dearpygui as dpg
from base import Node
from sklearn.metrics import confusion_matrix

class ConfusionMatrixNode(Node):
    name = "Confusion Matrix"

    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.Series}) as self.y_true_in:
            dpg.add_text("y_true")
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.Series}) as self.y_pred_in:
            dpg.add_text("y_pred")
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output):
            with dpg.plot(label="Confusion Matrix", width=250, height=250, no_menus=True):
                dpg.add_plot_legend()
                self.xaxis = dpg.add_plot_axis(dpg.mvXAxis, label="Predicted Class", no_gridlines=True)
                self.yaxis = dpg.add_plot_axis(dpg.mvYAxis, label="Actual Class", no_gridlines=True, invert=True)

    def calculate(self):
        y_true = self.get_value(self.y_true_in)
        y_pred = self.get_value(self.y_pred_in)
        
        dpg.delete_item(self.yaxis, children_only=True)
        
        if y_true is not None and y_pred is not None:
            try:
                cm = confusion_matrix(y_true, y_pred)
                rows, cols = cm.shape
                
                flat_cm = cm.flatten().astype(float).tolist()
                max_val = max(flat_cm) if flat_cm else 1
                
                dpg.add_heat_series(
                    flat_cm, rows, cols, 
                    scale_min=0, scale_max=max_val, 
                    format="%0.0f", parent=self.yaxis
                )
                
                dpg.set_axis_limits(self.xaxis, 0, cols)
                dpg.set_axis_limits(self.yaxis, 0, rows)
            except Exception as e:
                print(f"Confusion Matrix Error: {e}")
        return None
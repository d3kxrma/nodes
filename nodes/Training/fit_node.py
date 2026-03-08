import dearpygui.dearpygui as dpg
import pandas as pd
from base import Node

from sklearn.base import clone

class FitNode(Node):
    name = "Fit Model"

    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": "estimator"}) as self.in_estimator:
            dpg.add_text("Estimator")
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.DataFrame}) as self.in_x:
            dpg.add_text("X_train")
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.Series}) as self.in_y:
            dpg.add_text("y_train")
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": "fitted_estimator"}):
            dpg.add_text("Fitted Model")

    def calculate(self):
        estimator = self.get_value(self.in_estimator)
        x_data = self.get_value(self.in_x)
        y_data = self.get_value(self.in_y)

        if isinstance(x_data, dict) and "X_train" in x_data:
            x_data = x_data["X_train"]
        if isinstance(y_data, dict) and "y_train" in y_data:
            y_data = y_data["y_train"]

        if estimator is not None and x_data is not None and y_data is not None:
            
            fitted_model = clone(estimator)
            fitted_model.fit(x_data, y_data)
            return fitted_model
        return None
import dearpygui.dearpygui as dpg
import pandas as pd
from base import Node

class PredictNode(Node):
    name = "Predict"

    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": "fitted_estimator"}) as self.in_model:
            dpg.add_text("Fitted Model")
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.DataFrame}) as self.in_x:
            dpg.add_text("X_test")
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": pd.Series}):
            dpg.add_text("Predictions")

    def calculate(self):
        model = self.get_value(self.in_model)
        x_data = self.get_value(self.in_x)

        if isinstance(x_data, dict) and "X_test" in x_data:
            x_data = x_data["X_test"]

        if model is not None and x_data is not None:
            predictions = model.predict(x_data)
            return pd.Series(predictions, name="Prediction")
            
        return pd.Series(dtype=float)
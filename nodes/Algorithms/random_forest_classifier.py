import dearpygui.dearpygui as dpg
from base import Node

from sklearn.ensemble import RandomForestClassifier

class RandomForestClassifierNode(Node):
    name = "Random Forest Classifier"
    
    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.n_estimators = dpg.add_input_int(label="n_estimators", default_value=100, width=100, min_value=1)
            self.max_depth = dpg.add_input_int(label="max_depth", default_value=0, width=100)
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": "estimator"}):
            dpg.add_text("Estimator")

    def calculate(self):
        n_est = dpg.get_value(self.n_estimators)
        depth = dpg.get_value(self.max_depth)
        depth_val = depth if depth > 0 else None
        return RandomForestClassifier(n_estimators=n_est, max_depth=depth_val)
import dearpygui.dearpygui as dpg
from base import Node

from sklearn.tree import DecisionTreeClassifier


class DecisionTreeClassifierNode(Node):
    name = "Decision Tree Classifier"
    
    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.criterion = dpg.add_combo(items=["gini", "entropy", "log_loss"], default_value="gini", width=100, label="criterion")
            self.max_depth = dpg.add_input_int(label="max_depth", default_value=0, width=100)
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": "estimator"}):
            dpg.add_text("Estimator")

    def calculate(self):
        crit = dpg.get_value(self.criterion)
        depth = dpg.get_value(self.max_depth)
        depth_val = depth if depth > 0 else None
        return DecisionTreeClassifier(criterion=crit, max_depth=depth_val)
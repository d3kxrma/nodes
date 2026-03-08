import dearpygui.dearpygui as dpg
from base import Node

from sklearn.ensemble import HistGradientBoostingClassifier

class HistGradientBoostingClassifierNode(Node):
    name = "HistGradientBoosting Classifier"
    
    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.max_iter = dpg.add_input_int(label="max_iter", default_value=100, width=100, min_value=1)
            self.learning_rate = dpg.add_input_float(label="learning_rate", default_value=0.1, width=100, step=0.01)
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": "estimator"}):
            dpg.add_text("Estimator")

    def calculate(self):
        m_iter = dpg.get_value(self.max_iter)
        lr = dpg.get_value(self.learning_rate)
        return HistGradientBoostingClassifier(max_iter=m_iter, learning_rate=lr)
import dearpygui.dearpygui as dpg
from base import Node

from sklearn.neighbors import KNeighborsClassifier


class KNeighborsClassifierNode(Node):
    name = "KNN Classifier"
    
    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.n_neighbors = dpg.add_input_int(label="n_neighbors", default_value=5, width=100, min_value=1)
            self.weights = dpg.add_combo(items=["uniform", "distance"], default_value="uniform", width=100, label="weights")
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": "estimator"}):
            dpg.add_text("Estimator")

    def calculate(self):
        n = dpg.get_value(self.n_neighbors)
        w = dpg.get_value(self.weights)
        return KNeighborsClassifier(n_neighbors=n, weights=w)
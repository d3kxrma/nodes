import dearpygui.dearpygui as dpg
from base import Node

class InputNode(Node):
    name = "Number input"
        
    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": float}):
            self.inp = dpg.add_input_float(width=150)
 
    def calculate(self) -> float:
        return dpg.get_value(self.inp)
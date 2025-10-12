import dearpygui.dearpygui as dpg
from base import Node

class OutNode(Node):
    def __init__(self):
        self.name = "Output"
    
    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input) as i:
            self.i = i
            self.txt = dpg.add_text("output")
    
    def calculate(self):
        dpg.set_value(item = self.txt, value = f"Result: {dpg.get_item_user_data(self.i).calculate()}")
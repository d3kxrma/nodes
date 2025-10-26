import dearpygui.dearpygui as dpg
from base import Node

class StringInputNode(Node):
    def __init__(self):
        super().__init__(name="String input")
        
    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type":str}):
            self.inp = dpg.add_input_text(width=150)

    def calculate(self) -> str:
        return dpg.get_value(self.inp)
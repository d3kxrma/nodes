import dearpygui.dearpygui as dpg
from base import Node

class SumNode(Node):
    def __init__(self):
        self.A1: Node = None
        self.A2: Node = None
        
    def spawn(self):
        with dpg.node(label="Number input", parent="editor", user_data=self):
            with dpg.node_attribute(label="Float input", attribute_type=dpg.mvNode_Attr_Input):
                self.a = dpg.add_text("First digit")
            with dpg.node_attribute(label="Float input", attribute_type=dpg.mvNode_Attr_Input):
                dpg.add_text("Second digit")
            
            with dpg.node_attribute(label="Float Output", attribute_type=dpg.mvNode_Attr_Output):
                self.r = dpg.add_text("Result")
                dpg.add_text(dpg.get_item_parent(dpg.get_item_parent(self.a)))
    
    def set_children(self, children):
        if not self.A1:
            self.A1 = children
        else:
            self.A2 = children
    
    def calculate(self):
        dpg.set_value(item = self.r, value = f"Result: {self.A1.calculate() + self.A2.calculate()}")
        return self.A1.calculate() + self.A2.calculate()
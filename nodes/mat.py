import dearpygui.dearpygui as dpg
from base import Node

class MathNode(Node):
    def __init__(self):
        self.name = "Math operations"
        self.operation = "+"
    
    def on_select(self, sender, app_data, user_data):
        self.operation = app_data
    
    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input) as fd:
            self.fd = fd
            dpg.add_text("First digit")
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input) as sd:
            self.sd = sd
            dpg.add_text("Second digit")
            dpg.add_separator()
        
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            dpg.add_combo(
                items=["+", "-", "*", "/", "//", "%"],
                default_value="+",
                callback=self.on_select
            )
            dpg.add_separator()
        
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output):
            self.r = dpg.add_text("Result")
    
    def calculate(self):
        fd = dpg.get_item_user_data(self.fd).calculate()
        sd = dpg.get_item_user_data(self.sd).calculate()
        
        match self.operation:
            case "+":
                res = fd + sd
            
            case "-":
                res = fd - sd
                
            case "*":
                 res = fd * sd
                
            case "/":
                res = fd / sd
            
            case "//":
                res = fd // sd
                
            case "%":
                res = fd % sd 
        
        dpg.set_value(item = self.r, value = f"Result: {res}")
        return res
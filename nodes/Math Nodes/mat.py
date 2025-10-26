import dearpygui.dearpygui as dpg
from base import Node

class MathNode(Node):
    def __init__(self):
        super().__init__(name="Math operations")
        self.operation = "+"
    
    def on_select(self, sender, app_data, user_data):
        self.operation = app_data
    
    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": float}) as fd:
            self.fd = fd
            dpg.add_text("First digit")
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": float}) as sd:
            self.sd = sd
            dpg.add_text("Second digit")
        
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            dpg.add_combo(
                items=["+", "-", "*", "/", "//", "%"],
                default_value="+",
                callback=self.on_select,
                width=50
            )

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": float}):
            self.r = dpg.add_text("Result")
    
    def calculate(self):
        fd = self.get_value(self.fd)
        sd = self.get_value(self.sd)
        
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
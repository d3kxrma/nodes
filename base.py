import dearpygui.dearpygui as dpg

class Node:
    def __init__(self):
        self.name = "Base Node"
        pass
    
    def spawn(self):
        with dpg.node(label="Base Node", parent="editor", user_data=self):
            pass
    
    def set_children(self):
        pass
    
    def calculate(self):
        return None
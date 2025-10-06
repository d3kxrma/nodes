import dearpygui.dearpygui as dpg

class Node:
    def __init__(self):
        self.name = "Base Node"

    def spawn(self):
        with dpg.node(label=self.name, parent="editor", user_data=self) as tag:
            self.tag = tag
            self.design()
        self.popup()
    
    def design(self):
        self.txt = dpg.add_text(self.name)
    
    def popup(self):
        with dpg.popup(self.tag, mousebutton=dpg.mvMouseButton_Right):
                dpg.add_menu_item(label="Delete", callback=self.delete)
                dpg.add_separator()
                dpg.add_menu_item(label="Close")
    
    def delete(self):
        for pin in dpg.get_item_children(self.tag)[1]:
            conf = dpg.get_item_configuration(pin)
            if conf.get("attribute_type") == 1:
                if conf.get("user_data") and conf.get(conf.get("user_data")):
                    dpg.set_item_user_data(conf.get("user_data"), None)
        dpg.delete_item(self.tag)
    
    def calculate(self):
        return None
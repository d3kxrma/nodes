import dearpygui.dearpygui as dpg

class Node:
    """
    Base node class. All created nodes must inherit from this class. 
    If you want to create your own node, you need to write a class that inherits from this class and change the design and calculate functions.
    """
    def __init__(self):
        self.name = "Base Node"

    def spawn(self):
        """
        Node creation function. Creates the node itself and calls other functions. 
        Usually, no changes are required.
        """
        with dpg.node(label=self.name, parent="editor", user_data=self) as tag:
            self.tag = tag
            self.design()
        self.popup()
    
    def design(self):
        """
        A function that describes all elements of a node.
        """
        with dpg.node_attribute(label=self.name, attribute_type=dpg.mvNode_Attr_Static):
            dpg.add_text(self.name)
    
    def popup(self):
        """
        A function that defines the operation of the popup menu. 
        Usually does not require changes.
        """
        with dpg.popup(self.tag, mousebutton=dpg.mvMouseButton_Right):
                dpg.add_menu_item(label="Delete", callback=self.delete)
                dpg.add_menu_item(label="Duplicate", callback=self.duplicate)
                dpg.add_separator()
                dpg.add_menu_item(label="Close")
    
    def duplicate(self):
        """
        One of the menu items. This function is needed to clone the current node. No changes are required.
        """
        i = self.__class__()
        i.spawn()
        
    def delete(self):
        """
        Node deletion function. Yes, it is literally self-destruction. No changes are required.
        
        `This message will self-destruct in five seconds`
        """
        for pin in dpg.get_item_children(self.tag)[1]:
            conf = dpg.get_item_configuration(pin)
            if conf.get("attribute_type") == 1:
                if conf.get("user_data") and conf.get(conf.get("user_data")):
                    dpg.set_item_user_data(conf.get("user_data"), None)
        dpg.delete_item(self.tag)
    
    def calculate(self):
        """
        The function in which all calculations take place. 
        You must obtain data from elements that have an input attribute, perform any calculations, and return the value using `return`.
        """
        return
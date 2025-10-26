from abc import ABC, abstractmethod
import dearpygui.dearpygui as dpg

class Node(ABC):
    """
    Base node class. All created nodes must inherit from this class. 
    If you want to create your own node, you need to write a class that inherits from this class and change the design and calculate functions.
    """
    def __init__(self, name:str):
        self.name = name

    def spawn(self, pos:list[int]=[0, 0]):
        """
        Node creation function. Creates the node itself and calls other functions. 
        Usually, no changes are required.
        """
        if pos == [0, 0]: 
            editor_size = dpg.get_item_rect_size("editor")
            editor_pos = dpg.get_item_pos("editor")
            pos = [editor_pos[0]+editor_size[0]//2, editor_pos[1]+editor_size[1]//2]
        
        
        with dpg.node(label=self.name, parent="editor", user_data=self, pos=pos) as tag:
            self.tag = tag
            self.design()
            
        self.popup()
        self.set_types()

    @abstractmethod
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
    
    def set_types(self):
        """
        A function that sets the data types for all pins that do not have them set. No changes are required.
        """
        node_attrs = dpg.get_item_children(self.tag)[1]
        
        for attr in node_attrs:
            conf = dpg.get_item_configuration(attr)
            if conf.get("user_data") is None:
                dpg.set_item_user_data(attr, {'data_type': None})
    
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
            if conf.get("user_data"):
                
                if "right_node" in conf.get("user_data"):
                    right_node = conf.get("user_data").get("right_node")
                    right_data = dpg.get_item_user_data(right_node)
                    del right_data["left_node"]
                    dpg.set_item_user_data(right_node, right_data)

                if "left_node" in conf.get("user_data"):
                    left_node = conf.get("user_data").get("left_node")
                    left_data = dpg.get_item_user_data(left_node)
                    del left_data["right_node"]
                    dpg.set_item_user_data(left_node, left_data)
        dpg.delete_item(self.tag)
    
    def get_value(self, pin_tag:int|str) -> any:
        """
        A function to get the value from a specific pin. 
        You need to pass the tag of the pin from which you want to get the value.
        No changes are required.
        """
        left_node = dpg.get_item_user_data(pin_tag).get("left_node")
        node_class = dpg.get_item_user_data(dpg.get_item_parent(left_node))
        return node_class.calculate()
    
    @abstractmethod
    def calculate(self):
        """
        The function in which all calculations take place. 
        You must obtain data from elements that have an input attribute, perform any calculations, and return the value using `return`.
        """
        return
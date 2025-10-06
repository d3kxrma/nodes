import dearpygui.dearpygui as dpg
dpg.create_context()

"""
панель для додавання нодів, використавння бейз ноди, по можливості розширена інформація про ноди, валідація вихідних та вхідниї даних (типи)
"""

class InputNode:
    def __init__(self):
        self.name = "Number Input"
    
    def spawn(self):
        with dpg.node(label=self.name, parent="editor", user_data=self) as tag:
            self.tag = tag
            self.design()
        self.popup()
    
    def design(self):
        with dpg.node_attribute(label="Float input", attribute_type=dpg.mvNode_Attr_Output):
            self.inp = dpg.add_input_float(width=150)
            dpg.add_text(dpg.get_item_parent(dpg.get_item_parent(self.inp)))
    
    def delete(self):
        for pin in dpg.get_item_children(self.tag)[1]:
            conf = dpg.get_item_configuration(pin)
            if conf.get("attribute_type") == 1:
                if conf.get("user_data") and conf.get(conf.get("user_data")):
                    dpg.set_item_user_data(conf.get("user_data"), None)
        dpg.delete_item(self.tag)
    
    def duplicate(self):
        i = InputNode()
        i.spawn()
    
    def popup(self):
        with dpg.popup(self.tag, mousebutton=dpg.mvMouseButton_Right):
                dpg.add_menu_item(label="Delete", callback=self.delete)
                dpg.add_menu_item(label="Duplicate", callback=self.duplicate)
                dpg.add_separator()
                dpg.add_menu_item(label="Close")
    
    def calculate(self):
        return dpg.get_value(self.inp)
        
class SumNode:
    def __init__(self):
        self.A1: int = None
        self.A2: int = None
        
    def spawn(self):
        with dpg.node(label="Summa", parent="editor", user_data=self) as f:
            self.f = f
            with dpg.node_attribute(label="Float input", attribute_type=dpg.mvNode_Attr_Input) as fd:
                self.A1 = fd
                dpg.add_text("First digit")
            with dpg.node_attribute(label="Float input", attribute_type=dpg.mvNode_Attr_Input) as sd:
                self.A2 = sd
                dpg.add_text("Second digit")
            
            with dpg.node_attribute(label="Float Output", attribute_type=dpg.mvNode_Attr_Output):
                self.r = dpg.add_text("Result")
                dpg.add_text(dpg.get_item_parent(dpg.get_item_parent(self.r)))
    
    # def set_children(self, children):
    #     if not self.A1:
    #         self.A1 = children
    #     else:
    #         self.A2 = children
    
    def calculate(self):
        res = dpg.get_item_user_data(self.A1).calculate() + dpg.get_item_user_data(self.A2).calculate()
        dpg.set_value(item = self.r, value = f"Result: {res}")
    
        return res

class MulNode:
    def __init__(self):
        self.A1: int = None
        self.A2: int = None
        
    def spawn(self):
        with dpg.node(label="Multiply", parent="editor", user_data=self) as f:
            self.f = f
            with dpg.node_attribute(label="Float input", attribute_type=dpg.mvNode_Attr_Input) as fd:
                self.A1 = fd
                dpg.add_text("First digit")
            with dpg.node_attribute(label="Float input", attribute_type=dpg.mvNode_Attr_Input) as sd:
                self.A2 = sd
                dpg.add_text("Second digit")
            
            with dpg.node_attribute(label="Float Output", attribute_type=dpg.mvNode_Attr_Output):
                self.r = dpg.add_text("Result")
                dpg.add_text(dpg.get_item_parent(dpg.get_item_parent(self.r)))
        return self.f
    # def set_children(self, children):
    #     if not self.A1:
    #         self.A1 = children
    #     else:
    #         self.A2 = children
    
    def calculate(self):
        res = dpg.get_item_user_data(self.A1).calculate() * dpg.get_item_user_data(self.A2).calculate()
        dpg.set_value(item = self.r, value = f"Result: {res}")
        return res

class OutNode:
    def __init__(self):
        self.A1: int = None
        
    def spawn(self):
        with dpg.node(label="Output", parent="editor", user_data=self) as f:
            self.f = f
            with dpg.node_attribute(label="Output") as out:
                self.A1 = out
                self.txt = dpg.add_text("output")
                # self.txt = dpg.add_text(self.A1)
                dpg.add_text(dpg.get_item_parent(dpg.get_item_parent(self.txt)))
                
    # def set_children(self, children):
    #     self.A1 = children
            
    def calculate(self):
        
        dpg.set_value(item = self.txt, value = f"Result: {dpg.get_item_user_data(self.A1).calculate()}")
        
        dpg.set_item_label(self.f, "Output")
        
def open_modal_callback(text: str, name:str="Error"):
    with dpg.window(label=name, modal=True, show=False, tag="modal_window"):
        dpg.add_text(text)
        dpg.add_button(label="Close", callback=lambda: dpg.delete_item("modal_window"))
    dpg.show_item("modal_window")

def link_callback(sender, app_data):
    # app_data -> (link_id1, link_id2)
    left_parent = dpg.get_item_parent(app_data[0])
    dpg.add_node_link(app_data[0], app_data[1], parent=sender, user_data=left_parent)
    dpg.set_item_user_data(app_data[1], dpg.get_item_user_data(left_parent))
    dpg.set_item_user_data(app_data[0], app_data[1])
    print(sender)
    print(app_data)
    print("^^^")

def delink_callback(sender, app_data):
    # app_data -> link_id
    # print(dpg.get_item_children("editor"))
    # print(sender)
    # print(app_data)
    # print(dpg.get_item_user_data(app_data))
    # print(dpg.get_item_configuration(app_data))
    conf = dpg.get_item_configuration(app_data)
    right = conf.get("attr_2")
    left = conf.get("attr_1")
    dpg.set_item_user_data(right, None)
    dpg.set_item_user_data(left, None)
    
    dpg.delete_item(app_data)

def call(sender, app_data):
    print(sender)
    print(app_data)

def run_callback(sender, app_data, user_data):
    print(dpg.get_item_children("editor"))
    editor_children = dpg.get_item_children("editor")
    
    if not editor_children[0]: # if any connection exists
        open_modal_callback("No connection found. Connect at least 2 nodes.")
        return
    
    nodes: list = editor_children[1]
    for x in dpg.get_item_children("editor")[0]:
        # print(lid)
        # left: InputNode = dpg.get_item_user_data(lid)
        # right: OutNode = dpg.get_item_user_data(x)[1]
        
        # right.set_children(left)
        nodes.remove(dpg.get_item_user_data(x))
    
    if len(nodes) == 1:
        dpg.get_item_user_data(nodes[0]).calculate()
    elif len(nodes) >= 2:
        open_modal_callback("Run is not possible due to 2 or more chains detected. Remove all unnecessary chains.")
    else:
        open_modal_callback("Run is not possible because no chains have been detected.")

def input_node(sender, app_data, user_data):
    i = InputNode()
    i.spawn()

def sum_node(sender, app_data, user_data):
   s = SumNode()
   s.spawn()
   
def mul_node(sender, app_data, user_data):
   m = MulNode()
   m.spawn()

def output_node(sender, app_data, user_data):
    o = OutNode()
    o.spawn()

with dpg.window(label="Tutorial", width=1000, height=700):
    with dpg.group(horizontal=True):
        dpg.add_button(label="run", callback=run_callback)
        dpg.add_button(label="input", callback=input_node)
        dpg.add_button(label="multiply", callback=mul_node)
        dpg.add_button(label="sum", callback=sum_node)
        dpg.add_button(label="output", callback=output_node)
    
    
    with dpg.node_editor(callback=link_callback, delink_callback=delink_callback, minimap=True, minimap_location=3, tag="editor"):
        pass
    
def delete_callback(): 
    nodes = dpg.get_selected_nodes("editor")
    for node in nodes:
        for pin in dpg.get_item_children(node)[1]:
            conf = dpg.get_item_configuration(pin)
            if conf.get("attribute_type") == 1:
                if conf.get("user_data") and conf.get(conf.get("user_data")):
                    dpg.set_item_user_data(conf.get("user_data"), None)
        dpg.delete_item(node)
    
    links = dpg.get_selected_links("editor")
    for link in links:
        conf = dpg.get_item_configuration(link)
        dpg.set_item_user_data(conf.get("attr_1"), None)
        dpg.set_item_user_data(conf.get("attr_2"), None)
        dpg.delete_item(link)
        
with dpg.handler_registry():
    dpg.add_key_release_handler(key=dpg.mvKey_Delete, callback=delete_callback)


dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
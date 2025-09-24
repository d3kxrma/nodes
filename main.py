import dearpygui.dearpygui as dpg

dpg.create_context()
"""

Створити байнері трі з нодів. В функції ран отримати звязки між ними. Корнем (кінцевою нодою) буде той хто не має батька. всі інші матимуть. 
Звязки виглядають так
(29, 33)
(33, 42)
(47, 33)

лівий елемент це дитина, а правий батько. Незалежно від порядку створення звязків, нода 42 нематиме батька. Після побудови байнері трі, треба починати обчислення з неї. 
Можна буде відразу проставляти звязки в класи. 

"""

class InputNode:
    def spawn(self):
        with dpg.node(label="Number input", parent="editor", user_data=self):
            with dpg.node_attribute(label="Float input", attribute_type=dpg.mvNode_Attr_Output):
                self.inp = dpg.add_input_float(width=150)
                dpg.add_text(dpg.get_item_parent(dpg.get_item_parent(self.inp)))
    
    def calculate(self):
        return dpg.get_value(self.inp)
        
class SumNode:
    def __init__(self):
        self.A1: InputNode = None
        self.A2: InputNode = None
        
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

class MulNode:
    def __init__(self):
        self.A1: InputNode = None
        self.A2: InputNode = None
        
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
        dpg.set_value(item = self.r, value = f"Result: {self.A1.calculate() * self.A2.calculate()}")
        return self.A1.calculate() * self.A2.calculate()

class OutNode:
    def __init__(self):
        self.A1: InputNode = None
        
    def spawn(self):
        with dpg.node(label="Output", parent="editor", user_data=self):
            with dpg.node_attribute(label="Output"):
                self.txt = dpg.add_text("output")
                dpg.add_text(dpg.get_item_parent(dpg.get_item_parent(self.txt)))
                
    def set_children(self, children):
        self.A1 = children
            
    def calculate(self):
        dpg.set_value(item = self.txt, value = f"Result: {self.A1.calculate()}")
        


# callback runs when user attempts to connect attributes
def link_callback(sender, app_data):
    # app_data -> (link_id1, link_id2)
    dpg.add_node_link(app_data[0], app_data[1], parent=sender, user_data=(dpg.get_item_parent(app_data[0]), dpg.get_item_parent(app_data[1])))
    print(sender)
    print(app_data)
    
def call(sender, app_data):
    print(sender)
    print(app_data)

def run_callback(sender, app_data, user_data):
    print(dpg.get_item_children("editor"))
    nodes: list = dpg.get_item_children("editor")[1]
    for x in dpg.get_item_children("editor")[0]:
        lid = dpg.get_item_user_data(x)[0]
        l: InputNode = dpg.get_item_user_data(lid)
        r: OutNode = dpg.get_item_user_data(dpg.get_item_user_data(x)[1])
        
        r.set_children(l)
        nodes.remove(lid)
    
    dpg.get_item_user_data(nodes[0]).calculate()
        


# callback runs when user attempts to disconnect attributes
def delink_callback(sender, app_data):
    # app_data -> link_id
    dpg.delete_item(app_data)

def input_node(sender, app_data, user_data):
    i = InputNode()
    i.spawn()

def sum_node(sender, app_data, user_data):
   s = SumNode()
   s.spawn()

def output_node(sender, app_data, user_data):
    o = OutNode()
    o.spawn()

with dpg.window(label="Tutorial", width=1000, height=700):
    with dpg.group(horizontal=True):
        dpg.add_button(label="run", callback=run_callback)
        dpg.add_button(label="input", callback=input_node)
        dpg.add_button(label="multiply", callback=MulNode().spawn)
        dpg.add_button(label="sum", callback=sum_node)
        dpg.add_button(label="output", callback=output_node)
    
    
    with dpg.node_editor(callback=link_callback, delink_callback=delink_callback, minimap=True, minimap_location=3, tag="editor"):
        pass

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
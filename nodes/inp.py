import dearpygui.dearpygui as dpg

class InputNode:
    def spawn(self):
        with dpg.node(label="Float input", parent="editor", user_data=self):
            with dpg.node_attribute(label="Float input", attribute_type=dpg.mvNode_Attr_Output):
                self.inp = dpg.add_input_float(width=150)
                dpg.add_text(dpg.get_item_parent(dpg.get_item_parent(self.inp)))
    
    def calculate(self) -> float:
        return dpg.get_value(self.inp)
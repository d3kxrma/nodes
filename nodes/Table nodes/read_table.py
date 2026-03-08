import pandas as pd
import dearpygui.dearpygui as dpg
from base import Node

class ReadTableNode(Node):
    name = "Read Table"
    def __init__(self):
        super().__init__()
        
        with dpg.file_dialog(directory_selector=False, show=False, callback=self.file_selected, width=700, height=400) as self.file_dialog_id:
            dpg.add_file_extension(".csv", color=(0, 255, 0, 255))
    
    def file_selected(self, sender, app_data):
        selected_file = app_data['file_path_name']
        dpg.set_value(self.inp, selected_file)
    
    
    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type":pd.DataFrame}):
            with dpg.group(horizontal=True):
                self.inp = dpg.add_input_text(width=150, readonly=True)
                dpg.add_button(label="Select File", callback=lambda: dpg.show_item(self.file_dialog_id))
            
            self.chk = dpg.add_checkbox(label="First column as index", default_value=False)
            

    def calculate(self) -> pd.DataFrame:
        file_path = dpg.get_value(self.inp)
        if file_path:
            index_col = 0 if dpg.get_value(self.chk) else None
            
            return pd.read_csv(file_path, index_col=index_col)
        return pd.DataFrame()
import pandas as pd
import dearpygui.dearpygui as dpg
from base import Node

class InfoNode(Node):
    name = "Info Table"
        
    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.DataFrame}) as self.df:
            self.txt = dpg.add_text("Displays descriptive statistics of the input DataFrame.")

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type":pd.DataFrame}):
            self.table_id = dpg.add_table(header_row=True, policy=dpg.mvTable_SizingFixedFit, scrollX=True, borders_innerH=True,  borders_innerV=True, show=False, width=400, height=130)
            

    def calculate(self) -> str:
        df: pd.DataFrame = self.get_value(self.df)
        dpg.delete_item(self.table_id, children_only=True)
        if not df.empty:
            info = df.describe().T
            
            dpg.add_table_column(label="Name", parent=self.table_id)
            for name in info.columns:
                dpg.add_table_column(label=name, parent=self.table_id)
                
            for name, row in info.iterrows():
                with dpg.table_row(parent=self.table_id):
                    dpg.add_text(name)
                    for item in row:
                        dpg.add_text(str(item))
        
        dpg.show_item(self.table_id)
        
        return df
            
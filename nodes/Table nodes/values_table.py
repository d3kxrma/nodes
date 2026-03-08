import pandas as pd
import dearpygui.dearpygui as dpg
from base import Node

class ValuesNode(Node):
    name = "Values Table"
        
    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.DataFrame}) as self.df:
            self.txt = dpg.add_text("Displays values types of the input DataFrame.")

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type":pd.DataFrame}):
            self.table_id = dpg.add_table(header_row=True, policy=dpg.mvTable_SizingFixedFit, scrollX=True, borders_innerH=True,  borders_innerV=True, show=False, width=400, height=130)
            

    def calculate(self) -> str:
        df: pd.DataFrame = self.get_value(self.df)
        dpg.delete_item(self.table_id, children_only=True)
        if not df.empty:
            column_types = df.dtypes
            
            dpg.add_table_column(label="Column", parent=self.table_id)
            dpg.add_table_column(label="Data Type", parent=self.table_id)
            
            for column, dtype in column_types.items():
                with dpg.table_row(parent=self.table_id):
                    dpg.add_text(str(column))
                    dpg.add_text(str(dtype))
            
        
        dpg.show_item(self.table_id)
        
        return df
            
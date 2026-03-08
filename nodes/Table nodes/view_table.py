import pandas as pd
import dearpygui.dearpygui as dpg
from base import Node

class ViewNode(Node):
    name = "View Table"
    def __init__(self):
        super().__init__()
        self.operation = "Top"
    
    def on_select(self, sender, app_data, user_data):
        self.operation = app_data
        
    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.DataFrame}) as self.df:
            dpg.add_combo(
                items=["Top", "Bottom", "Random"],
                default_value="Top",
                callback=self.on_select,
                width=100
            )
            self.inp = dpg.add_input_int(width=100, default_value=5, label="Rows", min_value=1)
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type":pd.DataFrame}):
            self.table_id = dpg.add_table(header_row=True, policy=dpg.mvTable_SizingFixedFit, scrollX=True, borders_innerH=True,  borders_innerV=True, show=False, width=400, height=130)
            

    def calculate(self) -> str:
        df: pd.DataFrame = self.get_value(self.df)
        dpg.delete_item(self.table_id, children_only=True)
        if not df.empty:
            dpg.add_table_column(label="Index", parent=self.table_id)
            for name in df.columns:
                dpg.add_table_column(label=name, parent=self.table_id)
            
            rows = dpg.get_value(self.inp)
            if self.operation == "Top":
                df_samples = df.head(rows)
                
            elif self.operation == "Bottom":
                df_samples = df.tail(rows)
                
            elif self.operation == "Random":
                df_samples = df.sample(n=rows)
            
            for idx, row in df_samples.iterrows():
                with dpg.table_row(parent=self.table_id):
                    dpg.add_text(str(idx))
                    for item in row:
                        dpg.add_text(str(item))
                        
            dpg.show_item(self.table_id)
        
        return df
            
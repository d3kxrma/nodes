import pandas as pd
import dearpygui.dearpygui as dpg
from base import Node

class DropColumnsNode(Node):
    name = "Drop Columns"

    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.DataFrame}) as self.df_in:
            dpg.add_text("Columns to drop:")
            self.cols_input = dpg.add_input_text(width=150, hint="col1, col2")
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": pd.DataFrame}):
            dpg.add_text("Output DF")

    def calculate(self) -> pd.DataFrame:
        df: pd.DataFrame = self.get_value(self.df_in)
        cols_str = dpg.get_value(self.cols_input)
        if df is not None and cols_str:
            cols_to_drop = [c.strip() for c in cols_str.split(",") if c.strip() in df.columns]
            return df.drop(columns=cols_to_drop)
        return df
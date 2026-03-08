import pandas as pd
import dearpygui.dearpygui as dpg
from base import Node

class HandleNANode(Node):
    name = "Handle NA"

    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.DataFrame}) as self.df_in:
            self.method = dpg.add_combo(
                items=["Drop NA", "Fill with 0", "Fill with Mean", "Fill with Median"],
                default_value="Drop NA",
                width=150
            )
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": pd.DataFrame}):
            dpg.add_text("Cleaned DF")

    def calculate(self) -> pd.DataFrame:
        df: pd.DataFrame = self.get_value(self.df_in)
        if df is None: 
            return None
        
        method = dpg.get_value(self.method)
        try:
            if method == "Drop NA":
                return df.dropna().copy()
            elif method == "Fill with 0":
                return df.fillna(0).copy()
            elif method == "Fill with Mean":
                return df.fillna(df.mean(numeric_only=True)).copy()
            elif method == "Fill with Median":
                return df.fillna(df.median(numeric_only=True)).copy()
        except Exception as e:
            print(f"Handle NA error: {e}")
        return df
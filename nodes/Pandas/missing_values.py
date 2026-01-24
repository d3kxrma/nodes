import pandas as pd
import dearpygui.dearpygui as dpg
from base import Node

class MissingValuesNode(Node):
    name = "Handle Missing"

    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.DataFrame}) as self.df_in:
            self.mode = dpg.add_combo(
                items=["Drop Rows", "Fill with 0", "Fill Mean", "Fill Median"],
                default_value="Drop Rows",
                width=120
            )
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": pd.DataFrame}):
            dpg.add_text("Cleaned DF")

    def calculate(self) -> pd.DataFrame:
        df: pd.DataFrame = self.get_value(self.df_in)
        
        if df is None: 
            return None
        
        mode = dpg.get_value(self.mode)
        if mode == "Drop Rows":
            return df.dropna()
        elif mode == "Fill with 0":
            return df.fillna(0)
        elif mode == "Fill Mean":
            return df.fillna(df.mean(numeric_only=True))
        elif mode == "Fill Median":
            return df.fillna(df.median(numeric_only=True))
        return df
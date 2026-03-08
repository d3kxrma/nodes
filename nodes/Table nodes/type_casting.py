import pandas as pd
import dearpygui.dearpygui as dpg
from base import Node

class TypeCastNode(Node):
    name = "Type Casting"

    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.DataFrame}) as self.df_in:
            self.col_name = dpg.add_input_text(width=120, hint="Column name")
            self.new_type = dpg.add_combo(
                items=["int64", "float64", "str", "datetime64[ns]", "bool"],
                default_value="float64",
                width=120
            )
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": pd.DataFrame}):
            dpg.add_text("Casted DF")

    def calculate(self) -> pd.DataFrame:
        df: pd.DataFrame = self.get_value(self.df_in)
        col = dpg.get_value(self.col_name)
        target_type = dpg.get_value(self.new_type)
        
        if df is not None and col in df.columns:
            new_df = df.copy()
            try:
                if target_type == "datetime64[ns]":
                    new_df[col] = pd.to_datetime(new_df[col])
                else:
                    new_df[col] = new_df[col].astype(target_type)
                return new_df
            except Exception:
                return df
        return df
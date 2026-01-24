import pandas as pd
import dearpygui.dearpygui as dpg
from base import Node

class RenameColumnsNode(Node):
    name = "Rename Columns"

    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.DataFrame}) as self.df_in:
            dpg.add_text("Mapping (old:new):")
            self.map_input = dpg.add_input_text(width=150, hint="old:new, col1:age")
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": pd.DataFrame}):
            dpg.add_text("Renamed DF")

    def calculate(self) -> pd.DataFrame:
        df: pd.DataFrame = self.get_value(self.df_in)
        mapping_str = dpg.get_value(self.map_input)
        if df is not None and mapping_str:
            try:
                mapping = dict(item.split(":") for item in mapping_str.split(",") if ":" in item)
                mapping = {k.strip(): v.strip() for k, v in mapping.items()}
                return df.rename(columns=mapping)
            except Exception:
                return df
        return df
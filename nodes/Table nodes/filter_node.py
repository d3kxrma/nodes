import pandas as pd
import dearpygui.dearpygui as dpg
from base import Node

class FilterNode(Node):
    name = "Filter (Query)"

    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.DataFrame}) as self.df_in:
            dpg.add_text("Expression:")
            self.query_input = dpg.add_input_text(width=150, hint="column > 10")
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": pd.DataFrame}):
            dpg.add_text("Filtered DF")

    def calculate(self) -> pd.DataFrame:
        df: pd.DataFrame = self.get_value(self.df_in)
        query_str = dpg.get_value(self.query_input)
        
        if df is not None and query_str:
            try:
                return df.query(query_str).copy()
            except Exception as e:
                print(f"Filter error: {e}")
                return df
        return df
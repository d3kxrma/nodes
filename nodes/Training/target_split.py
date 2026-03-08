import pandas as pd
import dearpygui.dearpygui as dpg
from base import Node

class SplitXYNode(Node):
    name = "Split X / y"

    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.DataFrame}) as self.df_in:
            dpg.add_text("Target Column:")
            self.target_input = dpg.add_input_text(width=150, hint="target_name")
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": pd.DataFrame}) as self.x_out:
            dpg.add_text("Features (X)")
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": pd.DataFrame}) as self.y_out:
            dpg.add_text("Target (y)")

    def calculate(self) -> dict:
        df: pd.DataFrame = self.get_value(self.df_in)
        target_col = dpg.get_value(self.target_input)
        
        if df is not None and target_col in df.columns:
            try:
                y = df[[target_col]].copy()
                X = df.drop(columns=[target_col])
                
                return {
                    self.x_out: X,
                    self.y_out: y
                }
            except Exception as e:
                print(f"Split error: {e}")
                
        return {self.x_out: df, self.y_out: pd.DataFrame()}
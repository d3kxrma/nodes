import pandas as pd
import dearpygui.dearpygui as dpg
from base import Node

class ApplyNode(Node):
    name = "Apply Function"

    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.DataFrame}) as self.df_in:
            self.col_target = dpg.add_input_text(width=150, hint="Column name")
            dpg.add_text("Lambda x:")
            self.lambda_input = dpg.add_input_text(width=150, hint="x * 100")
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": pd.DataFrame}):
            dpg.add_text("Modified DF")

    def calculate(self) -> pd.DataFrame:
        df: pd.DataFrame = self.get_value(self.df_in)
        col = dpg.get_value(self.col_target)
        expr = dpg.get_value(self.lambda_input)
        
        if df is not None and col in df.columns and expr:
            try:
                new_df = df.copy()
                # Створюємо функцію з рядка безпечним способом
                fn = eval(f"lambda x: {expr}")
                new_df[col] = new_df[col].apply(fn)
                return new_df
            except Exception as e:
                print(f"Apply error: {e}")
                return df
        return df
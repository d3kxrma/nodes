import pandas as pd
import dearpygui.dearpygui as dpg
from base import Node
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, MaxAbsScaler

class ScalerNode(Node):
    name = "Data Scaler"

    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.DataFrame}) as self.df_in:
            self.scaler_type = dpg.add_combo(
                items=["Standard Scaler", "MinMax Scaler", "Robust Scaler", "MaxAbs Scaler"],
                default_value="Standard Scaler",
                width=160
            )
            dpg.add_text("Columns (empty = all numeric):")
            self.cols_input = dpg.add_input_text(width=160, hint="col1, col2")
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": pd.DataFrame}):
            dpg.add_text("Scaled DF")

    def calculate(self) -> pd.DataFrame:
        df: pd.DataFrame = self.get_value(self.df_in)
        cols_str = dpg.get_value(self.cols_input)
        scaler_choice = dpg.get_value(self.scaler_type)
        
        if df is not None:
            new_df = df.copy()
            try:
                match scaler_choice:
                    case "Standard Scaler":
                        scaler = StandardScaler()
                    case "MinMax Scaler":
                        scaler = MinMaxScaler()
                    case "Robust Scaler":
                        scaler = RobustScaler()
                    case "MaxAbs Scaler":
                        scaler = MaxAbsScaler()
                    case _:
                        return df

                if cols_str:
                    cols = [c.strip() for c in cols_str.split(",") if c.strip() in df.columns]
                else:
                    cols = df.select_dtypes(include=['number']).columns
                
                if len(cols) > 0:
                    new_df[cols] = scaler.fit_transform(new_df[cols])
                return new_df
                
            except Exception as e:
                print(f"Scaler error: {e}")
                return df
        return df
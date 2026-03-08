import pandas as pd
import dearpygui.dearpygui as dpg
from base import Node
from sklearn.impute import KNNImputer

class KNNImputerNode(Node):
    name = "KNN Imputer"

    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.DataFrame}) as self.df_in:
            dpg.add_text("Neighbors (k):")
            self.n_neighbors = dpg.add_input_int(width=100, default_value=5, min_value=1)
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": pd.DataFrame}):
            dpg.add_text("Imputed DF")

    def calculate(self) -> pd.DataFrame:
        df: pd.DataFrame = self.get_value(self.df_in)
        if df is not None:
            try:
                k = dpg.get_value(self.n_neighbors)
                imputer = KNNImputer(n_neighbors=k)
                new_df = df.copy()
                
                num_cols = new_df.select_dtypes(include=['number']).columns
                if len(num_cols) > 0:
                    new_df[num_cols] = imputer.fit_transform(new_df[num_cols])
                return new_df
            except Exception as e:
                print(f"KNN Imputer error: {e}")
                return df
        return df
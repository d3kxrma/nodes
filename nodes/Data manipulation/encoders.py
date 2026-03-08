import pandas as pd
import dearpygui.dearpygui as dpg
from base import Node
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder, OneHotEncoder

class EncoderNode(Node):
    name = "Data Encoder"

    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.DataFrame}) as self.df_in:
            self.encoder_type = dpg.add_combo(
                items=["Ordinal Encoder", "Label Encoder", "One-Hot Encoder"],
                default_value="Ordinal Encoder",
                width=160
            )
            dpg.add_text("Columns (empty = all text/category):")
            self.cols_input = dpg.add_input_text(width=160, hint="col1, col2")
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": pd.DataFrame}):
            dpg.add_text("Encoded DF")

    def calculate(self) -> pd.DataFrame:
        df: pd.DataFrame = self.get_value(self.df_in)
        cols_str = dpg.get_value(self.cols_input)
        enc_choice = dpg.get_value(self.encoder_type)
        
        if df is not None:
            new_df = df.copy()
            try:
                if cols_str:
                    cols = [c.strip() for c in cols_str.split(",") if c.strip() in df.columns]
                else:
                    cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                
                if len(cols) == 0:
                    return new_df

                if enc_choice == "Ordinal Encoder":
                    encoder = OrdinalEncoder()
                    new_df[cols] = encoder.fit_transform(new_df[cols])

                elif enc_choice == "Label Encoder":
                    encoder = LabelEncoder()
                    for col in cols:
                        new_df[col] = encoder.fit_transform(new_df[col])

                elif enc_choice == "One-Hot Encoder":
                    encoder = OneHotEncoder(sparse_output=False, drop='first')
                    encoded_data = encoder.fit_transform(new_df[cols])
                    
                    new_col_names = encoder.get_feature_names_out(cols)
                    
                    encoded_df = pd.DataFrame(encoded_data, columns=new_col_names, index=new_df.index)
                    
                    new_df = new_df.drop(columns=cols)
                    new_df = pd.concat([new_df, encoded_df], axis=1)

                return new_df
                
            except Exception as e:
                print(f"Encoder error: {e}")
                return df
        return df
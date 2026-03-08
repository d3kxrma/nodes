import pandas as pd
import dearpygui.dearpygui as dpg
from base import Node

class ValueCountsNode(Node):
    name = "Value Counts"

    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.DataFrame}) as self.df_in:
            self.col_name = dpg.add_input_text(width=150, hint="Column name")
            self.normalize = dpg.add_checkbox(label="Relative (%)", default_value=False, callback=self.calculate)
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": pd.DataFrame}):
            self.table_id = dpg.add_table(
                header_row=True, 
                policy=dpg.mvTable_SizingFixedFit,
                scrollX=True, 
                borders_innerH=True, 
                borders_innerV=True, 
                show=False, 
                width=200, 
                height=150
            )

    def calculate(self) -> pd.DataFrame:
        df: pd.DataFrame = self.get_value(self.df_in)
        col = dpg.get_value(self.col_name)
        is_norm = dpg.get_value(self.normalize)
        
        dpg.delete_item(self.table_id, children_only=True)
        dpg.hide_item(self.table_id)

        if df is not None and col in df.columns:
            counts_series = df[col].value_counts(normalize=is_norm)
            counts_df = counts_series.reset_index()
            counts_df.columns = ['value', 'count']

            dpg.add_table_column(label="Value", parent=self.table_id)
            dpg.add_table_column(label="Count", parent=self.table_id)

            for _, row in counts_df.iterrows():
                with dpg.table_row(parent=self.table_id):
                    dpg.add_text(str(row.iloc[0])) 
                    
                    val_raw = row.iloc[1]
                    val_formatted = f"{val_raw:.2%}" if is_norm else str(val_raw)
                    dpg.add_text(val_formatted)
            
            dpg.show_item(self.table_id)
            return df
            
        return df
import pandas as pd
import dearpygui.dearpygui as dpg
from base import Node

class CorrelationMatrixNode(Node):
    name = "Correlation Matrix"

    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.DataFrame}) as self.in_x:
            dpg.add_text("X (Features)")
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": None}) as self.in_y:
            dpg.add_text("y (Target) [Optional]")
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": pd.DataFrame}) as self.out_x:
            dpg.add_text("X (Out)")
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": None}) as self.out_y:
            dpg.add_text("y (Out)")
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": pd.DataFrame}) as self.out_corr:
            dpg.add_text("Correlation DF")

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            with dpg.plot(label="Correlation Heatmap", width=450, height=450, no_menus=True) as self.plot:
                dpg.add_plot_legend()
                self.xaxis = dpg.add_plot_axis(dpg.mvXAxis, label="", no_gridlines=True, no_tick_marks=True)
                self.yaxis = dpg.add_plot_axis(dpg.mvYAxis, label="", no_gridlines=True, no_tick_marks=True)
                dpg.bind_colormap(self.plot, dpg.mvPlotColormap_Jet)

    def calculate(self) -> dict:
        X = self.get_value(self.in_x)
        y = self.get_value(self.in_y)
        
        dpg.delete_item(self.yaxis, children_only=True)
        corr_df = pd.DataFrame()

        if X is not None and not X.empty:
            try:
                combined_df = X.copy()
                
                if y is not None:
                    if isinstance(y, pd.DataFrame):
                        for col in y.columns:
                            combined_df[col] = y[col]
                    elif isinstance(y, pd.Series):
                        name = y.name if y.name else "Target"
                        combined_df[name] = y
                    else:
                        combined_df["Target"] = y

                num_df = combined_df.select_dtypes(include=['number'])
                
                if not num_df.empty:
                    corr_df = num_df.corr().fillna(0)
                    
                    rows, cols = corr_df.shape
                    flat_corr = corr_df.values.flatten().astype(float).tolist()
                    
                    dpg.add_heat_series(
                        flat_corr, rows, cols, 
                        scale_min=-1.0, scale_max=1.0, 
                        format="%0.2f",
                        bounds_min=(0, 0),         
                        bounds_max=(cols, rows),   
                        parent=self.yaxis
                    )
                    
                    dpg.set_axis_limits(self.xaxis, 0, cols)
                    dpg.set_axis_limits(self.yaxis, 0, rows)
                    
                    ticks_x = tuple((str(col), i + 0.5) for i, col in enumerate(corr_df.columns))
                    
                    ticks_y = tuple((str(col), rows - i - 0.5) for i, col in enumerate(corr_df.index))
                    
                    dpg.set_axis_ticks(self.xaxis, ticks_x)
                    dpg.set_axis_ticks(self.yaxis, ticks_y)
                    
            except Exception as e:
                print(f"Correlation Matrix Error: {e}")
                
        return {
            self.out_x: X,
            self.out_y: y,
            self.out_corr: corr_df
        }
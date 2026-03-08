import dearpygui.dearpygui as dpg
import pandas as pd
from base import Node
from sklearn.model_selection import train_test_split

class TrainTestSplitNode(Node):
    name = "Train-Test Split"

    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.DataFrame}) as self.in_x:
            dpg.add_text("X (Features)")
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.DataFrame}) as self.in_y:
            dpg.add_text("y (Target)")
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.test_size = dpg.add_input_float(label="Test Size", default_value=0.2, width=120, max_value=0.99, min_value=0.01)
            self.random_state = dpg.add_input_int(label="Random", default_value=42, width=120)

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": pd.DataFrame}) as self.out_x_train:
            dpg.add_text("X_train")
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": pd.DataFrame}) as self.out_x_test:
            dpg.add_text("X_test")
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": pd.Series}) as self.out_y_train:
            dpg.add_text("y_train")
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data={"data_type": pd.Series}) as self.out_y_test:
            dpg.add_text("y_test")

    def calculate(self) -> dict:
        X: pd.DataFrame = self.get_value(self.in_x)
        y: pd.DataFrame = self.get_value(self.in_y)
        
        t_size = dpg.get_value(self.test_size)
        r_state = dpg.get_value(self.random_state)

        if X is None or y is None or X.empty or y.empty:
            return {}

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=t_size, random_state=r_state)
        
        if isinstance(y_train, pd.DataFrame):
            y_train = y_train.iloc[:, 0]
        if isinstance(y_test, pd.DataFrame):
            y_test = y_test.iloc[:, 0]
        
        return {
            self.out_x_train: X_train, 
            self.out_x_test: X_test, 
            self.out_y_train: y_train, 
            self.out_y_test: y_test
        }
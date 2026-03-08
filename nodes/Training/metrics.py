import dearpygui.dearpygui as dpg
import pandas as pd
from base import Node

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

class MetricsNode(Node):
    name = "Classification Metrics"

    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.Series}) as self.in_y_true:
            dpg.add_text("y_true")
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": pd.Series}) as self.in_y_pred:
            dpg.add_text("y_pred (Predictions)")
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.txt_acc = dpg.add_text("Accuracy: -")
            self.txt_prec = dpg.add_text("Precision: -")
            self.txt_rec = dpg.add_text("Recall: -")
            self.txt_f1 = dpg.add_text("F1 Score: -")

    def calculate(self):
        y_true = self.get_value(self.in_y_true)
        y_pred = self.get_value(self.in_y_pred)

        if y_true is not None and y_pred is not None:
            if isinstance(y_pred, pd.DataFrame):
                y_pred_series = y_pred.iloc[:, 0]
            else:
                y_pred_series = y_pred

            acc = accuracy_score(y_true, y_pred_series)
            prec = precision_score(y_true, y_pred_series, average='weighted', zero_division=0)
            rec = recall_score(y_true, y_pred_series, average='weighted', zero_division=0)
            f1 = f1_score(y_true, y_pred_series, average='weighted', zero_division=0)

            dpg.set_value(self.txt_acc, f"Accuracy: {acc:.4f}")
            dpg.set_value(self.txt_prec, f"Precision: {prec:.4f}")
            dpg.set_value(self.txt_rec, f"Recall: {rec:.4f}")
            dpg.set_value(self.txt_f1, f"F1 Score: {f1:.4f}")
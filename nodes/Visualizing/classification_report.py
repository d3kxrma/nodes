from sklearn.metrics import classification_report
import pandas as pd
import dearpygui.dearpygui as dpg
from base import Node

class ClassificationReportNode(Node):
    name = "Classification Report"

    def design(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": None}) as self.y_true_in:
            dpg.add_text("y_true (Actual)")
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data={"data_type": None}) as self.y_pred_in:
            dpg.add_text("y_pred (Predicted)")
            
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output):
            self.table_id = dpg.add_table(
                header_row=True, 
                borders_innerH=True, 
                borders_innerV=True, 
                width=450, 
                height=220, 
                scrollY=True,
                show=False
            )

    def calculate(self):
        y_true = self.get_value(self.y_true_in)
        y_pred = self.get_value(self.y_pred_in)

        dpg.delete_item(self.table_id, children_only=True)
        dpg.hide_item(self.table_id)

        if y_true is not None and y_pred is not None:
            try:
                yt = y_true.iloc[:, 0] if isinstance(y_true, pd.DataFrame) else y_true
                yp = y_pred.iloc[:, 0] if isinstance(y_pred, pd.DataFrame) else y_pred
                
                report_dict = classification_report(yt, yp, output_dict=True)
                
                headers = ["Metric", "Precision", "Recall", "F1-Score", "Support"]
                for h in headers:
                    dpg.add_table_column(label=h, parent=self.table_id)
                    
                for key, metrics in report_dict.items():
                    with dpg.table_row(parent=self.table_id):
                        if str(key).isdigit():
                            dpg.add_text(f"Class {key}")
                        else:
                            dpg.add_text(str(key))
                        
                        if isinstance(metrics, dict):
                            dpg.add_text(f"{metrics['precision']:.3f}")
                            dpg.add_text(f"{metrics['recall']:.3f}")
                            dpg.add_text(f"{metrics['f1-score']:.3f}")
                            
                            support = metrics['support']
                            if isinstance(support, float) and support.is_integer():
                                dpg.add_text(str(int(support)))
                            else:
                                dpg.add_text(f"{support:.2f}" if isinstance(support, float) else str(support))
                                
                        else:
                            dpg.add_text("")
                            dpg.add_text("")
                            dpg.add_text(f"{metrics:.3f}")
                            
                            total_support = int(report_dict['macro avg']['support'])
                            dpg.add_text(str(total_support))
                            
                dpg.show_item(self.table_id)
            except Exception as e:
                print(f"Classification Report Error: {e}")
                
        return None
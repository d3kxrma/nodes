import dearpygui.dearpygui as dpg
from base import Node
dpg.create_context()

"""
панель для додавання нодів, використавння бейз ноди, по можливості розширена інформація про ноди, валідація вихідних та вхідниї даних (типи)
"""
      
def open_modal_callback(text: str, name:str="Error"):
    with dpg.window(label=name, modal=True, show=False, tag="modal_window"):
        dpg.add_text(text)
        dpg.add_button(label="Close", callback=lambda: dpg.delete_item("modal_window"))
    dpg.show_item("modal_window")

def link_callback(sender, app_data):
    left_parent = dpg.get_item_parent(app_data[0])
    dpg.add_node_link(app_data[0], app_data[1], parent=sender, user_data=left_parent)
    dpg.set_item_user_data(app_data[1], dpg.get_item_user_data(left_parent))
    dpg.set_item_user_data(app_data[0], app_data[1])
    print(sender)
    print(app_data)
    print("^^^")

def delink_callback(sender, app_data):
    conf = dpg.get_item_configuration(app_data)
    right = conf.get("attr_2")
    left = conf.get("attr_1")
    dpg.set_item_user_data(right, None)
    dpg.set_item_user_data(left, None)
    
    dpg.delete_item(app_data)

def call(sender, app_data):
    print(sender)
    print(app_data)

def run_callback(sender, app_data, user_data):
    print(dpg.get_item_children("editor"))
    editor_children = dpg.get_item_children("editor")
    
    if not editor_children[0]: # if any connection exists
        open_modal_callback("No connection found. Connect at least 2 nodes.")
        return
    
    nodes: list = editor_children[1]
    for x in dpg.get_item_children("editor")[0]:
        nodes.remove(dpg.get_item_user_data(x))
    
    if len(nodes) == 1:
        dpg.get_item_user_data(nodes[0]).calculate()
    elif len(nodes) >= 2:
        open_modal_callback("Run is not possible due to 2 or more chains detected. Remove all unnecessary chains.")
    else:
        open_modal_callback("Run is not possible because no chains have been detected.")

with dpg.window(label="Tutorial", width=1000, height=700):
    with dpg.group(horizontal=True):
        dpg.add_button(label="run", callback=run_callback)
        dpg.add_button(label="input", callback=input_node)
        dpg.add_button(label="multiply", callback=mul_node)
        dpg.add_button(label="sum", callback=sum_node)
        dpg.add_button(label="output", callback=output_node)
    
    
    with dpg.node_editor(callback=link_callback, delink_callback=delink_callback, minimap=True, minimap_location=3, tag="editor"):
        pass
    
def delete_callback(): 
    nodes = dpg.get_selected_nodes("editor")
    for node in nodes:
        obj: Node = dpg.get_item_user_data(node)
        obj.delete()
    
    links = dpg.get_selected_links("editor")
    for link in links:
        conf = dpg.get_item_configuration(link)
        dpg.set_item_user_data(conf.get("attr_1"), None)
        dpg.set_item_user_data(conf.get("attr_2"), None)
        dpg.delete_item(link)
        
with dpg.handler_registry():
    dpg.add_key_release_handler(key=dpg.mvKey_Delete, callback=delete_callback)


dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
import os
import importlib
import dearpygui.dearpygui as dpg
from base import Node

dpg.create_context()

NODES_DIR = "nodes"

def open_modal_callback(text: str, name: str = "Error"):
    with dpg.window(label=name, modal=True, show=False, tag="modal_window"):
        dpg.add_text(text)
        dpg.add_button(label="Close", callback=lambda: dpg.delete_item("modal_window"))
    dpg.set_value("info_text", text)
    dpg.show_item("modal_window")


def link_callback(sender, app_data):
    out_data = dpg.get_item_user_data(app_data[0])
    inp_data = dpg.get_item_user_data(app_data[1])
    
    out_type = out_data.get("data_type")
    inp_type = inp_data.get("data_type")
    
    if inp_type != out_type and inp_type is not None:
        open_modal_callback(f"Type mismatch: cannot connect {out_type.__name__} to {inp_type.__name__}.")
        return
    
    left_parent = dpg.get_item_parent(app_data[0])
    dpg.add_node_link(app_data[0], app_data[1], parent=sender, user_data=left_parent)
    
    # inp_data["left_node"] = dpg.get_item_user_data(left_parent)
    inp_data["left_node"] = app_data[0]
    out_data["right_node"] = app_data[1]
    
    dpg.set_item_user_data(app_data[1], inp_data)
    dpg.set_item_user_data(app_data[0], out_data)
    


def delink_callback(sender, app_data):
    conf = dpg.get_item_configuration(app_data)
    right = conf.get("attr_2")
    left = conf.get("attr_1")
    
    right_data = dpg.get_item_user_data(right)
    left_data = dpg.get_item_user_data(left)
    
    del right_data["left_node"]
    del left_data["right_node"]

    dpg.set_item_user_data(right, right_data)
    dpg.set_item_user_data(left, left_data)
    dpg.delete_item(app_data)


def run_callback():
    editor_children = dpg.get_item_children("editor")
    if not editor_children[0]:  # if any connection exists
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


def delete_callback():
    nodes = dpg.get_selected_nodes("editor")
    for node in nodes:
        obj: Node = dpg.get_item_user_data(node)
        obj.delete()

    links = dpg.get_selected_links("editor")
    for link in links:
        conf = dpg.get_item_configuration(link)
        
        left_data = dpg.get_item_user_data(conf.get("attr_1"))
        right_data = dpg.get_item_user_data(conf.get("attr_2"))
        del left_data["right_node"]
        del right_data["left_node"]
        
        dpg.set_item_user_data(conf.get("attr_1"), left_data)
        dpg.set_item_user_data(conf.get("attr_2"), right_data)
        dpg.delete_item(link)


with dpg.handler_registry():
    dpg.add_key_release_handler(key=dpg.mvKey_Delete, callback=delete_callback)
    dpg.add_key_release_handler(key=dpg.mvKey_F5, callback=run_callback)

def load_node_classes():
    node_map = {}

    for category in sorted(os.listdir(NODES_DIR)):
        category_path = os.path.join(NODES_DIR, category)
        if not os.path.isdir(category_path):
            continue

        category_nodes = []
        for filename in sorted(os.listdir(category_path)):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = f"{NODES_DIR}.{category}.{filename[:-3]}"
                module = importlib.import_module(module_name)

                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, Node) and attr is not Node:
                        category_nodes.append(attr)

        if category_nodes:
            node_map[category] = category_nodes

    return node_map


def create_nodes_panel(node_map:dict):
    with dpg.child_window(width=250, border=True):
        
        for category, classes in node_map.items():
            
            with dpg.collapsing_header(label=category, default_open=True):
                
                for cls in classes:
                    if not cls.visible:
                        continue
                    
                    def make_callback(cls):
                        def callback(sender, app_data, user_data):
                            node = cls()
                            node.spawn()
                        return callback

                    btn = dpg.add_button(label=cls.name, callback=make_callback(cls))
                    with dpg.drag_payload(parent=btn, drag_data=cls):
                        dpg.add_text(cls.name)
                    
def on_drop(sender, app_data, user_data):
    pos = dpg.get_mouse_pos(local=False)
    ref_node = dpg.get_item_children("editor", slot=1)
    if not ref_node:
        ref_screen_pos = [0, 0]
        ref_grid_pos = [0, 0]
    else:
        ref_node = ref_node[-1]
        ref_screen_pos = dpg.get_item_rect_min(ref_node)
        ref_grid_pos = dpg.get_item_pos(ref_node)
        
    NODE_PADDING = (15, 8)

    pos[0] = pos[0] - (ref_screen_pos[0] - NODE_PADDING[0]) + ref_grid_pos[0]
    pos[1] = pos[1] - (ref_screen_pos[1] - NODE_PADDING[1]) + ref_grid_pos[1]
    node = app_data()
    node.spawn(pos)


with dpg.window(label="Main", tag="main"):
    with dpg.child_window(tag="content", autosize_x=True, autosize_y=False, height=-25, border=False):
        with dpg.group(horizontal=True):
            node_map = load_node_classes()
            create_nodes_panel(node_map)
            
            with dpg.group(drop_callback=on_drop):
                with dpg.node_editor(callback=link_callback, delink_callback=delink_callback, minimap=True, minimap_location=3, tag="editor"):
                    pass
        
    with dpg.group(horizontal=True, height=20):
        dpg.add_button(label="run", callback=run_callback)
        dpg.add_text("Info", tag="info_text")


dpg.create_viewport(title='Node editor', width=1280, height=720, x_pos=500, y_pos=500)
dpg.set_primary_window("main", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
""" This code will retrieve the information of your clipboard and
will check the context and copied node to create a fetch or 
object merge which will be linked to the clipboard content. """

import hou

def pasteNode():
    """ Create fetch or object merge based on context and node. """
    
    # Get information from clipboard.
    node = hou.ui.getTextFromClipboard()
    
    # Get information of the current network pane tabe.
    network_pane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    obj = hou.node(network_pane.pwd().path())
    
    # Get position of the cursor inside the network pane.
    pos = network_pane.cursorPosition()
    
    # Get category and name of the pane.
    cat = obj.type().category().name()
    name = obj.type().name()
    
    # Set render catergories and cache nodes.
    render_cat = ["ropnet", "out", "topnet"]
    cache_nodes = ["filip_cache", "filecache"]
    
    # Try to run and if no context, rasie exception.
    try:
    
        # Check if information from clipboard is a node.
        if hou.node(node):
            
            # Get node type from path.
            node_cat = hou.node(node).type().name()
            node_name = hou.node(node).name()
            obj_merge_name = "IN_" + node_name
            
            # Check if we are in render or top context.
            if name in render_cat or "Driver" in cat:
                
                # Look for coincidences for cache nodes.
                for cache in cache_nodes:
                    if cache in node_cat:
                        
                        # If file cache node is found, add /render.
                        node = node + "/render"
                
                # Check if topnet context.        
                if name == "topnet":
                
                    # Create top fetches.
                    fetch = obj.createNode("ropfetch", node_name=obj_merge_name)
                    fetch.parm("roppath").set(node)
                    fetch.setPosition(pos)
                    customizeNode(fetch)
                else:
                    
                    # Create rop fetches.
                    fetch = obj.createNode("fetch", node_name=obj_merge_name)
                    fetch.parm("source").set(node)
                    fetch.setPosition(pos)
                    customizeNode(fetch)   
            else:
                
                # Create merge nodes.
                merge = obj.createNode("object_merge", node_name=obj_merge_name)
                merge.parm("objpath1").set(node)
                merge.setPosition(pos)
                customizeNode(merge)       
        else:
            
            # If not a node, display message.
            hou.ui.displayMessage("Copy a houdini node before paste.")
    except:
    
        # Exception if not in proper context.
        hou.ui.displayMessage("Paste the node in a different context.")

def customizeNode(node):
    """ Customize node appearance. """

    # Set user node shape and color.
    node.setUserData("nodeshape", "chevron_down")
    node.setColor(hou.Color((0, 0.28, 0.67)))
""" This code will retrieve the information of your clipboard and
will check the context and copied node to create a fetch or 
object merge which will be linked to the clipboard content. """

import hou

def pasteNode():
    """ Create fetch or object merge based on context and node. """
    
    # Get information from clipboard.
    n = hou.ui.getTextFromClipboard()
    
    # Get information of the current network pane tabe.
    network_pane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    obj = hou.node(network_pane.pwd().path())
    
    # Get position of the cursor inside the network pane.
    cursor_pos = network_pane.cursorPosition()
    
    # Get category and name of the pane.
    cat = obj.type().category().name()
    name = obj.type().name()
    
    # Set render catergories and cache nodes.
    render_cat = ["ropnet", "out", "topnet"]
    cache_nodes = ["filip_cache", "filecache"]
    
    # Try to run and if no context, rasie exception.
    try:
        
        # Get all the copied nodes.
        node_list = n.split(" ")
        errors = 0
        node_num = 0

        for node in node_list:
        
            # Compute node position.
            pos = hou.Vector2((cursor_pos.x() + 3*node_num, cursor_pos.y()))
            
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
                        customizeNode(fetch, pos)
                    else:
                        
                        # Create rop fetches.
                        fetch = obj.createNode("fetch", node_name=obj_merge_name)
                        fetch.parm("source").set(node)
                        customizeNode(fetch, pos)   
                else:
                    
                    # Create merge nodes.
                    merge = obj.createNode("object_merge", node_name=obj_merge_name)
                    merge.parm("objpath1").set(node)
                    customizeNode(merge, pos)

                node_num += 1
                
            else:

                # Add number errors.
                errors+=1
                continue

        if errors>0 and node_num==0:  

            # If errors and no nodes, display message.
            hou.ui.displayMessage("Copy a Houdini node.")
        
        elif errors>0 and node_num!=0:
            
            # If errors, but nodes, display message.
            hou.ui.displayMessage("Maybe you copied a non-valid object.")
                   
    except:
    
        # Exception if not in proper context.
        hou.ui.displayMessage("Paste the node in a different context.")

def customizeNode(node, pos):
    """ Customize node appearance. """

    # Set user node shape and color.
    node.setUserData("nodeshape", "chevron_down")
    node.setColor(hou.Color((0, 0.28, 0.67)))
    node.setPosition(pos)
import tkinter as tk
import hou

root = tk.Tk()
root.withdraw()
root.update()
node = root.call("clipboard", "get")
root.destroy()

network_pane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
obj = hou.node(network_pane.pwd().path())
pos = network_pane.cursorPosition()

if hou.node(node):
    merge = obj.createNode("object_merge")
    merge.parm("objpath1").set(node)
    merge.setPosition(pos)
else:
    hou.ui.displayMessage("Copy a houdini node before pase.")

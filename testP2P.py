try:
    from pythonp2p import Node
except:
    from setup import setup
    setup()
    from pythonp2p import Node


class NodeTest(Node):
  def on_message(message, sender, private):
    print(message)
node = NodeTest(p)
node.start()
node.connect_to("")
node.send_message("slt la zone", reciever=None)
node.savestate()
node.stop()
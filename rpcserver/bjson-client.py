import bjsonrpc
c = bjsonrpc.connect(port=8002)
print ("::> %s\n" % c.call.hello(name = "john"))
print ("::> %s\n" % c.call.hello("arnold"))

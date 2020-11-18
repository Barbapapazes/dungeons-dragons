from network import Network

n = Network()
print(n.get_p())


while True:
    try:
        game = n.send("get")
    except:
        break

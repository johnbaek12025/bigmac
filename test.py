role = {'vendor': 1, 'customer': 2}

x = 2
if x := role.get('vendor', 1):
    print(x)

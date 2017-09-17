fruitPrices = {'apples': 2.00, 'oranges': 1.5, 'pears' : 1.75}

def buyFruit(fruit,numPounds):
    if fruit not in fruitPrices:
        print "sorry we don't have %s" %(fruit)
    else:
        cost = fruitPrices[fruit] * numPounds
        print "Tha'll be %f please" % (cost)
if __name__ == '__main__':
    buyFruit('apples', 2.4)
    buyFruit('coconuts', 2)

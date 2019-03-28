def fuc():
    params = ['r','x']
    
    print("(-----------------------------------------)")
    repetidos = False
    counter1 = 0
    while counter1 < len(params):
        counter2 = counter1+1
        while 0 < len(params[counter2:]):
            if params[counter1] == params[counter2:][0]:
                repetidos == True
                print(params[counter1])
                print(params[counter2:][0])
                break
            print(counter2)
            counter2 += 1
        counter1 += 1
    if repetidos == True:
        return "error"
    print("(-----------------------------------------)")

def getArgs(messageIn):
    list = messageIn.content.split(' ')
    del list[0]
    for element in list:
        print(element)

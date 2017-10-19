def getArgs(messageIn):
    list = messageIn.content.split(' ')
    del list[0]
    return list

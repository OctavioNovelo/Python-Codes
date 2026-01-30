def linealSearch(data, element):
    for i in range(len(data)):
        if element == data[i]:
            return i
    
    return -1
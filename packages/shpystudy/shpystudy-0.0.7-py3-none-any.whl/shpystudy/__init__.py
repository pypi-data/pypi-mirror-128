import shpystudy
name = "shpystudy"

def changenum(num,change):
    if change == '10-2':
        finalnum = bin(num)
    elif change == '2-10':
        finalnum = int(num,2)
    elif change == '10-16':
        finalnum = hex(num)
    elif change == '16-10':
        finalnum = int(num,16)
    elif change == '2-16':
        finalnum = hex(int(num,2))
    elif change == '16-2':
        finalnum = bin(int(num,16))
    return finalnum
import pd_pystudy
name = "pd_pystudy"

def changenum(num,change):
    try:
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
    except:
        return 'ERROR'

def delete_list_allcontent(content,list):
    try:
        while content in list:
            list.remove(content)
        return list
    except:
        return 'ERROR'

def check_list_content(content,list):
    try:
        if content in list:
            return True
        else:
            return False
    except:
        return False
import datetime

def timestamp_convertor(date):
    try:
        return int(datetime.datetime.strptime(date, "%Y-%m-%d").timestamp()*1000)
    except:
        return ''

def timestamp_convertor2(date):
    try:
        return int(datetime.datetime.strptime(date, "%d/%m/%Y").timestamp()*1000)
    except:
        return ''


import datetime

def timestamp_convertor(date):

    return datetime.datetime.strptime(date, "%d/%m/%Y").timestamp()*1000


def timestamp_convertor2(date):

    return datetime.datetime.strptime(date, "%Y-%m-%d").timestamp()*1000


from datetime import datetime

def month_to_date(month_str):
    return datetime.strptime(month_str.strip()+'-01', "%Y-%m-%d").date()


def month_to_str(month):
    return month.strftime("%Y-%m")

def week_of_month(date_value):
    return date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1] + 1

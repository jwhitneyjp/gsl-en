'''
  Handy date functions
'''

## Cookbook code from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/476197

from datetime import date, timedelta

def daynames(weekday):
    first_day = dateDelta( date.today() ).get_first_day()
    first_weekday = first_day.weekday()
    offset = 7 - first_weekday + weekday
    daynames = []
    for pos in range(0,7,1):
        d = date( first_day.year, first_day.month, 1 + offset + pos)
        daynames.append( d.strftime('%A') )
    return daynames

class dateDelta:
    def __init__(self,dt):
        self.dt = dt

    def get_first_day(self, d_years=0, d_months=0):
        # d_years, d_months are "deltas" to apply to dt
        y, m = self.dt.year + d_years, self.dt.month + d_months
        a, m = divmod(m-1, 12)
        return date(y+a, m+1, 1)

    def get_last_day(self):
        return self.get_first_day(0, 1) + timedelta(-1)

    def get_last_month(self):
        y, m = self.dt.year, self.dt.month
        a, m = divmod(m-2, 12)
        return date(y+a, m+1, 1)

    def get_next_month(self):
        y, m = self.dt.year, self.dt.month
        a, m = divmod(m, 12)
        return date(y+a, m+1, 1)

def date_tuple(dt):
    return (dt.year, dt.month, dt.day)


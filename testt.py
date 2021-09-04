from datetime import date, timedelta

t1 = timedelta(7)
t2 = date.today()
t3 = date.today() + t1

print(t3.weekday())
print(t2.weekday())
# timekeepr
import os, sys, time, datetime

months = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sept', 'oct', 'nov', 'dec')
def intMonth(m):
    m = m.lower()
    for mo in months:
        if m.find(mo) == 0:
            return months.index(mo)

day0 = datetime.date(2010,1,1).toordinal()

cmd = "git log > temp.log"
os.system(cmd)

f = open("temp.log")
lines = f.readlines()

days = {}

for i in range(len(lines)):
    if lines[i][:6] == "commit":
        commit = lines[i].split()[1]
        dateline = lines[i+2].split()
        yr = int(dateline[5])
        mo = intMonth(dateline[2])
        date = int(dateline[3])
        tim = dateline[4].split(":")
        hr = int(tim[0])
        mn = int(tim[1])
        sec = int(tim[2])
        comment = lines[i+4].strip()
        day = datetime.date(yr, mo+1, date+1).toordinal() - day0
        hour = hr + mn/60.0 + sec/3600.0
        print commit, day, hour, yr, months[mo], date, hr, mn, sec, comment
        

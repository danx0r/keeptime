# timekeepr
import os, sys, time, datetime

months = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sept', 'oct', 'nov', 'dec')
def intMonth(m):
    m = m.lower()
    for mo in months:
        if m.find(mo) == 0:
            return months.index(mo)

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
        print commit, yr, months[mo], date, hr, mn, sec, comment
        

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
        print commit, yr, months[mo], date, hr, mn, sec, comment

        #convert into day + hour since 2010
        day = datetime.date(yr, mo+1, date+1).toordinal() - day0
        hour = hr + mn/60.0 + sec/3600.0

        #move it all back 6 hours (work cycle from 6am - 6am)
        hour -= 6
        if hour < 0:
            hour += 24
            day -= 1

        if day not in days:
            days[day] = {
                'hist':[0 for i in range(24)],
                'commits':[],
                'comments':[]
                }
        days[day]['commits'].append(commit)
        days[day]['comments'].append(comment)
        hist = days[day]['hist']
        ihr = int(hour)
        hist[ihr] += 1

print "----------------------------------------------------------------------"
keys = days.keys()
keys.sort()
for i in keys:
    day = days[i]
    h = ""
    for j in day['hist']:
        if j:
            h += "%3d" % j
        else:
            h += "   "
    print h, day['comments']

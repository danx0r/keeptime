# timekeepr
import os, sys, time, datetime

months = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec')
def intMonth(m):
    m = m.lower()
    for mo in months:
        if m.find(mo) == 0:
            return months.index(mo)

def agglomCom(c):
    c = ""
    for j in range(len(day['comments'])-1, -1, -1):
        c += day['comments'][j][:35] + "; "
    c = c[:-1]
    return c

##def agglomCom(c):
##    words = {}
##    for com in c:
##        for w in com.split():
##            w = w.replace(".", "")
##            w = w.replace(",", "")
##            w = w.replace(":", "")
##            w = w.replace(";", "")
##            w = w.replace("(", "")
##            w = w.replace(")", "")
##            w = w.strip()
##            if w in words:
##                words[w] += 1
##            else:
##                words[w] = 1
##    return str(words)

day0 = datetime.date(2010,1,1).toordinal()

cmd = "git log -g | grep -v Reflog > temp.log"
os.system(cmd)

f = open("temp.log")
lines = f.readlines()

days = {}

for i in range(len(lines)):
    if lines[i][:6] == "commit":
        commit = lines[i].split()[1]
        for j in range(1,5):
            if lines[i+j][:5] == "Date:":
                break
        dateline = lines[i+j].split()
        yr = int(dateline[5])
        mo = intMonth(dateline[2])
        date = int(dateline[3])-1
        tim = dateline[4].split(":")
        hr = int(tim[0])
        mn = int(tim[1])
        sec = int(tim[2])
        comment = lines[i+j+2].strip()
##        print commit, yr, months[mo], date, hr, mn, sec, comment

        #convert into day + hour since 2010
        day = datetime.date(yr, mo+1, date+1).toordinal() - day0
        hour = hr + mn/60.0 + sec/3600.0

        #move it all back 6 hours (work cycle from 6am - 6am)
        hour -= 6
        if hour < 0:
            hour += 24
            day -= 1

        date = datetime.date.fromordinal(day0+day)

        if day not in days:
            days[day] = {
                'hist':[0 for i in range(24)],
                'date': date,
                'commits':[],
                'comments':[]
                }
        days[day]['commits'].append(commit)
        days[day]['comments'].append(comment)
        hist = days[day]['hist']
        ihr = int(hour)
        hist[ihr] += 1

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
    c = agglomCom(day['comments'])
    d = "%10s" % day['date']
    print d, h, c[-144:-1]

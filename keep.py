# timekeepr
import os, sys, time, datetime
COMMENTS = True

months = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec')
def intMonth(m):
    m = m.lower()
    for mo in months:
        if m.find(mo) == 0:
            return months.index(mo)

def agglomCom(c):
    c = ""
    for j in range(len(day['comments'])-1, -1, -1):
        c += day['comments'][j][:33] + "|"
    c = c[:-1]
    return c

roots = ['.']
for arg in sys.argv[1:]:
    if arg == "-nocomments":
        COMMENTS = False
    else:
        roots.append(arg)

print "projects to track:", roots
for i in range(len(roots)):
    roots[i] = os.path.abspath(roots[i])

day0 = datetime.date(2010,1,1).toordinal()

home = roots[0] + "/"
temp = home + "__keep_temp_.log"
temp2 = home + "__keep_temp2_.log"
print "temp:", temp
print "temp2:", temp2

#make sure temp_keep.log exists but is empty
f = open(temp, "w")
f.close()

for root in roots:
    os.chdir(root)
    branches = []
    cmd = "git branch > %s" % temp2
    os.system(cmd)
    f = open(temp2)
    lines = f.readlines()
    for line in lines:
        line = line.replace("*","").strip()
        branches.append(line)
    f.close()
    print "branches:", branches

    #list of all commits
    for branch in branches:
        if branch == "master":
            cmd = "git log >> " + temp
        else:
            cmd = "git log HEAD..%s >> %s" % (branch, temp)
        print cmd
        os.system(cmd)

f = open(temp)
lines = f.readlines()

days = {}
duplicates = set()

for i in range(len(lines)):
    if lines[i][:6] == "commit":
        commit = lines[i].split()[1]
        for j in range(1,5):
            if lines[i+j][:7] == "Author:":
                w = lines[i+j].split()
                author = w[1]
            if lines[i+j][:5] == "Date:":
                break
        if author.lower() not in ("dan", "danx0r", "dbm"):
            continue
        dateline = lines[i+j].split()
        zone = int(dateline[-1][:-2])
        yr = int(dateline[5])
        mo = intMonth(dateline[2])
        date = int(dateline[3])-1
        tim = dateline[4].split(":")
        hr = int(tim[0])
        mn = int(tim[1])
        sec = int(tim[2])
        comment = lines[i+j+2].strip()
        key = str(dateline) + "|" + comment
        if key in duplicates:
            continue
        duplicates.add(key)
##        print commit, yr, months[mo], date, hr, mn, sec, comment

        #convert into day + hour since 2010
        day = datetime.date(yr, mo+1, date+1).toordinal() - day0
        hour = hr + mn/60.0 + sec/3600.0

        #adjust for time zone (assume CA ftw!)
        hour -= zone + 8

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
total = 0
for i in keys:
    day = days[i]
    h = ""
    for j in day['hist']:
        if j:
            h += "%3d" % j
            total += 1
        else:
            h += "   "
    c = agglomCom(day['comments'])
    d = "%10s" % day['date']
    print d, h, c[-144:] if COMMENTS else ""

print "total hours with checkins:", total
os.system("rm %s %s" % (temp, temp2))

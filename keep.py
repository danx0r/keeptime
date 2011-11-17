# timekeepr
import os, sys, time, datetime

cmd = "git log > temp.log"
os.system(cmd)

f = open("temp.log")
lines = f.readlines()

days = {}

for i in range(len(lines)):
    if lines[i][:6] == "commit":
        commit = lines[i].split()[1]
        dateline = lines[i+2].split()
        yr = dateline[5]
        mo = dateline[2]
        date = dateline[3]
        tim = dateline[4].split(":")
        hr = tim[0]
        mn = tim[1]
        sec = tim[2]
        
        comment = lines[i+4].strip()
        print commit, yr, mo, date, hr, mn, sec, comment
        

import ekg
import urllib
import time
import datetime

homeDir = "~"

prevUptime = homeDir + "/status/prevUptime"
lastStat = homeDir + "/status/lastStatus"
ggStatLog = homeDir + "/status/gg.log"
ircStatLog = homeDir + "/status/irc.log"

topfile = homeDir + "/status/topsum.db"
#topqfile = homeDir + "/status/topq.db"
toponfile = homeDir + "/status/topup.db"

parserHg = "http://188.165.227.93/parser.irc"

onlineGGStat = "HellGround.pl | Online | Players: %i (max: %i) | Uptime: %s | Rev: %i | Diff: %i (avg: %i)"
#                "HellGround.pl | Online | Players: %i (max: %i) | Uptime: %s | Queue: %i (max: %i) | Revision: %i"
offlineGGStat = "HellGround.pl | HellGround is Offline "

onlineIRCStat = "Hellground is ONLINE with %i (top: %i) players, %i ingame (Horde: %i Ally: %i). Uptime: %s (top: %s). Revision:#%i"
offlineIRCStat = "HellGround is Offline "

maintenanceStat = "(probably daily maintenance in progress) | should be online ~ 5:30"

def statusgg():
    error = 0
    try:
        plik = urllib.urlopen(parserHg).read()
    except:
        error = 1

    tmpFile = open(lastStat, "rb")
    lastStatus = str(tmpFile.read())
    tmpFile.close()

    if error != 1:
        dane = str(plik);
        dane = dane.split(" ")

        if unicode(dane[0]).isnumeric():
            stfile = open(prevUptime, "rb")
            prevUp = int(stfile.read())
            stfile.close()

            online = int(dane[1])
            maxOnline = int(dane[2])
            up = int(dane[0])
#            maxKolejka = int(dane[4])
            rev = int(dane[6])
#            kolejka = int(dane[3])
            curDiff = int(dane[7])
            avgDiff = int(dane[8])

            tmp = up/60
            mm = tmp%60
            hh = tmp/60
            ss = up%60

            uptime = "%ih %im %is" % (hh, mm, ss)

            stfile = open(prevUptime, "w")
            stfile.write(str(up))
            stfile.close()

            tmpFile = open(topfile, "rb")
            topOn = int(tmpFile.read())
            tmpFile.close()

#           tmpFile = open(topqfile, "rb")
#           topQ = int(tmpFile.read())
#           tmpFile.close()

            tmpFile = open(toponfile, "rb")
            topUp = int(tmpFile.read())
            tmpFile.close()

            if topOn < maxOnline:
                tmpFile = open(topfile, "w")
                tmpFile.write(str(maxOnline))
                tmpFile.close()

#           if topQ < maxKolejka:
#                tmpFile = open(topqfile, "w")
#                tmpFile.write(str(maxKolejka))
#                tmpFile.close()

            if topUp < up:
                tmpFile = open(toponfile, "w")
                tmpFile.write(str(up))
                tmpFile.close()

            if online == 0 and up == 0:
                struct = time.localtime()
                if struct[3] >= 4 and struct[3] < 5:
                    status = offlineGGStat + maintenanceStat
                else:
                    status = offlineGGStat + "(or just DC)"
            elif prevUp == up:
                status = offlineGGStat + "(maybe freeze)"
            else:
                status = onlineGGStat % (online, maxOnline, uptime, rev, curDiff, avgDiff)
        else:
            status = offlineGGStat

        now = datetime.datetime.now()
        tmpFile = open(ggStatLog, "a")
        tmpFile.write("%s - %s\n" % (now.strftime("%Y-%m-%d %H:%M"), str(status)))
        tmpFile.close()

        #ekg.printf("generic", lastStatus)

        if lastStatus != status:
            tmpFile = open(lastStat, "w")
            tmpFile.write(str(status))
            tmpFile.close()
            ekg.command("session -w status")
            ekg.command("gg:away " + status)

        #ekg.command("gg:away " + status)

def statusirc():
    error = 0
    try:
        plik = urllib.urlopen(parserHg).read()
    except:
        error = 1

    if error != 1:
        dane = str(plik)
        dane = dane.split(" ")

        if unicode(dane[0]).isnumeric() and error != 1:
            online = int(dane[1])
            maxOnline = int(dane[2])
#            maxKolejka = int(dane[4])
            rev = int(dane[6])
#            kolejka = int(dane[3])

            suma = int(0)
            horda = int(0)
            ally = int(0)
            up = int(dane[0])

            tmpFile = open(topfile, "rb")
            top = int(tmpFile.read())
            tmpFile.close()

#            tmpFile = open(topqfile, "rb")
#            topq = int(tmpFile.read())
#            tmpFile.close()

            tmpFile = open(toponfile, "rb")
            topon = int(tmpFile.read())
            tmpFile.close()

            tmp = up/60
            mm = tmp%60
            hh = tmp/60
            ss = up%60

            uptime = "%ih %im %is" % (hh, mm, ss)

            tmp = topon/60
            mm = tmp%60
            hh = tmp/60
            ss = topon%60

            topUptime = "%ih %im %is" % (hh, mm, ss)

            if (online == 0 and up == 0) or online == afk:
                struct = time.localtime()
                if struct[3] >= 5 and struct[3] < 6:
                    status = offlineIRCStat + maintenanceStat
                else:
                    status = offlineIRCStat + "(or just DC)"
            else:
                status = onlineIRCStat % (online, top, suma, horda, ally, uptime, topUptime, rev)
        else:
            status = "Hellground or GameFreedom is OFFLINE"

        now = datetime.datetime.now()

        tmpFile = open(ircStatLog, "a")
        tmpFile.write("%s - %s\n" % (now.strftime("%Y-%m-%d %H:%M"), str(status)))
        tmpFile.close()

        ekg.command("session -w HellGround")
        ekg.command("irc:notice #gamefreedom " + status)
#        if status2 != "":
#            ekg.command("irc:notice #gamefreedom " + status2)  

ekg.timer_bind(90, statusgg)
ekg.timer_bind(1800, statusirc)

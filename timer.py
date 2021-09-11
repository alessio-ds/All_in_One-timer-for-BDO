import time
import requests
import os
import sys
sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=6, cols=42))
def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def selectserver():
    try:
        with open('preferred_server.txt', mode='r') as f:
            check = f.read()
            gather(check)
    except:
        server=input('Which server are you on?\n1 - EU\n2 - NA\n3 - KR\n4 - SEA\n5 - RU\n\n')
        if server=='1':
            server='eu'
        elif server=='2':
            server='na'
        elif server=='3':
            server='kr'
        elif server=='4':
            server='sea'
        elif server=='5':
            server='ru'

        with open('preferred_server.txt', mode='w') as f:
            f.write(server)
        gather(server)

def gather(server):
    try:
        sito = requests.get('https://mmotimer.com/bdo/?server='+server)
    except:
        print('Site is down now.')
    testopagina = sito.text

    nomiboss = 'Nouver', 'Karanda', 'Kzarka', 'Offin', 'Vell', 'Garmoth', 'Quint', 'Muraka', 'Kutum'

    postrading = testopagina.find('Imperial trading reset in:')
    trading = testopagina[postrading + 52:postrading + 60]

    prossimo = testopagina.find('Next boss')
    seguitoda = testopagina.find('Followed by')
    trovabosstxt = testopagina[prossimo:seguitoda]

    nomeboss2=''
    occorrenze = 0
    for x in nomiboss:
        occorrenze = occorrenze + trovabosstxt.count(x)

    if occorrenze == 2:
        posboss = 0
        while posboss == 0:
            for b in nomiboss:
                posboss = trovabosstxt.find(b)
                if posboss == -1:
                    posboss = 0
                else:
                    break

        nomeboss = trovabosstxt[posboss:posboss + 7]
        nomeboss = nomeboss.replace('<', '')
        nomeboss = nomeboss.replace('/', '')
        if nomeboss[:5] == 'Kutum':
            nomeboss = 'Kutum'
        postboss = trovabosstxt.find('timer countdown">')
        tboss = trovabosstxt[postboss + 39:postboss + 47]
        tboss = list(tboss)
    else:
        posboss = 0
        while posboss == 0:
            for b in nomiboss:
                posboss = trovabosstxt.find(b)
                if posboss == -1:
                    posboss = 0
                else:
                    break

        nomeboss = trovabosstxt[posboss:posboss + 7]
        nomeboss = nomeboss.replace('<', '')
        nomeboss = nomeboss.replace('/', '')
        if nomeboss[:5] == 'Kutum':
            nomeboss = 'Kutum'

        postboss = trovabosstxt.find('timer countdown">')
        tboss = trovabosstxt[postboss + 39:postboss + 47]

        secondo = trovabosstxt[postboss:]
        posboss2 = 0
        while posboss2 == 0:
            for b in nomiboss:
                posboss2 = secondo.find(b)
                if posboss2 == -1:
                    posboss2 = 0
                else:
                    break

        nomeboss2 = secondo[posboss2:posboss2 + 7]
        nomeboss2 = nomeboss2.replace('<', '')
        nomeboss2 = nomeboss2.replace('/', '')
        if nomeboss2[:5] == 'Kutum':
            nomeboss2 = 'Kutum'

    hi = hb = int(tboss[1])
    mi = mb = int(str((tboss[3]) + (tboss[4])))
    si = sb = int(str((tboss[6]) + (tboss[7])))

    hba = ht = int(trading[1])
    mba = mt = int(str((trading[3]) + (trading[4])))
    sba = st = int(str((trading[6]) + (trading[7])))

    dnpos = testopagina.find('Night in:')  #dnpos = day night position
    if dnpos!=-1:
        orario = testopagina[dnpos + 42:dnpos + 50]
        ho = int(orario[1])
        mo = int(str((orario[3]) + (orario[4])))
        so = int(str((orario[6]) + (orario[7])))
        gn='Night in: '
        countdown(hb,mb,sb, ho,mo,so, hi,mi,si, ht,mt,st, hba,mba,sba, gn, nomeboss, nomeboss2, server)
        gather()

    else:
        dnpos = testopagina.find('Day in:')
        orario = testopagina[dnpos + 40:dnpos + 48]
        ho = int(orario[1])
        mo = int(str((orario[3]) + (orario[4])))
        so = int(str((orario[6]) + (orario[7])))
        gn='Day in: '
        countdown(hb,mb,sb, ho,mo,so, hi,mi,si, ht,mt,st, hba,mba,sba, gn, nomeboss, nomeboss2, server)
        gather()

def hmsToSecs(h,m,s):
    return h*3600 + m*60 + s

def secsToHms(secs):
    hours = secs//3600
    secs -= hours*3600
    mins = secs//60
    secs -= mins*60
    return hours,mins,secs

def countdown(hb,mb,sb, ho,mo,so, hi,mi,si, ht,mt,st, hba,mba,sba, gn, nomeboss, nomeboss2, server):
    autoreset=120
    bseconds = hmsToSecs(hb,mb,sb)
    oseconds = hmsToSecs(ho, mo, so)
    iseconds = hmsToSecs(hi,mi,si)
    tseconds = hmsToSecs(ht, mt, st)
    baseconds = hmsToSecs(hba, mba, sba)
    while bseconds > 0 and oseconds > 0 and iseconds > 0 and tseconds > 0 and baseconds >0 and autoreset > 0:
        clr()
        if nomeboss2!='':
            print("Next boss: ",nomeboss,'&',nomeboss2,'\t',("%02d:%02d:%02d"%secsToHms(bseconds)))
        else:
            print("Next boss: ", nomeboss, '\t\t', ("%02d:%02d:%02d" % secsToHms(bseconds)))

        if gn=='Day in: ':
            print(gn,'  \t\t\t',("%02d:%02d:%02d" % secsToHms(oseconds)))
        else:
            print(gn, '\t\t\t', ("%02d:%02d:%02d" % secsToHms(oseconds)))
        print("Imperial reset in: \t\t",("%02d:%02d:%02d" % secsToHms(iseconds)))
        print("Imperial trading reset in: \t",("%02d:%02d:%02d" % secsToHms(baseconds)))
        print("Bartering reset in: \t\t",("%02d:%02d:%02d" % secsToHms(baseconds)))

        bseconds, oseconds, iseconds, tseconds, baseconds, autoreset = bseconds-1, oseconds-1, iseconds-1, tseconds-1, baseconds-1, autoreset-1
        
        time.sleep(1)
    gather(server)


selectserver()

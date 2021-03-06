import os, sys
import urllib2
import traceback
import argparse
from time import sleep,time
import json
from pokemons import pokemonlist
import httplib
import re
import requests
import subprocess
import wincolors
import datetime

__author__ = 'hypertoken'
__version__ = '0.1.6'
__git__ ='https://github.com/hypertoken/PokeVisionFinder'
__thanks__ ='Encode, and everyone at Github, Discord and Ownedcore!'

_nt = False
if os.name is "nt":
    _nt = True

_cities = []

_pokemons = []

_pokemonslisted = []

ps_use = []

_session =requests.Session()
_sessionid = ""

frozen = getattr(sys, 'frozen', '')

if not frozen:
    # not frozen: in regular python interpreter
    _scriptpath = os.path.abspath(os.path.dirname(__file__))

elif frozen:
    # py2exe:
    _scriptpath = os.path.abspath(os.path.dirname(sys.executable))

ps_dir = os.path.join(_scriptpath,"Sniper")
ps_path = os.path.join(ps_dir,"PokeSniper2.exe")

#ErrorLogger
def _logError(error):
    os.chdir(_scriptpath)
    with open("errors.log", "a+") as f:
        f.write(error + "\n")
        f.close()

#JsonData
def _jsondata(url):
    if _nt and _colors:
        wincolors.paint(wincolors.colors.ERROR)
    try:
        _rawdata = urllib2.urlopen(url)
        return json.load(_rawdata)
    except urllib2.HTTPError, e:
        if _verbose == 1:
            print '[ERROR] HTTPError'
        elif _verbose == 2:
            print '[ERROR] HTTPError = ' + str(e)
        _logError(str(e))
        return url
    except urllib2.URLError, e:
        if _verbose == 1:
            print '[ERROR] URLError'
        elif _verbose == 2:
            print '[ERROR] URLError = ' + str(e)
        _logError(str(e))
        return url
    except httplib.HTTPException, e:
        if _verbose == 1:
            print '[ERROR] HTTPException'
        elif _verbose == 2:
            print '[ERROR] HTTPException = ' + str(e)
        _logError(str(e))
        return url
    except ValueError, e:
        if _verbose == 1:
            print '[ERROR] ValueError'
        elif _verbose == 2:
            print '[ERROR] ValueError = ' + str(e)
        _logError(str(e))
        return url
    except Exception:
        if _verbose == 1:
            print '[ERROR] generic exception: '
        elif _verbose == 2:
            print '[ERROR] generic exception: ' + traceback.format_exc()
        _logError(traceback.format_exc())
        return url

#JsonData Custom Headers
def _jsondatach(url):
    if _nt and _colors:
        wincolors.paint(wincolors.colors.ERROR)
    try:
        _headers = { 'User-Agent' : 'Mozilla/5.0' }
        _req = urllib2.Request(url, None,_headers)
        _rawdata = urllib2.urlopen(_req)
        return json.load(_rawdata)
    except urllib2.HTTPError, e:
        if _verbose == 1:
            print '[ERROR] HTTPError'
        elif _verbose == 2:
            print '[ERROR] HTTPError = ' + str(e)
        _logError(str(e))
        return url
    except urllib2.URLError, e:
        if _verbose == 1:
            print '[ERROR] URLError'
        elif _verbose == 2:
            print '[ERROR] URLError = ' + str(e)
        _logError(str(e))
        return url
    except httplib.HTTPException, e:
        if _verbose == 1:
            print '[ERROR] HTTPException'
        elif _verbose == 2:
            print '[ERROR] HTTPException = ' + str(e)
        _logError(str(e))
        return url
    except ValueError, e:
        if _verbose == 1:
            print '[ERROR] ValueError'
        elif _verbose == 2:
            print '[ERROR] ValueError = ' + str(e)
        _logError(str(e))
        return url
    except Exception:
        if _verbose == 1:
            print '[ERROR] generic exception: '
        elif _verbose == 2:
            print '[ERROR] generic exception: ' + traceback.format_exc()
        _logError(traceback.format_exc())
        return url

def _jsondatachTrack(url):
    if _nt and _colors:
        wincolors.paint(wincolors.colors.ERROR)
    try:
        global sessionid
        if sessionid == "":
            return _jsondatachTrack(url)
        else:
            _rawdata = _session.get(url+sessionid, stream=True)
            return _rawdata.json()
    except urllib2.HTTPError, e:
        if _verbose == 1:
            print '[ERROR] HTTPError'
        elif _verbose == 2:
            print '[ERROR] HTTPError = ' + str(e)
        _logError(str(e))
        return url
    except urllib2.URLError, e:
        if _verbose == 1:
            print '[ERROR] URLError'
        elif _verbose == 2:
            print '[ERROR] URLError = ' + str(e)
        _logError(str(e))
        return url
    except httplib.HTTPException, e:
        if _verbose == 1:
            print '[ERROR] HTTPException'
        elif _verbose == 2:
            print '[ERROR] HTTPException = ' + str(e)
        _logError(str(e))
        return url
    except ValueError, e:
        if _verbose == 1:
            print '[ERROR] ValueError'
        elif _verbose == 2:
            print '[ERROR] ValueError = ' + str(e)
        _logError(str(e))
        return url
    except Exception:
        if _verbose == 1:
            print '[ERROR] generic exception: '
        elif _verbose == 2:
            print '[ERROR] generic exception: ' + traceback.format_exc()
        _logError(traceback.format_exc())
        return url

#Find TrackMon Session
def _findSessionIdTrack():
    global sessionid
    if _nt and _colors:
        wincolors.paint(wincolors.colors.INFO)
    print "[INFO] Finding SessionId for TrackMon"
    rw = re.compile('var sessionId \= \'(.*?)\'\;')
    r = _session.get("http://www.trackemon.com/")
    for line in r.iter_lines():
        if "sessionId" in line:
            suc = rw.search(line)
            if suc:
                sessionid = suc.group(1)
                if _nt and _colors:
                    wincolors.paint(wincolors.colors.SUCCESS)
                print "[INFO] SessionId for TrackMon Found"
            else:
                _findSessionIdTrack()

#Pokemon Name
def _pokename(id):
    return pokemonlist[int(id)-1]

#PokeSplit
def _pokesplit(pokemons):
    global _pokemons
    _pokemons = pokemons.split(",")

#POkePrinter
def _printer(name,lat,lng,exp,src):
    _remain = float(exp)-time()
    _minutes = int(_remain / 60)
    _seconds = int(_remain % 60)
    _expire = str(_minutes) + " Minutes, " + str(_seconds) + " Seconds"
    if _nt and _colors:
        wincolors.paint(wincolors.colors.SUCCESS)
    print "-------------------------------------------------"
    print "Pokemon: " + name
    print "Coordinates: " + str(lat) + "," + str(lng)
    print "Expires in: " + _expire
    print "Source: " + src
    print "-------------------------------------------------"
    if _logging:
        _logPokemon(name, str(lat), str(lng), _expire)

# Cleanup function for logfile
def _logCleanup():
    os.chdir(_scriptpath)
    with open("pokemons.log", "r") as f:
        timestrings = f.readlines()
        f.close()
    with open("pokemons.log", "w") as f:
        for timestring in timestrings:
            expireindex = timestring.find("Expires in:")
            expiretime = timestring[expireindex+len("Expires in: ["):timestring.find("[Timestamp")-2]
            expireminindex = expiretime.find("Minutes")
            expireminutes = expiretime[:expireminindex-1]
            expiresecindex = expiretime.find("Seconds")
            expireseconds = expiretime[expireminindex+len("Minutes, "):expiresecindex-1]
            expireinseconds = (int(expireminutes) * 60) + int(expireseconds)
            oldtimeindex = timestring.find("Timestamp: ")
            oldtimeindex = oldtimeindex + len("Timestamp: ")
            oldtime = timestring[oldtimeindex:]
            oldtimeindex = oldtime.find("]")
            oldtime = oldtime[:oldtimeindex]
            oldtime = datetime.datetime.strptime(oldtime, '%Y-%m-%d %H:%M:%S')
            xpiretime = oldtime + datetime.timedelta(seconds = expireinseconds)
            nowtime = datetime.datetime.now()
            timeleft = xpiretime - nowtime
            expired = datetime.timedelta(seconds=45)
            if timeleft >= expired:
                f.write(timestring)
        f.close()
        
#Logger
def _logPokemon(name, lat, lng, expire):
    os.chdir(_scriptpath)
    with open("pokemons.log", "a+") as f:
        f.write("[" + name + "] [" + lat + "," + lng + "] Expires in: [" + expire + "] [" +'Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) +"]\n")
        f.close() 
        _logCleanup()

#CoordsLoader
def _populateCities():
    os.chdir(_scriptpath)
    with open("coords.txt", "a+") as f:
        _data = f.readlines()
        for line in _data:
            _citydata = line.split(":")
            _cities.append([_citydata[0],_citydata[1],_citydata[2]])
        f.close()

#Finder
def _finderTrackemon(city):
    if _nt and _colors:
        wincolors.paint(wincolors.colors.INFO)
    print "[INFO] Looking for pokemons in: " + city[0]
    _latitudesw = float(city[1]) - (0.05 * _zoomFactor)
    _longitudesw = float(city[2]) - (0.05 * _zoomFactor)
    _latitudene = float(city[1]) + (0.05 * _zoomFactor)
    _longitudene = float(city[2]) + (0.05 * _zoomFactor)

    _scanurl = "http://www.trackemon.com/fetch?location="+str(city[1])+","+str(city[2])+"&sessionId="
    _scanurljsondata = _jsondatachTrack(_scanurl)

    for pokename in _pokemons:
        try:
            for pokemon in _scanurljsondata['pokemon']:
                _id = pokemon['pokedexTypeId']
                _name = _pokename(_id)
                if _name.lower() in pokename.lower():
                    _lat = pokemon['latitude']
                    _lng = pokemon['longitude']
                    _exp = pokemon['expirationTime']
                    _id = pokemon['id']
                    _expired = int((float(_exp)-time())/60)
                    if  _expired < 0:
                        if _nt and _colors:
                            wincolors.paint(wincolors.colors.WARNING)
                        print "[INFO] Pokemon already expired."                        
                    elif _id not in _pokemonslisted:
                        _pokemonslisted.append(_id)
                        _printer(_name, _lat, _lng, _exp)
                        if ps_use: _pokeSniper(_name, str(_lat), str(_lng))
                    else:
                        if _nt and _colors:
                            wincolors.paint(wincolors.colors.WARNING)
                        print "[INFO] This "+_name+" already found."
        except KeyError, e:
            if _nt and _colors:
                wincolors.paint(wincolors.colors.ERROR)
            if _verbose == 1:
                print '[ERROR] KeyError'
            elif _verbose == 2:
                import traceback
                print '[ERROR] KeyError = ' + str(e)
            _logError(str(e))
        except IndexError, e:
            if _nt and _colors:
                wincolors.paint(wincolors.colors.ERROR)
            if _verbose == 1:
                print '[ERROR] IndexError'
            elif _verbose == 2:
                print '[ERROR] IndexError = ' + str(e)
            _logError(str(e))
        except TypeError, e:
            if _verbose == 1:
                print '[ERROR] TypeError'
            elif _verbose == 2:
                print '[ERROR] TypeError= ' + str(e)
            _logError(str(e))

#Finder
def _finderSkipLagged(city):
    if _nt and _colors:
        wincolors.paint(wincolors.colors.INFO)
    print "[INFO] Looking for pokemons in: " + city[0]
    _latitudesw = float(city[1]) - (0.05 * _zoomFactor)
    _longitudesw = float(city[2]) - (0.05 * _zoomFactor)
    _latitudene = float(city[1]) + (0.05 * _zoomFactor)
    _longitudene = float(city[2]) + (0.05 * _zoomFactor)

    _scanurl = "http://skiplagged.com/api/pokemon.php?bounds="+str(_latitudesw)+","+str(_longitudesw)+\
               ","+str(_latitudene)+","+str(_longitudene)
    _scanurljsondata = _jsondatach(_scanurl)

    for pokename in _pokemons:
        try:
            for pokemon in _scanurljsondata['pokemons']:
                _id = pokemon['pokemon_id']
                _name = _pokename(_id)
                if _name.lower() in pokename.lower():
                    _lat = pokemon['latitude']
                    _lng = pokemon['longitude']
                    _exp = pokemon['expires']
                    _combo = _name+str(_lat)+str(_lng)
                    _expired = int((float(_exp)-time())/60)
                    if  _expired < 0:
                        if _nt and _colors:
                            wincolors.paint(wincolors.colors.WARNING)
                        print "[INFO] Pokemon already expired."                              
                    elif _id not in _pokemonslisted:
                        _pokemonslisted.append(_combo)
                        _printer(_name, _lat, _lng, _exp, "Skiplagged")
                        if ps_use: _pokeSniper(_name, str(_lat), str(_lng))
                    else:
                        if _nt and _colors:
                            wincolors.paint(wincolors.colors.WARNING)
                        print "[INFO] This "+_name+" already found."
        except KeyError, e:
            if _nt and _colors:
                wincolors.paint(wincolors.colors.ERROR)
            if _verbose == 1:
                print '[ERROR] KeyError'
            elif _verbose == 2:
                import traceback
                print '[ERROR] KeyError = ' + str(e)
            _logError(str(e))
        except IndexError, e:
            if _nt and _colors:
                wincolors.paint(wincolors.colors.ERROR)
            if _verbose == 1:
                print '[ERROR] IndexError'
            elif _verbose == 2:
                print '[ERROR] IndexError = ' + str(e)
            _logError(str(e))
        except TypeError, e:
            if _verbose == 1:
                print '[ERROR] TypeError'
            elif _verbose == 2:
                print '[ERROR] TypeError= ' + str(e)
            _logError(str(e))
"""
#Finder
def _finderGo(city):
    if _nt and _colors:
        wincolors.paint(wincolors.colors.INFO)
    print "[INFO] Looking for pokemons in: " + city[0]
    _latitudesw = float(city[1]) - (0.05 * _zoomFactor)
    _longitudesw = float(city[2]) - (0.05 * _zoomFactor)
    _latitudene = float(city[1]) + (0.05 * _zoomFactor)
    _longitudene = float(city[2]) + (0.05 * _zoomFactor)

    _scanurl = "https://api-live-iix1.pokemongo.id/maps?vt="+str(_latitudesw)+","+str(_longitudesw)+\
               ","+str(_latitudene)+","+str(_longitudene)+"&u="+str(time())
    _scanurljsondata = _jsondata(_scanurl)

    for pokename in _pokemons:
        try:
            for pokemon in _scanurljsondata['pokemons']:
                _id = pokemon['pokemon_id']
                _name = _pokename(_id)
                if pokename.lower() in _name.lower():
                    _lat = pokemon['latitude']
                    _lng = pokemon['longitude']
                    _exp = pokemon['expires']
                    _printer(_name, _lat, _lng, _exp, "pokemongo.id")
        except KeyError, e:
            print '[ERROR] KeyError = ' + str(e)
        except IndexError, e:
            print '[ERROR] IndexError = ' + str(e)
"""
#Sniper
def _pokeSniper(name, lat, lng):
    if _nt and _colors:
        wincolors.paint(wincolors.colors.WARNING)
    try:
        if _terminal:
            subp = subprocess.Popen([ps_path, name, lat, lng], cwd=ps_dir, creationflags = subprocess.CREATE_NEW_CONSOLE)
            subp.wait()
        else:
            subp = subprocess.Popen([ps_path, name, lat, lng], cwd=ps_dir)
            subp.wait()
            for i in reversed(range(0, _timer)):
                sleep(1)
                if _nt and _colors:
                    wincolors.paint(wincolors.colors.TIMER)
                print "Waiting for %s seconds due to API change \r" %i,
            print "Done Waiting due to API change.                                                    "

    except OSError, e:
        error = "[WARNING] - PokeSniper2 Not found on Sniper folder"    
        if _nt and _colors:
            wincolors.paint(wincolors.colors.ERROR)
        if _verbose == 0:
            print error
        elif _verbose == 1:
            print '[ERROR] OSError'
            print error
        elif _verbose == 2:
            print '[ERROR] OSError = ' + str(e)
            print error
        _logError(str(e))
        _logError(error)
#Loop
def _loop():
    for city in _cities:
        if "Skip" in _useMode or "All" in _useMode:
            _finderSkipLagged(city)
            """elif "Track" in _useMode or "All" in _useMode:
            _finderTrackemon(city)
            elif "Go" in _useMode or "All" in _useMode:
            _finderGo(city)"""
        else:
            _finderSkipLagged(city)
            
#Init
_parser = argparse.ArgumentParser(description='PokeVisionFinder v'+__version__+' - encode')
_parser.add_argument('-m','--mode', help='Mode of work', choices=["Go","Skip", "Track","All"], default="All")
_parser.add_argument('-s', '--sniper', help='No Use sniper', action='store_false', default=True)
_parser.add_argument('-S', '--sniperterminal', help='Sniper on a different terminal', action='store_true', default=False)
_parser.add_argument('-l', '--loop', help='Run infinite', action='store_true', default=False)
_parser.add_argument('-L','--logging', help='Log pokemons found', action='store_true', default=False)
_parser.add_argument('-c','--catchfile', help='Use catch file', action='store_true', default=True)
_parser.add_argument('-C','--colors', help='No use colors', action='store_false', default=True)
_parser.add_argument('-p','--pokemons', help='List of pokemons', default="Pikachu")
_parser.add_argument('-f','--factor', help='ZoomFactor', type=int, default=1)
_parser.add_argument('-t','--timer', help='Wait Timer in seconds', type=int, default=10)
_parser.add_argument('-v','--verbose', help='Verbose mode', type=int, choices=[0, 1, 2], default=0)
_args = _parser.parse_args()

_useMode = _args.mode

ps_use = _args.sniper

_terminal = True if ps_use and _args.sniperterminal else False

_logging = _args.logging

_zoomFactor = _args.factor

_catchfile = _args.catchfile

_colors = _args.colors

_nonstop = _args.loop

_timer = _args.timer

_verbose = _args.verbose

_inputpoke = ""

if _catchfile:
    _inputpoke = [line.strip() for line in open("catch.txt", 'r')]
    _pokemons = _inputpoke
else:
    _inputpoke = _args.pokemons
    _pokesplit(_inputpoke)

if _nt and _colors:
    wincolors.paint(wincolors.colors.HEADER)
print """=====================================================================
Welcome to PokeVisionFinder """ + __version__ + """
Original Author Encode! Updated by: """ + __author__ + """
Check out our Github at: """+ __git__ + """
Special Thanks to: """+ __thanks__ + """
====================================================================="""
sleep(2)
if _nt and _colors:
    wincolors.paint(wincolors.colors.INFO)
if "Track" in _useMode or "All" in _useMode:
    _findSessionIdTrack()
_populateCities()

if _nonstop:
    while 1:
        _loop()
else:
    _loop()

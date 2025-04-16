import os
import yt_dlp
import json
from urllib.parse import urlparse
import requests
from datetime import datetime

# to do
# create json file if missing (with init)
# create urls.txt file if missing
# urls txt can manage path and (options)
# Json keys verifications
# ask to ytdlp availible format for an url
# input check
# ignore error options
# - subbtitle
# - logs file options (can be set in options), fonction --
# - verbose options -v
# - language options
# - two levels errors

current_file_path = os.path.abspath(__file__).rsplit(os.sep, 1)[0]

# Error console return
def ErrorDef(msgErr):
    errorTxt = f'[\033[31mError\033[0m] {msgErr}'
    # errorTxt = f'[Error] {msgErr}'
    return errorTxt

def ConsoleReturn(msgCR):
    ConsoleMsg = f'[Script] {msgCR}'
    return ConsoleMsg

# Exception Error
def ExcpetionReturn(msgEx, JSONScriptConfig, step):
    print(f"An error has occured while {step}")
    try:
        if JSONScriptConfig['verbose']:
            print(f"[\033[31mException Error\033[0m] {msgEx}")
            return
    except:
        return
    
# Logs function
def logs(msgLog ,JSONScriptConfig, type, level):
    if not JSONScriptConfig['logs']:
        return
    if not level: level = ''
    else: level = f'[{level}]'
    # date and syntax
    now = datetime.now()
    logSyntax = f'{now.date()} {now.time().strftime("%H:%M:%S")} [{type}] {level}'
    # Verbose mode (print logs in console if true)
    if JSONScriptConfig['verbose']: print(f'{logSyntax} {msgLog}')
    # Try to open and write logs.log
    try:
        with open('logs.log', "a", encoding='utf-8') as logFile:
            logFile.write(f'{logSyntax} {msgLog}\n')
            logFile.flush()
    except Exception as e:
        print('Unable to create or access file')
        print(e)

# Logs type function
# INFO > Informations
# WARN > Unexpected thing happened but script can still continue
# ERROR > An error has occured but script can still continue
# EXCEPTION > An exception has occured
# CRITICAL > An critical error has occured, script can't continue
def logsInfo(msgLog, level):
    logs(msgLog ,JSONScriptConfig, 'INFO', level)

def logsWarn(msgLog, level):
    logs(msgLog ,JSONScriptConfig, 'WARN', level)

def logsError(msgLog, level):
    logs(msgLog ,JSONScriptConfig, 'ERROR', level)

def logsException(msgLog, level):
    logs(msgLog ,JSONScriptConfig, 'EXCEPTION', level)

def logsCritical(msgLog, level):
    logs(msgLog ,JSONScriptConfig, 'CRITICAL', level)


def YoN(msg, F):
    while True:
        In = input(f'{msg}').strip().upper()
        if In == 'Y':
            logsInfo('User chooses Y', 'Function/UseUrlsTXT')
            if F == 'UseUrlsTXT':
                logsInfo('User chooses Y, urls.txt will be used', f'Function/YoN>{F}')
            return True
        elif In == 'N':
            logsInfo('User chooses N, urls.txt will not be used', f'Function/YoN>{F}')
            return False
        else:
            print('Type Y or N')
            logsWarn(f"User entered '{In}'", f'Function/YoN>{F}')





    

# defaultJson (if json file missing)
defaultJson = {
    "ScriptConfig": {
        "AskUrlsTxt": True,
        "_comment_AskUrlsTxt": "true = ask for using Urls.txt (default), false = don't ask",
        "DownloadPath": "",
        "_comment_DownloadPath": "set a default path here, path will not be asked (make sure to use / and not one of these \\, if empty = path asked in terminal (default)",
        "AskPath": True,
        "_comment_AskPath": "true = ask the path for the file (default), false = don't ask the path",

        "FileName": "download-ppdl",
        "_comment_FileName": "set a default file name here, please don't insert an file extension in the file name",
        "AskFileName": True,
        "_comment_AskFileName": "true = ask the name for each files (default), false = use default name for every files",

        "logs": False,
        "_comment_logs": "true = A logs.txt file will be created, return and errors will be saved, false is the default value",
        "verbose": False,
        "_comment_verbose": "true = Error and return will be more detailed, can be useful for debugging, false is the default value",

        "favoriteFileExtension": "mp4",
        "_comment_FavoriteFileExtension": "set the favorite file extension (will be used if possible)"
    },
    "ytdlpConfig": {
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
            "Referer": "https://app.pandaplay.io/",
            "Origin": "https://app.pandaplay.io",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
            "Connection": "keep-alive"
        },
        "options": {
            "format": "best",
            "merge_output_format": "mp4",
            "ignoreerrors": True,
            "ffmpeg_location": "C:/Users/deb84/Documents/Installeur/ffmpeg-2024-07-24-git-896c22ef00-full_build/bin/ffmpeg.exe"
        }
    }
}


JSONfileName = 'pandaplay-dl2.settings.json'

# Init the json file with data
def JSONinit(defaultJson, JSONfileName, msg, mode):
    failMsg = f'Impossible to write in "{JSONfileName}"'
    try:
        with open(JSONfileName, mode) as jsonFile:
            jsonFile.write(json.dumps(defaultJson, ensure_ascii=False, indent=4))
            print(ConsoleReturn(msg))
    except Exception as e:
        if failMsg:
            print(ErrorDef(failMsg))
        print(ErrorDef(e))
    return

# Load the json file
def JSONLoad(JSONfileName):
        try:
            with open(JSONfileName, 'r') as jsonFile:
                dataJSON = json.load(jsonFile)
        except Exception as e:
            dataJSON = None
            # verbose*
            print(ErrorDef(e))
        return dataJSON


# Json file import
while True:
    if os.path.isfile(os.path.join(current_file_path, JSONfileName)):
        dataJSON = JSONLoad(JSONfileName)

        if not dataJSON:
            print('6544')
            JSONinit(defaultJson, JSONfileName, f'Empty JSON file "{JSONfileName}", trying to write the file...', 'w')
            dataJSON = JSONLoad(JSONfileName)
                
        # check if the keys 'ScriptConfig' and 'ytdlpConfig' exist
        if not dataJSON['ScriptConfig'] or not dataJSON['ytdlpConfig']:
            JSONinit(defaultJson, JSONfileName, f'Incorrect JSON file content "{JSONfileName}", trying to rewrite the file...', 'w')
            dataJSON = JSONLoad(JSONfileName)

        JSONScriptConfig = dataJSON['ScriptConfig']
        JSONYtdlpConfig = dataJSON['ytdlpConfig']

        # Check for each keys from 'ScriptConfig' and 'ytdlpConfig' if they exist
        # Ignore the comments from the json file
        # If a key is incorrect, user can chooses to reset the json file
        for keys in defaultJson['ScriptConfig']:
            if not keys[0] == '_':
                if keys not in JSONScriptConfig:
                    logsError(f'The key "{keys}" is missing in {JSONfileName}', 'Json Importation')
                    if YoN(f'An error has occured in the JSON settings file {JSONfileName}, do you want to reset this file ? (Y/N)', 'Json Importation'): 
                        JSONinit(defaultJson, JSONfileName, 'Json file has been reset with success', 'w')
                        logsInfo(f'{JSONfileName} has been reset with success', 'Json Importation')
                else:
                    logsInfo(f"JSONScriptConfig['{keys}'] correctly imported from {JSONfileName}", 'Json Importation')

        for keys in defaultJson['ytdlpConfig']:
            if not keys[0] == '_':
                if keys not in JSONYtdlpConfig:
                    logsError(f'The key "{keys}" is missing in {JSONfileName}', 'Json Importation')
                    if YoN(f'An error has occured in the JSON settings file {JSONfileName} (key: {keys} is missing), do you want to reset this file ? (Y/N)', 'Json Importation'): 
                        JSONinit(defaultJson, JSONfileName, 'Json file has been reset with success', 'w')
                        logsInfo(f'{JSONfileName} has been reset with success', 'Json Importation')
                else:
                    logsInfo(f"JSONYtdlpConfig['{keys}'] correctly imported from {JSONfileName}", 'Json Importation')

        break
    else :
        try:
            msg = f'JSON file {JSONfileName} is missing, file created the file at "{current_file_path}"'
            JSONinit(defaultJson, JSONfileName, msg, 'w')
            JSONLoad(JSONfileName)

        except Exception as e:
            msg = f'JSON file {JSONfileName} is missing, impossible to create at file named "{JSONfileName}" at "{current_file_path}"'
            print(ConsoleReturn(msg))
            print(ErrorDef(e))
            exit()

# log start script
logs('---New Execution---', JSONScriptConfig, 'START', None)

# Use Urls.txt, Y true, F false
def UseUrlsTXT(JSONScriptConfig): 
    if JSONScriptConfig["AskUrlsTxt"]:
        return YoN('Use Urls.txt for URLS (Y/N):', 'UseUrlsTxt')
    else:
        return False

# Get url if N
def GetUrl():
    while True:
        base_url = input('URL:')
        logsInfo(f"User entered '{base_url}' as a url", 'Function/GetUrl')
        final_url = VideoUrlEdit(base_url, JSONYtdlpConfig)
        if final_url:
            return final_url



# url editing
def VideoUrlEdit(base_url,JSONYtdlpConfig):
    url_parsed = urlparse(base_url)
    # print(url_parsed)

    if all([url_parsed.scheme, url_parsed.netloc]):
        if url_parsed.netloc.endswith('pandaplay.io'):
            
            url_scheme = url_parsed.scheme # HTTP/HTTPS
            url_netlock = url_parsed.netloc # Domain
            url_path = url_parsed.path # Path
            url_file = url_path.rsplit('/', 1)[-1] # File
            url_OPath = url_path.rsplit('/', 1)[0] # Path without file

            if url_file != 'video.m3u8':
                final_url = "{}://{}{}{}".format(url_scheme, url_netlock, url_OPath, '/video.m3u8')
            else:
                final_url = base_url

            try:
                response = requests.get(final_url, headers=JSONYtdlpConfig['headers'])
                response.raise_for_status()
                print(f'Url "{final_url}" available')
                logsInfo(f'Url "{final_url}" available', 'Function/VideoUrlEdit')
                return final_url
            except requests.exceptions.RequestException as e:
                print(ErrorDef(e)) #del
                logsException(e, 'Function/VideoUrlEdit')

        
        else: 
            print(ErrorDef(f'Invalid url: "{base_url}"'))
            logsError(f'Invalid url: "{base_url}" (not pandaplay.io)', 'Function/VideoUrlEdit')
            return None
    else:
        print(ErrorDef(f'Invalid url: "{base_url}"'))
        logsError(f'Invalid url syntax: "{base_url}"', 'Function/VideoUrlEdit')
        return None

def UrlsTxtCheck(current_file_path):
    if os.path.isfile(os.path.join(current_file_path, 'urls.txt')):
        logsInfo('urls.txt exist', 'Function/UrlsTxtCheck')
        return True
    else:
        print(ErrorDef("urls.txt don't exist"))
        logsWarn("urls.txt don't exist", 'Function/UrlsTxtCheck')
        try:
            with open('urls.txt', 'a'):
                print(ConsoleReturn('urls.txt created'))
                logsInfo('urls.txt created', 'Function/UrlsTxtCheck')
                exit()
        except Exception as e:
            print(ErrorDef('Unable to create urls.txt'))
            logsCritical('Unable to create urls.txt', 'Function/UrlsTxtCheck')
            logsException(e, 'Function/UrlsTxtCheck')
            # verbose
            print(e)
            exit()


# loop for txt read Urls.txt
def UrlsLoop():
    validsUrl = []
    if UrlsTxtCheck(current_file_path):
        try: 
            with open('urls.txt', 'r') as file:
                txtUrls = [line.strip() for line in file.readlines() if line.strip()]

                for url in txtUrls:
                    final_url = VideoUrlEdit(url, JSONYtdlpConfig)
                    if final_url:
                        validsUrl.append(final_url)

                if not validsUrl:
                    print(ErrorDef('No correct url found'))
                    logsCritical('No correct url found in urls.txt', 'Function/UrlsLoop')
                    exit()
                else:
                    return validsUrl
        except Exception as e:
            logsException(e, 'Function/UrlsLoop')


# Location
def locationF(current_file_path, JSONScriptConfig, JSONfileName):
    # Check JSON settings
    if JSONScriptConfig['DownloadPath'] == '':
        if JSONScriptConfig['AskPath']:
            while True:
                destinationFolder = input('Location (empty for py file path):').strip()
            
                if destinationFolder:
                    if os.path.isdir(destinationFolder):
                        logsInfo(f'User entered "{destinationFolder}" as a correct destination folder', 'Function/locationF')
                        return destinationFolder
                    else:
                        msg = f"{destinationFolder} is an invalid path or folder"
                        print(ErrorDef(msg))
                        logsWarn(f'User entered "{destinationFolder}" as an incorrect destination folder', 'Function/locationF')
                else:
                    logsInfo(f'User did not specify a folder, current script file returned "{current_file_path}"', 'Function/locationF')
                    return current_file_path
        else:
            logsInfo(f'User did not specify a folder, current script file returned "{current_file_path}"', 'Function/locationF')
            return current_file_path
    else:
        if os.path.isdir(JSONScriptConfig['DownloadPath']):
            destinationFolder = JSONScriptConfig['DownloadPath']
            logsInfo(f'JSON file settings specified "{destinationFolder}" as a correct destination folder', 'Function/locationF')
            return destinationFolder
        else:
            destinationFolder = JSONScriptConfig['DownloadPath']
            msg = f"The path '{destinationFolder}' is invalid, if you don't understand this error, please check the JSON file '{JSONfileName}'"
            print(ErrorDef(msg))
            logsCritical(f'JSON file settings specified "{destinationFolder}" as a incorrect destination folder', 'Function/locationF')
            exit()
            

# File naming
def fileName(current_file_path, JSONScriptConfig, JSONfileName):
    location = locationF(current_file_path, JSONScriptConfig, JSONfileName)

    if not JSONScriptConfig['AskFileName']:
        fileN = input('File name (empty for default name):')
        logsInfo(f'User entered {fileN} for the name of downloded file', 'Function/fileName')
    else:
        fileN = ''
        logsInfo('Default name will be used for downloded file', 'Function/fileName')

    # if fileN empty
    if not fileN:
        if not JSONScriptConfig['FileName']:
            print(ErrorDef(f"File name empty or misconfigured (if you don't understand this error please check the JSON file '{JSONfileName}')"))

            exit()
        else:
            fileN = JSONScriptConfig['FileName']

    fileN2 = fileN
    it = 0
    while os.path.isfile(os.path.join(location, fileN2 + '.mp4')):
        it += 1
        fileN2 = f"{fileN}({it})"

    finalPath = os.path.join(location, fileN2)
    print(f'Actual file path : "{finalPath}"')
    logsInfo(f'The final name for downloded file is {fileN2}', 'Function/fileName')
    logsInfo(f'The final path for downloded file is {finalPath}', 'Function/fileName')
    return finalPath




# Download
def download(final_url, JSONYtdlpConfig, fileNameVar):
    options = JSONYtdlpConfig['options']
    ffmpegPath = options['ffmpeg_location']
    options["http_headers"] = JSONYtdlpConfig['headers']
    if not fileNameVar:
        return None


    if not ffmpegPath:
        ffmpegPath = ''
    else:
        options['outtmpl'] = fileNameVar

    options['ffmpeg_location'] = ffmpegPath

    options['verbose'] = True #del

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([final_url])
            logsInfo(f'{final_url} downloaded', 'Function/download')
    except Exception as e:
        print(ErrorDef(e))
        logsError(f'Issue to download "{final_url}"', 'Function/download')
        logsException(e, 'Function/download')




        # if Urls.txt used > loop
if UseUrlsTXT(JSONScriptConfig):
    urls = UrlsLoop()

    # call download() and fileName for each urls
    for element in urls:
        # filaName needs to be here if a name is already used
        fileNameVar = fileName(current_file_path, JSONScriptConfig, JSONfileName)
        download(element, JSONYtdlpConfig, fileNameVar)

else:
    while True:
        base_url = GetUrl()
        if base_url:
            fileNameVar = fileName(current_file_path, JSONScriptConfig, JSONfileName)
            final_url = VideoUrlEdit(base_url, JSONYtdlpConfig)
            if final_url:
                # dl fonc
                download(final_url, JSONYtdlpConfig, fileNameVar)
                break
        else:
            print(ErrorDef('Please enter a url'))
    







    



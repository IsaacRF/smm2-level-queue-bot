#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""SMM2 Level Queue System"""

# ---------------------------------------
# Libraries and references
# ---------------------------------------
import codecs
import json
import os
import re
import winsound
import ctypes

# ---------------------------------------
# [Required] Script information
# ---------------------------------------
ScriptName = "SMM2 Level Queue System"
Website = "https://twitch.tv/clickandslash"
Creator = "IsaacRF239 & Gabriel Rodríguez"
Author1Website = "https://isaacrf.com"
Author2Website = "https://twitter.com/gabri239"
Version = "1.1.0"
Description = "Super Mario Maker 2 Level Queue System"

# ---------------------------------------
# Versions
# ---------------------------------------
""" Major and recent Releases (open README.txt for full release notes)
1.1.0 - Adds a levels overlay and adds responses to configuration
1.0.0 - Initial Release
"""

# ---------------------------------------
# Variables
# ---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
levelsFile = os.path.join(os.path.dirname(__file__), "levels.txt")
overlayIndexPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "overlay", "index.html")
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YES = 6
eventLevelUpdate = "EVENT_SMM2QS_LEVEL_UPDATE"
levelCodePattern = re.compile("([A-HJ-NP-Za-hj-np-z0-9]{3})(-| )([A-HJ-NP-Za-hj-np-z0-9]{3})(-| )([A-HJ-NP-Za-hj-np-z0-9]{3})$")
twitchLineBreak = "_______________________________________  "
twitchLineHeader = "---------------- Cola de niveles -------------------"
wins = 0
skips = 0

# ---------------------------------------
# Classes
# ---------------------------------------
class Settings:
    """" Loads settings from file if file is found if not uses default values"""

    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile=None):
        if settingsFile and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')

        else:  # set variables if no custom settings file is found
            self.OnlyLive = False
            self.QueueOpen = True
            self.command_info = "!smm2lqs"
            self.command_add = "!add"
            self.command_list = "!list"
            self.command_position = "!position"
            self.command_current_level = "!level"
            self.command_next_level = "!nextlevel"
            self.command_queue_open = "!queueopen"
            self.command_queue_close = "!queueclose"
            self.command_win_level = "!winlevel"
            self.command_skip_level = "!skiplevel"
            self.command_delete_level = "!deletelevel"
            self.command_refresh_overlay = "!refreshlevels"
            self.PermissionBase = "Everyone"
            self.PermissionInfoBase = ""
            self.PermissionAdvanced = "Moderator"
            self.PermissionInfoAdvanced = ""
            self.Usage = "Stream Chat"
            self.omit_duplicated_levels = True
            self.OnDuplicatedLevel = "@{0} Level {1} is already on queue. Duplicated levels are omitted"
            self.is_queue_limited = False
            self.queue_length = 25
            self.OnQueueLimitReached = "@{0} Level queue is full (Max {1} levels). Wait till a slot is free to add your level"
            self.is_user_limited = False
            self.max_levels_by_user = 3
            self.OnMaxLevelsByUserReached = "@{0} You have reached max levels by user ({1}), wait till one of your levels is completed to add another one"
            self.UseCD = True
            self.CasterCD = True
            self.CooldownAdd = 0
            self.UserCooldownAdd = 3
            self.CooldownList = 10
            self.UserCooldownList = 10
            self.CooldownPosition = 0
            self.UserCooldownPosition = 10
            self.CooldownCurrentLevel = 3
            self.UserCooldownCurrentLevel = 3
            self.CooldownNextLevel = 3
            self.UserCooldownNextLevel = 3
            self.CooldownWinLevel = 2
            self.UserCooldownWinLevel = 2
            self.CooldownSkipLevel = 2
            self.UserCooldownSkipLevel = 2
            self.CooldownDeleteLevel = 2
            self.UserCooldownDeleteLevel = 2
            self.CooldownRefreshOverlay = 2
            self.UserCooldownRefreshOverlay = 2
            self.OnCooldown = "@{0} the command {1} is still on cooldown for {2} seconds!"
            self.OnUserCooldown = "@{0} the command {1} is still on user cooldown for {2} seconds!"
            self.RespInfo = "{0} <code> (XXX-YYY-ZZZ format, alphanumeric characters excluding I, O) to add a level to queue. {1}, {2}, {3} or {4} for info. SMM2 Level Queue System developed by {5}"
            self.RespQueueOpened = "Level queue is now open! Use {0} to add levels to queue"
            self.RespQueueClosed = "Level queue closed! Wait till a mod open the queue again to add your level"
            self.RespLevelAdded = "@{0} added level {1} to queue on position [{2}]"
            self.RespErrorLevelAdd = "System error adding level to queue, call a mod"
            self.RespWrongLevelCodeFormat = "Código de nivel incorrecto, el formato debe coincidir con XXX-YYY-ZZZ, caracteres alfanuméricos sin símbolos ni las letras I, O"
            self.RespCurrentLevelRequested = "@{0} Level currently played is {1}"
            self.RespNextLevelRequested = "@{0} Next level on queue is {1}"
            self.RespNoLevelsOnQueue = "No levels on queue, add yours using {0}"
            self.RespErrorReadingQueue = "Error reading queue file, call a mod"
            self.RespErrorModifyingQueue = "Error updating queue file, call a mod"
            self.RespUserLevelPositions = "@{0} you have levels on positions {1}"
            self.RespUserLevelPositionsNoLevels = "@{0} you have no levels on queue"
            self.RespLevelFinishedWin = "Level completed!"
            self.RespLevelFinishedSkip = "Level skipped."
            self.RespLevelFinishedDelete = "Level deleted."
            self.RespNextLevel = "Next level is {0}"
            self.RespNoMoreLevels = "No more levels on queue. Add your level using {0}"
            self.RespOverlayUpdated = "Here we go! Levels Overlay updated"
            self.RespErrorOverlayUpdate = "Error updating overlay. Call a staff member"
            self.RespPermissionBase= "$user -> Only $permissionbase ($permissioninfobase) or higher can use this command"
            self.RespPermissionAdvanced= "$user -> Only $permissionadvanced ($permissioninfoadvanced) or higher can use this command"

        #Create levels file if it doesn't exist on initialization
        if not os.path.exists(levelsFile):
            open(levelsFile, 'w').close()

    # Reload settings on save through UI
    def Reload(self, data):
        """Reload settings on save through UI"""
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        return

    def Save(self, settingsfile):
        """ Save settings contained within to .json and .js settings files. """
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8",
                          ensure_ascii=False)
            with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(
                    self.__dict__, encoding='utf-8', ensure_ascii=False)))
        except ValueError:
            Parent.Log(ScriptName, "Failed to save settings to file.")
        return

class OverlayInfo:
    def __init__(self, currentLevelInfo = "", nextLevelInfo = "", wins = 0, skips = 0):
        for char in ['[', '@', '\n', ']'] :
            currentLevelInfo = currentLevelInfo.replace(char, '')
            nextLevelInfo = nextLevelInfo.replace(char, '')

        if currentLevelInfo != "":
            currentLevelInfoSplits = currentLevelInfo.split(" ")
            currentLevelCode = currentLevelInfoSplits[0]
            currentLevelUser = currentLevelInfoSplits[1]
        else:
            currentLevelCode = ""
            currentLevelUser = ""

        if nextLevelInfo != "":
            nextLevelInfoSplits = nextLevelInfo.split(" ")
            nextLevelCode = nextLevelInfoSplits[0]
            nextLevelUser = nextLevelInfoSplits[1]
        else:
            nextLevelCode = ""
            nextLevelUser = ""

        self.currentLevelCode = currentLevelCode
        self.currentLevelUser = currentLevelUser
        self.nextLevelCode = nextLevelCode
        self.nextLevelUser = nextLevelUser
        self.wins = wins
        self.skips = skips

# ---------------------------------------
# Settings functions
# ---------------------------------------
def SetDefaults():
    """Set default settings function"""
    winsound.MessageBeep()
    returnValue = MessageBox(0, u"You are about to reset the settings, "
                                "are you sure you want to contine?", u"Reset settings file?", 4)
    if returnValue == MB_YES:
        global MySet
        Settings.Save(MySet, settingsFile)
        returnValue = MessageBox(
            0, u"Settings successfully restored to default values", u"Reset complete!", 0)

def RestoreAndTranslateDefaultResponsesESP():
    RestoreAndTranslateDefaultResponses("ESP")

def RestoreAndTranslateDefaultResponsesENG():
    RestoreAndTranslateDefaultResponses("ENG")

def RestoreAndTranslateDefaultResponses(language="ENG"):
    """Restore ONLY default responses in different languages"""

    """Set default settings function"""
    winsound.MessageBeep()
    returnValue = MessageBox(0, u"You are about to reset the chat responses to default ones (" + language + "), "
                                "are you sure you want to contine?", u"Reset chat responses?", 4)
    if returnValue != MB_YES:
        return

    if language == "ESP":
        MySet.OnDuplicatedLevel = "@{0} El nivel {1} ya está en la cola. Los niveles duplicados se omiten"
        MySet.OnQueueLimitReached = "@{0} La cola está llena ({1} niveles máximo). Espera a que se libere un hueco para añadir tu nivel"
        MySet.OnMaxLevelsByUserReached = "@{0} Has alcanzado el máximo de niveles por persona ({1}), espera a que se complete alguno de tus niveles para añadir otro"
        MySet.OnCooldown = "@{0} el comando {1} aún está en cooldown global. Espera {2} segundos"
        MySet.OnUserCooldown = "@{0} aún faltan {2} segundos para que puedas usar el comando {1}"
        MySet.RespInfo = "{0} <código> (En formato XXX-YYY-ZZZ, caracteres alfanuméricos excluyendo I, O) para añadir un nivel a la lista. {1}, {2}, {3} o {4} para info. SMM2 Level Queue System desarrollado por {5}"
        MySet.RespQueueOpened = "Cola de niveles abierta! Usa {0} <código> para añadir niveles a la cola"
        MySet.RespQueueClosed = "Cola de niveles cerrada! Espera a que un mod la vuelva a abrir para añadir tus niveles"
        MySet.RespLevelAdded = "@{0} ha añadido el nivel {1} a la cola en la posición [{2}]"
        MySet.RespErrorLevelAdd = "Error del sistema al añadir el nivel a la cola, avisa a un mod"
        MySet.RespWrongLevelCodeFormat = "Código de nivel incorrecto, el formato debe coincidir con XXX-YYY-ZZZ, caracteres alfanuméricos sin símbolos ni las letras I, O"
        MySet.RespCurrentLevelRequested = "@{0} El nivel en juego es {1}"
        MySet.RespNextLevelRequested = "@{0} El siguiente nivel en cola es {1}"
        MySet.RespNoLevelsOnQueue = "No hay niveles en la cola. Añade el tuyo usando {0}"
        MySet.RespErrorReadingQueue = "Error al intentar leer la lista de niveles, avisa a un mod"
        MySet.RespErrorModifyingQueue = "Error al intentar actualizar la lista de niveles, avisa a un mod"
        MySet.RespUserLevelPositions = "@{0} tienes niveles en las posiciones {1}"
        MySet.RespUserLevelPositionsNoLevels = "@{0} no tienes niveles en cola"
        MySet.RespLevelFinishedWin = "¡Nivel superado!"
        MySet.RespLevelFinishedSkip = "Nivel skipeado."
        MySet.RespLevelFinishedDelete = "Nivel eliminado."
        MySet.RespNextLevel = "El siguiente nivel es {0}"
        MySet.RespNoMoreLevels = "No hay más niveles en cola, añade el tuyo con {0}"
        MySet.RespOverlayUpdated = "Here we go! Overlay de niveles actualizado"
        MySet.RespErrorOverlayUpdate = "Error actualizando el overlay de niveles. Dale un toque a alguien del staff"
        MySet.RespPermissionBase= "$user -> Sólo $permissionbase ($permissioninfobase) o superior pueden usar este comando"
        MySet.RespPermissionAdvanced= "$user -> Sólo $permissionadvanced ($permissioninfoadvanced) o superior pueden usar este comando"
    else:
        MySet.OnDuplicatedLevel = "@{0} Level {1} is already on queue. Duplicated levels are omitted"
        MySet.OnQueueLimitReached = "@{0} Level queue is full (Max {1} levels). Wait till a slot is free to add your level"
        MySet.OnMaxLevelsByUserReached = "@{0} You have reached max levels by user ({1}), wait till one of your levels is completed to add another one"
        MySet.OnCooldown = "@{0} the command {1} is still on cooldown for {2} seconds!"
        MySet.OnUserCooldown = "@{0} the command {1} is still on user cooldown for {2} seconds!"
        MySet.RespInfo = "{0} <code> (XXX-YYY-ZZZ format, alphanumeric characters excluding I, O) to add a level to queue. {1}, {2}, {3} or {4} for info. SMM2 Level Queue System developed by {5}"
        MySet.RespQueueOpened = "Level queue is now open! Use {0} to add levels to queue"
        MySet.RespQueueClosed = "Level queue closed! Wait till a mod open the queue again to add your level"
        MySet.RespLevelAdded = "@{0} added level {1} to queue on position [{2}]"
        MySet.RespErrorLevelAdd = "System error adding level to queue, call a mod"
        MySet.RespWrongLevelCodeFormat = "Código de nivel incorrecto, el formato debe coincidir con XXX-YYY-ZZZ, caracteres alfanuméricos sin símbolos ni las letras I, O"
        MySet.RespCurrentLevelRequested = "@{0} Level currently played is {1}"
        MySet.RespNextLevelRequested = "@{0} Next level on queue is {1}"
        MySet.RespNoLevelsOnQueue = "No levels on queue, add yours using {0}"
        MySet.RespErrorReadingQueue = "Error reading queue file, call a mod"
        MySet.RespErrorModifyingQueue = "Error updating queue file, call a mod"
        MySet.RespUserLevelPositions = "@{0} you have levels on positions {1}"
        MySet.RespUserLevelPositionsNoLevels = "@{0} you have no levels on queue"
        MySet.RespLevelFinishedWin = "Level completed!"
        MySet.RespLevelFinishedSkip = "Level skipped."
        MySet.RespLevelFinishedDelete = "Level deleted."
        MySet.RespNextLevel = "Next level is {0}"
        MySet.RespNoMoreLevels = "No more levels on queue. Add your level using {0}"
        MySet.RespOverlayUpdated = "Here we go! Levels Overlay updated"
        MySet.RespErrorOverlayUpdate = "Error updating overlay. Call a staff member"
        MySet.RespPermissionBase= "$user -> Only $permissionbase ($permissioninfobase) or higher can use this command"
        MySet.RespPermissionAdvanced= "$user -> Only $permissionadvanced ($permissioninfoadvanced) or higher can use this command"

    Settings.Save(MySet, settingsFile)

    MessageBox(
            0, u"Default responses in (" + language + ") restored. "
                "RELOAD SCRIPTS to see new responses on config panel.", u"Translation complete!", 0)

def ReloadSettings(jsondata):
    """Reload settings on pressing the save button"""
    global MySet
    MySet.Reload(jsondata)

def openCreatorTwitchChannel():
    os.startfile(Website)

def openAuthor1Website():
    os.startfile(Author1Website)

def openAuthor2Website():
    os.startfile(Author2Website)

# ---------------------------------------
# Optional functions
# ---------------------------------------
def OpenReadMe():
    """Open the readme.txt in the scripts folder"""
    location = os.path.join(os.path.dirname(__file__), "README.txt")
    os.startfile(location)


def SendResp(data, Usage, Message):
    """Sends message to Stream or discord chat depending on settings"""
    Message = Message.replace("$user", data.UserName)
    Message = Message.replace("$currencyname", Parent.GetCurrencyName())
    Message = Message.replace("$target", data.GetParam(1))
    Message = Message.replace("$permissionbase", MySet.PermissionBase)
    Message = Message.replace("$permissioninfobase", MySet.PermissionInfoBase)
    Message = Message.replace("$permissionadvanced", MySet.PermissionAdvanced)
    Message = Message.replace("$permissioninfoadvanced", MySet.PermissionInfoAdvanced)

    l = ["Stream Chat", "Chat Both", "All", "Stream Both"]
    if not data.IsFromDiscord() and (Usage in l) and not data.IsWhisper():
        Parent.SendStreamMessage(Message)

    l = ["Stream Whisper", "Whisper Both", "All", "Stream Both"]
    if not data.IsFromDiscord() and data.IsWhisper() and (Usage in l):
        Parent.SendStreamWhisper(data.User, Message)

    l = ["Discord Chat", "Chat Both", "All", "Discord Both"]
    if data.IsFromDiscord() and not data.IsWhisper() and (Usage in l):
        Parent.SendDiscordMessage(Message)

    l = ["Discord Whisper", "Whisper Both", "All", "Discord Both"]
    if data.IsFromDiscord() and data.IsWhisper() and (Usage in l):
        Parent.SendDiscordDM(data.User, Message)


def IsFromValidSource(data, Usage):
    """Return true or false depending on the message is sent from
    a source that's in the usage setting or not"""
    if not data.IsFromDiscord():
        l = ["Stream Chat", "Chat Both", "All", "Stream Both"]
        if not data.IsWhisper() and (Usage in l):
            return True

        l = ["Stream Whisper", "Whisper Both", "All", "Stream Both"]
        if data.IsWhisper() and (Usage in l):
            return True

    if data.IsFromDiscord():
        l = ["Discord Chat", "Chat Both", "All", "Discord Both"]
        if not data.IsWhisper() and (Usage in l):
            return True

        l = ["Discord Whisper", "Whisper Both", "All", "Discord Both"]
        if data.IsWhisper() and (Usage in l):
            return True
    return False


def CopyOverlayIndexPath():
    """Copy index.html filepath to clipboard"""
    command = 'echo ' + overlayIndexPath.strip() + '| clip'
    os.system(command)


def AddCooldown(command, user, userCooldown, globalCooldown):
    """add cooldowns"""
    isCaster = Parent.HasPermission(user, "Caster", "")

    Parent.AddCooldown(ScriptName, command, globalCooldown)
    if not isCaster or (isCaster and not MySet.CasterCD):
        Parent.AddUserCooldown(ScriptName, command, user, userCooldown)


def IsOnCooldown(data):
    """Return true if command is on cooldown and send cooldown message if enabled"""
    isOnCooldown = Parent.IsOnCooldown(ScriptName, data.GetParam(0).lower())
    isOnUserCooldown = Parent.IsOnUserCooldown(ScriptName, data.GetParam(0).lower(), data.User)
    isCaster = (Parent.HasPermission(data.User, "Caster", "") and MySet.CasterCD)

    if (isOnCooldown or isOnUserCooldown) and not isCaster:
        if MySet.UseCD:
            cooldownDuration = Parent.GetCooldownDuration(ScriptName, data.GetParam(0).lower())
            userCDD = Parent.GetUserCooldownDuration(ScriptName, data.GetParam(0).lower(), data.User)

            if cooldownDuration > userCDD:
                m_CooldownRemaining = cooldownDuration
                message = MySet.OnCooldown.format(data.UserName, data.GetParam(0).lower(), m_CooldownRemaining)
                SendResp(data, MySet.Usage, message)
            else:
                m_CooldownRemaining = userCDD
                message = MySet.OnUserCooldown.format(data.UserName, data.GetParam(0).lower(), m_CooldownRemaining)
                SendResp(data, MySet.Usage, message)
        return True
    return False

def HasPermission(data):
    """Returns true if user has permission and false if user doesn't"""
    if (data.GetParam(0).lower() == MySet.command_info.lower() or
    data.GetParam(0).lower() == MySet.command_add.lower() or
    data.GetParam(0).lower() == MySet.command_list.lower() or
    data.GetParam(0).lower() == MySet.command_position.lower() or
    data.GetParam(0).lower() == MySet.command_current_level.lower() or
    data.GetParam(0).lower() == MySet.command_next_level.lower()):
        if not Parent.HasPermission(data.User, MySet.PermissionBase, MySet.PermissionInfoBase):
            message = MySet.RespPermissionBase.format(data.UserName, MySet.PermissionBase, MySet.PermissionInfoBase)
            SendResp(data, MySet.Usage, message)
            return False
    elif (data.GetParam(0).lower() == MySet.command_win_level.lower() or
    data.GetParam(0).lower() == MySet.command_queue_open.lower() or
    data.GetParam(0).lower() == MySet.command_queue_close.lower() or
    data.GetParam(0).lower() == MySet.command_skip_level.lower() or
    data.GetParam(0).lower() == MySet.command_delete_level.lower() or
    data.GetParam(0).lower() == MySet.command_refresh_overlay.lower()):
        if not Parent.HasPermission(data.User, MySet.PermissionAdvanced, MySet.PermissionInfoAdvanced):
            message = MySet.RespPermissionAdvanced.format(data.UserName, MySet.PermissionAdvanced, MySet.PermissionInfoAdvanced)
            SendResp(data, MySet.Usage, message)
            return False

    return True

# ---------------------------------------
# [Script] functions
# ---------------------------------------
def SMM2LQSInfo(data):
    """Sends a chat response containing commands info"""

    message = MySet.RespInfo.format(MySet.command_add, MySet.command_current_level, MySet.command_next_level, MySet.command_list, MySet.command_position, Creator)
    SendResp(data, MySet.Usage, message)

def AddLevel(code, data):
    """Adds a level to queue file and updates overlay if 1 or less levels are in queue

    Parameters:
    code (string): Level code in XXX-YYY-ZZZ format
    data: Command execution info
    """

    levelsNumber = CountLevels()

    if code == "":
        SMM2LQSInfo(data)
        return

    if not MySet.QueueOpen:
        SendResp(data, MySet.Usage, MySet.RespQueueClosed)
        return

    if MySet.is_queue_limited and levelsNumber >= MySet.queue_length:
        message = MySet.OnQueueLimitReached.format(data.UserName, MySet.queue_length)
        SendResp(data, MySet.Usage, message)
        return

    if MySet.is_user_limited and CountLevelsByUser(data.UserName) >= MySet.max_levels_by_user:
        message = MySet.OnMaxLevelsByUserReached.format(data.UserName, str(MySet.max_levels_by_user))
        SendResp(data, MySet.Usage, message)
        return

    if MySet.omit_duplicated_levels and IsLevelOnQueue(code):
        message = MySet.OnDuplicatedLevel.format(data.UserName, code)
        SendResp(data, MySet.Usage, message)
        return

    if levelCodePattern.match(code):
        try:
            isUIUpdateRequired = (levelsNumber <= 1)

            with open(levelsFile, 'a') as file:
                file.write(code + " [@" + data.UserName + "]" + '\n')

            #UPDATE OVERLAY IF REQUIRED
            if isUIUpdateRequired:
                with open(levelsFile, 'r') as file:
                    levels = file.readlines()

                    if len(levels) > 0:
                        currentLevel = levels[0].strip()
                    else:
                        currentLevel = ""

                    if len(levels) > 1:
                        nextLevel = levels[1].strip()
                    else:
                        nextLevel = ""

                    overlayInfo = OverlayInfo(currentLevel, nextLevel, wins, skips)
                    Parent.BroadcastWsEvent(eventLevelUpdate, json.dumps(overlayInfo.__dict__))

            message = MySet.RespLevelAdded.format(data.UserName, code, str(levelsNumber + 1))
            SendResp(data, MySet.Usage, message)
        except:
            SendResp(data, MySet.Usage, MySet.RespErrorLevelAdd)
    else:
        SendResp(data, MySet.Usage, MySet.RespWrongLevelCodeFormat)

def ListLevels(data):
    """List levels on queue"""
    if CountLevels() <= 0:
        message = MySet.RespNoLevelsOnQueue.format(MySet.command_add)
        SendResp(data, MySet.Usage, message)
        return

    header = twitchLineBreak + twitchLineHeader + twitchLineBreak
    body = ""
    lineNumber = 1

    try:
        with open(levelsFile, "r") as file:
            for line in file:
                body += "[" + str(lineNumber) + "] " + line.replace('\n','') + " " + twitchLineBreak
                lineNumber += 1

        SendResp(data, MySet.Usage, header + body)
    except:
        SendResp(data, MySet.Usage, MySet.RespErrorReadingQueue)

def GetPositions(data):
    """List positions in which user has levels on"""
    positions = ""

    try:
        with open(levelsFile, 'r') as f:
            levels = f.readlines()

        if len(levels) <= 0:
            message = MySet.RespNoLevelsOnQueue.format(MySet.command_add)
            SendResp(data, MySet.Usage, message)
            return

        for i, level in enumerate(levels):
            if data.UserName in level:
                positions += " [" + str(i + 1) + "]"

        if positions != "":
            message = MySet.RespUserLevelPositions.format(data.UserName, positions)
            SendResp(data, MySet.Usage, message)
        else:
            message = MySet.RespUserLevelPositionsNoLevels.format(data.UserName)
            SendResp(data, MySet.Usage, message)
    except:
        SendResp(data, MySet.Usage, MySet.RespErrorReadingQueue)

def CountLevels():
    """Count levels on queue

    Returns:
    int: Number of levels on queue
    """

    try:
        with open(levelsFile, 'r') as f:
            levels = f.readlines()

        return len(levels)
    except:
        return 0

def IsLevelOnQueue(levelCode):
    """Checks if specified level is already on queue

    Returns:
    bool: True if level is present in queue, False otherwise
    """

    try:
        with open(levelsFile, 'r') as f:
            levels = f.readlines()

            for level in levels:
                if levelCode in level:
                    return True

        return False
    except:
        return False

def CountLevelsByUser(userName):
    """Count levels on queue added by specified user

    Parameters:
    userName (string): User name

    Returns:
    int: Number of levels on queue by user
    """

    count = 0

    try:
        with open(levelsFile, 'r') as f:
            levels = f.readlines()

        if len(levels) <= 0:
            return 0
        else:
            for level in levels:
                if userName in level:
                    count += 1

        return count
    except:
        return 0

def CurrentLevel(data):
    """Shows first level on queue"""
    #try:
    with open(levelsFile, 'r') as f:
        level = f.readline().strip()

    if level == "":
        message = MySet.RespNoLevelsOnQueue.format(MySet.command_add)
        SendResp(data, MySet.Usage, message)
    else:
        message = MySet.RespCurrentLevelRequested.format(data.UserName, level)
        SendResp(data, MySet.Usage, message)
    #except:
    #    SendResp(data, MySet.Usage, MySet.RespErrorReadingQueue)

def NextLevel(data):
    """Shows next level on queue"""
    try:
        with open(levelsFile, 'r') as f:
            levels = f.readlines()
            if len(levels) >= 2:
                level = levels[1].strip()
                if level != "":
                    message = MySet.RespNextLevelRequested.format(data.UserName, level)
                    SendResp(data, MySet.Usage, message)
                else:
                    message = MySet.RespNoLevelsOnQueue.format(MySet.command_add)
                    SendResp(data, MySet.Usage, message)
            else:
                message = MySet.RespNoLevelsOnQueue.format(MySet.command_add)
                SendResp(data, MySet.Usage, message)
    except:
        SendResp(data, MySet.Usage, MySet.RespErrorReadingQueue)

def FinishLevel(data, result=0):
    """Removes first level from queue and updates score if needed

    Parameters:
    data: Command execution info
    result (int): 0 = Win, 1 = Skip, 2 = Delete / No score update (default 0)
    """

    global wins
    global skips

    try:
        with open(levelsFile, 'r') as f: #open in read / write mode
            levels = f.readlines()
            if len(levels) <= 0:
                message = MySet.RespNoLevelsOnQueue.format(MySet.command_add)
                SendResp(data, MySet.Usage, message)
                return

        with open(levelsFile, 'w') as f:
            del levels[0]
            f.writelines(levels)

            if len(levels) > 0:
                currentLevel = levels[0].strip()
            else:
                currentLevel = ""

            if len(levels) > 1:
                nextLevel = levels[1].strip()
            else:
                nextLevel = ""

            #CRAFT RESPONSE AND UPDATE SCORE
            if result == 0:
                message = MySet.RespLevelFinishedWin
                wins = wins + 1
            elif result == 1:
                message = MySet.RespLevelFinishedSkip
                skips = skips + 1
            else:
                message = MySet.RespLevelFinishedDelete

            if currentLevel != "":
                message = message + " " + MySet.RespNextLevel.format(currentLevel)
            else:
                message = message + " " + MySet.RespNoMoreLevels.format(MySet.command_add)

            #SEND BOT RESPONSE
            SendResp(data, MySet.Usage, message)

            #UPDATE OVERLAY INFO
            overlayInfo = OverlayInfo(currentLevel, nextLevel, wins, skips)
            Parent.BroadcastWsEvent(eventLevelUpdate, json.dumps(overlayInfo.__dict__))
    except:
        SendResp(data, MySet.Usage, MySet.RespErrorModifyingQueue)

def RefreshOverlay(data):
    """Refreshes bot overlay"""
    global wins
    global skips

    if CountLevels() <= 0:
        message = MySet.RespNoLevelsOnQueue.format(MySet.command_add)
        SendResp(data, MySet.Usage, message)
    else:
        try:
            with open(levelsFile, 'r') as f:
                levels = f.readlines()

            if len(levels) > 0:
                currentLevel = levels[0].strip()
            else:
                currentLevel = ""

            if len(levels) > 1:
                nextLevel = levels[1].strip()
            else:
                nextLevel = ""

            overlayInfo = OverlayInfo(currentLevel, nextLevel, wins, skips)
            Parent.BroadcastWsEvent(eventLevelUpdate, json.dumps(overlayInfo.__dict__))

            SendResp(data, MySet.Usage, MySet.RespOverlayUpdated)
        except:
            SendResp(data, MySet.Usage, MySet.RespErrorOverlayUpdate)

def QueueChangeState(data, state=True):
    """Changes queue state

    Parameters:
    data: Command execution info
    state (bool): Open queue if True, close queue otherwise (default True)
    """

    MySet.QueueOpen = state
    Settings.Save(MySet, settingsFile)

    if state:
        message = MySet.RespQueueOpened.format(MySet.command_add)
        SendResp(data, MySet.Usage, message)
    else:
        SendResp(data, MySet.Usage, MySet.RespQueueClosed)

# ---------------------------------------
# [Required] functions
# ---------------------------------------
def Init():
    """data on Load, required function"""
    global MySet
    MySet = Settings(settingsFile)

    if MySet.Usage == "Twitch Chat":
        MySet.Usage = "Stream Chat"
        Settings.Save(MySet, settingsFile)

    elif MySet.Usage == "Twitch Whisper":
        MySet.Usage = "Stream Whisper"
        Settings.Save(MySet, settingsFile)

    elif MySet.Usage == "Twitch Both":
        MySet.Usage = "Stream Both"
        Settings.Save(MySet, settingsFile)


def Execute(data):
    """Required Execute data function"""
    if not IsFromValidSource(data, MySet.Usage):
        return

    if not HasPermission(data):
        return

    if data.IsChatMessage() and not MySet.OnlyLive or Parent.IsLive():
        if IsOnCooldown(data):
            return

        if data.GetParam(0).lower() == MySet.command_add.lower():
            levelCode = data.Message.replace(data.GetParam(0),'').strip().replace(' ','-').upper()
            AddLevel(levelCode, data)
            AddCooldown(data.GetParam(0).lower(), data.User, MySet.UserCooldownAdd, MySet.CooldownAdd)
            return
        elif data.GetParam(0).lower() == MySet.command_list.lower():
            ListLevels(data)
            AddCooldown(data.GetParam(0).lower(), data.User, MySet.UserCooldownList, MySet.CooldownList)
            return
        elif data.GetParam(0).lower() == MySet.command_position.lower():
            GetPositions(data)
            AddCooldown(data.GetParam(0).lower(), data.User, MySet.UserCooldownPosition, MySet.CooldownPosition)
            return
        elif data.GetParam(0).lower() == MySet.command_current_level.lower():
            CurrentLevel(data)
            AddCooldown(data.GetParam(0).lower(), data.User, MySet.UserCooldownCurrentLevel, MySet.CooldownCurrentLevel)
            return
        elif data.GetParam(0).lower() == MySet.command_next_level.lower():
            NextLevel(data)
            AddCooldown(data.GetParam(0).lower(), data.User, MySet.UserCooldownNextLevel, MySet.CooldownNextLevel)
            return
        elif data.GetParam(0).lower() == MySet.command_queue_open.lower():
            QueueChangeState(data, True)
            return
        elif data.GetParam(0).lower() == MySet.command_queue_close.lower():
            QueueChangeState(data, False)
            return
        elif data.GetParam(0).lower() == MySet.command_win_level.lower():
            FinishLevel(data, 0)
            AddCooldown(data.GetParam(0).lower(), data.User, MySet.UserCooldownWinLevel, MySet.CooldownWinLevel)
            return
        elif data.GetParam(0).lower() == MySet.command_skip_level.lower():
            FinishLevel(data, 1)
            AddCooldown(data.GetParam(0).lower(), data.User, MySet.UserCooldownSkipLevel, MySet.CooldownSkipLevel)
            return
        elif data.GetParam(0).lower() == MySet.command_delete_level.lower():
            FinishLevel(data, 2)
            AddCooldown(data.GetParam(0).lower(), data.User, MySet.UserCooldownDeleteLevel, MySet.CooldownDeleteLevel)
            return
        elif data.GetParam(0).lower() == MySet.command_refresh_overlay.lower():
            RefreshOverlay(data)
            AddCooldown(data.GetParam(0).lower(), data.User, MySet.UserCooldownRefreshOverlay, MySet.CooldownRefreshOverlay)
            return


def Tick():
    """Required tick function"""

#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""SMM2 Level queue system"""

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
ScriptName = "SMM2 Queue"
Website = "https://www.twitch.tv/clickandslash"
Creator = "IsaacRF239 from Click and Slash"
Version = "1.0.0"
Description = "Super Mario Maker 2 level queue system"

# ---------------------------------------
# TODO List
# ---------------------------------------
#TODO: Make cooldowns work
#TODO: Allow to open and close the queue
#TODO: Make an overlay to represent info
#TODO: Do something with the levels cut from levels file on win or skip

# ---------------------------------------
# Versions
# ---------------------------------------
""" Major and recent Releases (open README.txt for full release notes)
1.0.0 - Initial Release
"""

# ---------------------------------------
# Variables
# ---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
levelsFile = os.path.join(os.path.dirname(__file__), "levels.txt")
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YES = 6
levelCodePattern = re.compile("([A-HJ-NP-Za-hj-np-z0-9]{3})(-| )([A-HJ-NP-Za-hj-np-z0-9]{3})(-| )([A-HJ-NP-Za-hj-np-z0-9]{3})$")
twitchLineBreak = "__________________________________________________________"

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
            self.command_add = "!add"
            self.command_list = "!list"
            self.command_position = "!position"
            self.command_current_level = "!level"
            self.command_next_level = "!nextlevel"
            self.command_win_level = "!winlevel"
            self.command_skip_level = "!skiplevel"
            self.is_queue_limited = False
            self.queue_length = 25
            self.is_user_limited = False
            self.max_levels_by_user = 3
            self.PermissionBase = "Everyone"
            self.PermissionInfoBase = ""
            self.PermissionAdvanced = "Moderator"
            self.PermissionInfoAdvanced = ""
            self.Usage = "Stream Chat"
            self.UseCD = True
            self.Cooldown = 5
            self.OnCooldown = "{0} the command is still on cooldown for {1} seconds!"
            self.UserCooldown = 10
            self.OnUserCooldown = "{0} the command is still on user cooldown for {1} seconds!"
            self.CasterCD = True
            self.NotEnoughResponse = "{0} you don't have that many {1} to gamble! "
            self.InfoResponse = "!add <código> para añadir un nivel a la lista. !currentlevel, !nextlevel o !list para info"
            self.PermissionRespBase= "$user -> Sólo $permissionbase ($permissioninfobase) o superior pueden usar este comando"
            self.PermissionRespAdvanced= "$user -> Sólo $permissionadvanced ($permissioninfoadvanced) o superior pueden usar este comando"

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

# ---------------------------------------
# Settings functions
# ---------------------------------------
def SetDefaults():
    """Set default settings function"""
    winsound.MessageBeep()
    returnValue = MessageBox(0, u"You are about to reset the settings, "
                                "are you sure you want to contine?", u"Reset settings file?", 4)
    if returnValue == MB_YES:
        returnValue = MessageBox(
            0, u"Settings successfully restored to default values", u"Reset complete!", 0)
        global MySet
        Settings.Save(MySet, settingsFile)


def ReloadSettings(jsondata):
    """Reload settings on pressing the save button"""
    global MySet
    MySet.Reload(jsondata)

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


def ControlC():
    """Copy index.html filepath to clipboard"""
    """    winsound.MessageBeep()
        returnValue = MessageBox(0, u"You are about copy the index.html filepath "
                                    "to your clipboard, this will overwrite any "
                                    "information you have there now. "
                                    "Are you sure you want to contine?"
                                , u"Copy to clipboard", 4)
        if returnValue == 6:
            indexPath = os.path.dirname(os.path.abspath(__file__)) + "\\index.html"
            command = 'echo ' + indexPath.strip() + '| clip'
            os.system(command)
    """
    winsound.MessageBeep()
    returnValue = MessageBox(
        0, u"This is just a placeholder.\r\nWanna open another box?", u"Open another window?", 4)
    if returnValue == 6:
        returnValue = MessageBox(
            0, u"Here's your box, now you gotta be happy!", u"Happy now?", 0)


def AddCooldown(data):
    """add cooldowns"""
    if Parent.HasPermission(data.User, "Caster", "") and MySet.CasterCD:
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
        return

    else:
        Parent.AddUserCooldown(ScriptName, MySet.Command,
                               data.User, MySet.UserCooldown)
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)


def IsOnCooldown(data):
    """Return true if command is on cooldown and send cooldown message if enabled"""
    cooldown = Parent.IsOnCooldown(ScriptName, MySet.Command)
    userCooldown = Parent.IsOnUserCooldown(
        ScriptName, MySet.Command, data.User)
    caster = (Parent.HasPermission(data.User, "Caster", "") and MySet.CasterCD)

    if (cooldown or userCooldown) and caster is False:

        if MySet.UseCD:
            cooldownDuration = Parent.GetCooldownDuration(
                ScriptName, MySet.Command)
            userCDD = Parent.GetUserCooldownDuration(
                ScriptName, MySet.Command, data.User)

            if cooldownDuration > userCDD:
                m_CooldownRemaining = cooldownDuration

                message = MySet.OnCooldown.format(
                    data.UserName, m_CooldownRemaining)
                SendResp(data, MySet.Usage, message)

            else:
                m_CooldownRemaining = userCDD

                message = MySet.OnUserCooldown.format(
                    data.UserName, m_CooldownRemaining)
                SendResp(data, MySet.Usage, message)
        return True
    return False

def HasPermission(data):
    """Returns true if user has permission and false if user doesn't"""
    if (data.GetParam(0).lower() == MySet.command_add.lower() or
    data.GetParam(0).lower() == MySet.command_list.lower() or
    data.GetParam(0).lower() == MySet.command_position.lower() or
    data.GetParam(0).lower() == MySet.command_current_level.lower() or
    data.GetParam(0).lower() == MySet.command_next_level.lower()):
        if not Parent.HasPermission(data.User, MySet.PermissionBase, MySet.PermissionInfoBase):
            message = MySet.PermissionRespBase.format(data.UserName, MySet.PermissionBase, MySet.PermissionInfoBase)
            SendResp(data, MySet.Usage, message)
            return False
    elif (data.GetParam(0).lower() == MySet.command_win_level.lower() or
    data.GetParam(0).lower() == MySet.command_skip_level.lower()):
        if not Parent.HasPermission(data.User, MySet.PermissionAdvanced, MySet.PermissionInfoAdvanced):
            message = MySet.PermissionRespAdvanced.format(data.UserName, MySet.PermissionAdvanced, MySet.PermissionInfoAdvanced)
            SendResp(data, MySet.Usage, message)
            return False

    return True

# ---------------------------------------
# [Script] functions
# ---------------------------------------
def AddLevel(code, data):
    if code == "":
        SendResp(data, MySet.Usage, MySet.InfoResponse)
        return

    if MySet.is_queue_limited and CountLevels() >= MySet.queue_length:
        SendResp(data, MySet.Usage, "La cola está llena, espera a que se libere un hueco para añadir tu nivel")
        return

    if MySet.is_user_limited and CountLevelsByUser(data.UserName) >= MySet.max_levels_by_user:
        SendResp(data, MySet.Usage, "Has alcanzado el máximo de niveles por persona (" + str(MySet.max_levels_by_user) + "), espera a que se complete alguno de tus niveles")
        return

    if levelCodePattern.match(code):
        try:
            with open(levelsFile, 'a') as file:
                file.write(code + " [@" + data.UserName + "]" + '\n')

            SendResp(data, MySet.Usage, "@" + data.UserName + " ha añadido el nivel " + code + " a la cola en posición [" + str(CountLevels()) + "]")
        except:
            SendResp(data, MySet.Usage, "Ha ocurrido un error al intentar agregar el nivel a la cola, avisa a un mod")
    else:
        SendResp(data, MySet.Usage, "Código de nivel incorrecto, el formato debe coincidir con XXX-YYY-ZZZ, caracteres alfanuméricos sin símbolos ni las letras I, O")

def ListLevels(data):
    if CountLevels() <= 0:
        SendResp(data, MySet.Usage, "No hay niveles en cola, añade el tuyo con " + MySet.command_add)
        return

    header = twitchLineBreak + " ------------------------------------ Cola de niveles --------------------------------------"
    body = ""
    lineNumber = 1

    try:
        with open(levelsFile, "r") as file:
            for line in file:
                body += "[" + str(lineNumber) + "] " + line.replace('\n','') + " " + twitchLineBreak
                lineNumber += 1

        SendResp(data, MySet.Usage, header + body)
    except:
        SendResp(data, MySet.Usage, "Error al intentar leer la lista de niveles, avisa a un mod")

def GetPositions(data):
    positions = ""

    try:
        with open(levelsFile, 'r') as f:
            levels = f.readlines()

        if len(levels) <= 0:
            SendResp(data, MySet.Usage, "No hay niveles en cola, añade el tuyo con " + MySet.command_add)
            return

        for i, level in enumerate(levels):
            if data.UserName in level:
                positions += " [" + str(i + 1) + "]"

        if positions != "":
            SendResp(data, MySet.Usage, "@" + data.UserName + " tienes niveles en las posiciones" + positions)
        else:
            SendResp(data, MySet.Usage, "@" + data.UserName + " no tienes niveles en cola")
    except:
        SendResp(data, MySet.Usage, "Error al intentar leer la lista de niveles, avisa a un mod")

def CountLevels():
    try:
        with open(levelsFile, 'r') as f:
            levels = f.readlines()

        return len(levels)
    except:
        return 0

def CountLevelsByUser(userName):
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
    try:
        with open(levelsFile, 'r') as f:
            level = f.readline().strip()

        if level == "":
            SendResp(data, MySet.Usage, "No hay niveles en cola, añade el tuyo con " + MySet.command_add)
        else:
            SendResp(data, MySet.Usage, level)
    except:
        SendResp(data, MySet.Usage, "Error al intentar leer la lista de niveles, avisa a un mod")

def NextLevel(data):
    try:
        with open(levelsFile, 'r') as f:
            levels = f.readlines()
            if len(levels) >= 2:
                level = levels[1].strip();
                if level != "":
                    SendResp(data, MySet.Usage, level)
                else:
                    SendResp(data, MySet.Usage, "No hay más niveles en cola, añade el tuyo con " + MySet.command_add)
            else:
                SendResp(data, MySet.Usage, "No hay más niveles en cola, añade el tuyo con " + MySet.command_add)
    except:
        SendResp(data, MySet.Usage, "Error al intentar leer la lista de niveles, avisa a un mod")

def FinishLevel(data, result):
    if result == 0:
        message = "¡Nivel superado!"
    else:
        message = "Nivel skipeado."

    try:
        with open(levelsFile, 'r') as f: #open in read / write mode
            levels = f.readlines()
            if len(levels) <= 0:
                SendResp(data, MySet.Usage, "No hay ningún nivel en juego")
                return

        with open(levelsFile, 'w') as f:
            del levels[0]
            f.writelines(levels)

            if len(levels) > 0:
                nextLevel = levels[0].strip()
                if nextLevel != "":
                    SendResp(data, MySet.Usage, message + " El siguiente nivel es " + levels[0])
                else:
                    SendResp(data, MySet.Usage, message + " No hay más niveles en cola, añade el tuyo con " + MySet.command_add)
            else:
                SendResp(data, MySet.Usage, message + " No hay más niveles en cola, añade el tuyo con " + MySet.command_add)
    except:
        SendResp(data, MySet.Usage, "Error al intentar modificar la lista de niveles, dale un golpe al bot")

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
        if data.GetParam(0).lower() == MySet.command_add.lower():
            levelCode = data.Message.replace(data.GetParam(0),'').strip().replace(' ','-').upper();
            AddLevel(levelCode, data)
            return
        elif data.GetParam(0).lower() == MySet.command_list.lower():
            ListLevels(data)
            return
        elif data.GetParam(0).lower() == MySet.command_position.lower():
            GetPositions(data)
            return
        elif data.GetParam(0).lower() == MySet.command_current_level.lower():
            CurrentLevel(data)
            return
        elif data.GetParam(0).lower() == MySet.command_next_level.lower():
            NextLevel(data)
            return
        elif data.GetParam(0).lower() == MySet.command_win_level.lower():
            FinishLevel(data, 0)
            return
        elif data.GetParam(0).lower() == MySet.command_skip_level.lower():
            FinishLevel(data, 1)
            return


def Tick():
    """Required tick function"""

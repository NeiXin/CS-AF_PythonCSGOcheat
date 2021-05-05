import time
import pymem
import pymem.process
import keyboard
import win32gui
import threading
import tkinter as tk
import math
import multiprocessing
from math import asin, atan2
from tkinter import *
from threading import Thread
from win32gui import GetWindowText, GetForegroundWindow
from tkinter import messagebox

# TO-DO #

# Add re-coil contrast for trigger bot
# Debug trigger bot crash error

# Account #
# crack9291

# APP #
def app_gui():

    print("""
DO NOT CLOSE THIS WINDOW!
    """)
    root = tk.Tk()
    root.title('CS:AF / CHEAT')
    title = Label(root, text="CS:AF / By; PackedUP")
    ver = Label(root, text="Version / 1.0 (20F2)")
    title.grid(row=0, column=0)
    ver.grid(row=1, column=0)
    
    run = tk.Button(root, text="INJECT", command=execute, fg="White", bg="#cc0099")
    run.grid(row=3, column=0)

    KILL = tk.Button(root, text="FORCE KILL (PROGRAM)", command=kill, fg="White", bg="#cc0099")
    KILL.grid(row=3, column=2)

    KILL = tk.Button(root, text="UN-INJECT", command=UTC, fg="White", bg="#cc0099")
    KILL.grid(row=2, column=0)
    


    root.mainloop()
dwEntityList = (0x4DA3F9C)
dwLocalPlayer = (0xD8C2BC)
m_iTeamNum = (0xF4)
dwGlowObjectManager = (0x52EC580)
m_iGlowIndex = (0xA438)





def aimbot():
    class Vector3:
        def __init__(self, x = 0.0, y = 0.0, z = 0.0):
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)

        def __add__(self, other):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        def __sub__(self, other):
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        def __mul__(self, scale):
            return Vector3(self.x * scale, self.y * scale, self.z * scale)
        def __str__(self):
            return f"(x: {str(self.x)}, y: {str(self.y)}, z: {str(self.z)})"
        def __repr__(self):
            return f"(x: {str(self.x)}, y: {str(self.y)}, z: {str(self.z)})"

        def distanceTo(self, other):
            delta = other - self; return ((delta.x ** 2) + (delta.y ** 2) + (delta.z ** 2))**(0.5)

    pm = pymem.Pymem()
    pm.open_process_from_name("csgo.exe")

    client = pymem.process.module_from_name(
                pm.process_handle,
                "client.dll"
    ).lpBaseOfDll
    engine = pymem.process.module_from_name(
                pm.process_handle,
                "engine.dll"
    ).lpBaseOfDll

    """ =============================================
    ::: Offsets needed, as they always change, sorry.
    ============================================= """
    offset = {
        "dwClientState_GetLocalPlayer" : (0x180),
        "dwEntityList"                 : (0x4DA3F9C),
        "dwLocalPlayer"                : (0xD8C2BC),
        "dwClientState"                : (0x588FE4),
        "dwClientState_ViewAngles"     : (0x4D90),
        "dwGlowObjectManager"          : (0x52EC580),
        "m_bDormant"                   : (0xED),

        "netvar"               : {
            "m_iTeamNum"       : (0xF4),
            "m_vecOrigin"      : (0x138),
            "m_dwBoneMatrix"   : (0x26A8),
            "m_vecViewOffset"  : (0x108),
            "m_iHealth"        : (0x100),
            "m_bSpottedByMask" : (0x980),
            "m_iGlowIndex"     : (0xA438),
        }
    }

    def getPlayer(index: int) -> int: 
        return pm.read_int(client + offset["dwEntityList"] + (index * 0x10))

    def getLocalPlayer() -> int:
        return pm.read_int(client + offset['dwLocalPlayer'])
    
    def getPlayerTeam(player: int) -> int:
        return pm.read_int(player + offset['netvar']['m_iTeamNum'])

    def getPlayerHealth(player: int) -> int:
        return pm.read_int(player + offset['netvar']['m_iHealth'])
    
    def isDormant(player: int) -> bool:
        return bool(pm.read_int(player + offset['m_bDormant']))

    def getGlowObjectManager() -> int:
        return pm.read_int(client + offset["dwGlowObjectManager"])

    def getPlayerGlowIndex(player: int) -> int:
        return pm.read_int(player + offset['netvar']["m_iGlowIndex"])

    def sameTeam(player: int) -> bool:
        return getPlayerTeam(player) == getPlayerTeam(getLocalPlayer())

    def isDead(player: int) -> bool:
        return getPlayerHealth(player) < 1 or getPlayerHealth(player) > 100

    def isVisible(player: int) -> bool:
        clientState = pm.read_int(engine + offset['dwClientState'])
        localPlayerId = pm.read_int(clientState + offset['dwClientState_GetLocalPlayer'])

        spottedByMask = pm.read_int(player + offset['netvar']['m_bSpottedByMask'])

        return spottedByMask & (1 << localPlayerId)

    def getPlayerLocation(player: int) -> Vector3:
        return Vector3(
            x = pm.read_float(player + offset['netvar']['m_vecOrigin'] + 0x0),
            y = pm.read_float(player + offset['netvar']['m_vecOrigin'] + 0x4),
            z = pm.read_float(player + offset['netvar']['m_vecOrigin'] + 0x8),
        )

    def getPlayerBoneLocation(player: int, bone: int) -> Vector3:
        boneMatrix = pm.read_int(player + offset['netvar']['m_dwBoneMatrix'])
        return Vector3(
            x = pm.read_float(boneMatrix + 0x30 * bone + 0x0C),
            y = pm.read_float(boneMatrix + 0x30 * bone + 0x1C),
            z = pm.read_float(boneMatrix + 0x30 * bone + 0x2C),
        )

    def getLocalPlayerViewOffset() -> Vector3:
        return Vector3(
            x = pm.read_float(getLocalPlayer() + offset['netvar']['m_vecViewOffset'] + 0x0),
            y = pm.read_float(getLocalPlayer() + offset['netvar']['m_vecViewOffset'] + 0x4),
            z = pm.read_float(getLocalPlayer() + offset['netvar']['m_vecViewOffset'] + 0x8),
        )

    def getLocalPlayerViewAngles() -> Vector3:
        clientState = pm.read_int(engine  + offset['dwClientState']); return Vector3(
            x = pm.read_float(clientState + offset['dwClientState_ViewAngles'] + 0x0),
            y = pm.read_float(clientState + offset['dwClientState_ViewAngles'] + 0x4),
            z = pm.read_float(clientState + offset['dwClientState_ViewAngles'] + 0x8),
        )

    def writeLocalPlayerViewAngles(x: float, y: float) -> None:
        if y >  180.0: y -= 360.0
        if y < -180.0: y += 360.0
        if x >   89.0: x -= 180.0
        if x <  -89.0: x += 180.0

        clientState = pm.read_int(engine + offset['dwClientState'])
        pm.write_float(clientState + offset['dwClientState_ViewAngles'] + 0x0, x)
        pm.write_float(clientState + offset['dwClientState_ViewAngles'] + 0x4, y)

    def forceLocalPlayerAimTo(target: Vector3) -> None:
        localPlayerHead = getPlayerLocation(getLocalPlayer()) + getLocalPlayerViewOffset()

        delta       = target - localPlayerHead
        deltaLength = localPlayerHead.distanceTo(target)

        writeLocalPlayerViewAngles(-asin(delta.z / deltaLength) * (180.0 / 3.14159235368979), 
                                   atan2(delta.y , delta.x    ) * (180.0 / 3.14159235368979))

    def glowPlayer(player: int) -> None:
        entityGlow  = getPlayerGlowIndex(player)
        glowManager = getGlowObjectManager()

        if sameTeam(player):
            pm.write_float(glowManager + entityGlow * 0x38 + 0x4 , float(0))
            pm.write_float(glowManager + entityGlow * 0x38 + 0x8 , float(0))
            pm.write_float(glowManager + entityGlow * 0x38 + 0xC , float(1))
            pm.write_float(glowManager + entityGlow * 0x38 + 0x10, float(1))
            pm.write_int  (glowManager + entityGlow * 0x38 + 0x24, int  (1))
        else:
            pm.write_float(glowManager + entityGlow * 0x38 + 0x4 , float(1))
            pm.write_float(glowManager + entityGlow * 0x38 + 0x8 , float(0))
            pm.write_float(glowManager + entityGlow * 0x38 + 0xC , float(0))
            pm.write_float(glowManager + entityGlow * 0x38 + 0x10, float(1))
            pm.write_int  (glowManager + entityGlow * 0x38 + 0x24, int  (1))

    def findClosestValidEnemy() -> bool or int:

        closestDistance      = 99999999.99
        closestDistanceIndex = -1

        for i in range(1, 32):
            entity = getPlayer(i)

            if not entity            : continue
            if not isVisible(entity) : continue

            if isDormant(entity)     : continue
            if isDead   (entity)     : continue
            if sameTeam (entity)     : continue

            currentDistance = getPlayerLocation(getLocalPlayer() ).distanceTo( getPlayerLocation(entity))
        
            if  currentDistance      < closestDistance:
                closestDistance      = currentDistance
                closestDistanceIndex = i

            return False if closestDistanceIndex == -1 else closestDistanceIndex

    def main():
        while True:
            if keyboard.is_pressed('end'): exit(0)

            #if keyboard.is_pressed('shift'):
            while True:
                entity = findClosestValidEnemy()

                if   entity:forceLocalPlayerAimTo(getPlayerBoneLocation(getPlayer(entity), bone = 8))

            for i in range(1, 32):
                entity = getPlayer(i)

                if   entity:glowPlayer(entity)

    if __name__ == '__main__' : main()

def ESP():
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

    while True:
        glow_manager = pm.read_int(client + dwGlowObjectManager)

        for i in range(1, 32):  # Entities 1-32 are reserved for players.
            entity = pm.read_int(client + dwEntityList + i * 0x10)

            if entity:
                entity_team_id = pm.read_int(entity + m_iTeamNum)
                entity_glow = pm.read_int(entity + m_iGlowIndex)

                if entity_team_id == 2:  # Terrorist
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(1))   # R 
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))   # G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))   # B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow

                elif entity_team_id == 3:  # Counter-terrorist
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0))   # R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))   # G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))   # B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow

def TB():
    dwForceAttack = (0x31D54DC)
    dwEntityList = (0x4DA3F9C)
    dwLocalPlayer = (0xD8C2BC)
    m_fFlags = (0x104)
    m_iCrosshairId = (0xB3E4)
    m_iTeamNum = (0xF4)

    #trigger_key = "c"
    
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

    #while True:
        #if not keyboard.is_pressed(trigger_key):
            #time.sleep(0.1)

        #if not GetWindowText(GetForegroundWindow()) == "Counter-Strike: Global Offensive":
            #continue

        #if keyboard.is_pressed(trigger_key):
    while True:
        player = pm.read_int(client + dwLocalPlayer)
        entity_id = pm.read_int(player + m_iCrosshairId)
        entity = pm.read_int(client + dwEntityList + (entity_id - 1) * 0x10)

        entity_team = pm.read_int(entity + m_iTeamNum)
        player_team = pm.read_int(player + m_iTeamNum)

        if entity_id > 0 and entity_id <= 64 and player_team != entity_team:
            pm.write_int(client + dwForceAttack, 6)
            time.sleep(0.006)
def BHOP():
    dwForceJump = (0x524DEDC)
    dwLocalPlayer = (0xD8C2BC)
    m_fFlags = (0x104)

    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

    while True:
        if not GetWindowText(GetForegroundWindow()) == "Counter-Strike: Global Offensive":
            continue

        if keyboard.is_pressed("space"):
            force_jump = client + dwForceJump
            player = pm.read_int(client + dwLocalPlayer)
            if player:
                on_ground = pm.read_int(player + m_fFlags)
                if on_ground and on_ground == 257:
                    pm.write_int(force_jump, 5)
                    time.sleep(0.08)
                    pm.write_int(force_jump, 4)

        time.sleep(0.002)

#def FOV():
    #dwEntityList = (0x4DA3F9C)
    #m_iDefaultFOV = (0x332C)

    #def main():
        #pm = pymem.Pymem("csgo.exe")
        #client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

        #while True:
            #player = pm.read_int(client + dwEntityList)
            #iFOV = pm.read_int(player + m_iDefaultFOV)
                
            #if keyboard.is_pressed("i"):
                #pm.write_int(player + m_iDefaultFOV, 140)
                #print("iFOV Set to: ", iFOV)
                #time.sleep(2)
                
            #if keyboard.is_pressed("o"):
                #pm.write_int(player + m_iDefaultFOV, 100)
                #print("iFOV Set to: ", iFOV)
                #time.sleep(2)
                
    #if __name__ == '__main__' : main()

def end():
        print("""
injected source code into process (csgo.exe) with 0 errors
Thank you for using CS:AF
        """)

def execute():
    if __name__ == '__main__':
        Thread(target = TB).start()
        Thread(target = ESP).start()
        Thread(target = BHOP).start()
        Thread(target = aimbot).start()
        Thread(target = end).start()
def UTC():
    proc = multiprocessing.Process(target=ESP, args=())
    proc.terminate()
def kill():
    quit()   
# ESP()
# TB()
app_gui()

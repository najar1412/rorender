import os
import sys, os.path, ctypes, ctypes.wintypes


def kill_process(process_name=None):
    # globals
    in_there = 0
    Psapi = ctypes.WinDLL('Psapi.dll')
    EnumProcesses = Psapi.EnumProcesses
    EnumProcesses.restype = ctypes.wintypes.BOOL
    GetProcessImageFileName = Psapi.GetProcessImageFileNameA
    GetProcessImageFileName.restype = ctypes.wintypes.DWORD

    Kernel32 = ctypes.WinDLL('kernel32.dll')
    OpenProcess = Kernel32.OpenProcess
    OpenProcess.restype = ctypes.wintypes.HANDLE
    TerminateProcess = Kernel32.TerminateProcess
    TerminateProcess.restype = ctypes.wintypes.BOOL
    CloseHandle = Kernel32.CloseHandle

    MAX_PATH = 260
    PROCESS_TERMINATE = 0x0001
    PROCESS_QUERY_INFORMATION = 0x0400

    count = 32

    while True:
        ProcessIds = (ctypes.wintypes.DWORD*count)()
        cb = ctypes.sizeof(ProcessIds)
        BytesReturned = ctypes.wintypes.DWORD()
        if EnumProcesses(ctypes.byref(ProcessIds), cb, ctypes.byref(BytesReturned)):
            if BytesReturned.value<cb:
                break
            else:
                count *= 2
        else:
            sys.exit("Call to EnumProcesses failed")

    for index in range(int(BytesReturned.value / ctypes.sizeof(ctypes.wintypes.DWORD))):
        ProcessId = ProcessIds[index]
        hProcess = OpenProcess(PROCESS_TERMINATE | PROCESS_QUERY_INFORMATION, False, ProcessId)
        if hProcess:
            ImageFileName = (ctypes.c_char*MAX_PATH)()
            if GetProcessImageFileName(hProcess, ImageFileName, MAX_PATH)>0:
                filename = str(os.path.basename(ImageFileName.value), 'utf-8')

                if filename == process_name:
                    TerminateProcess(hProcess, 1)
                    in_there = 1

            CloseHandle(hProcess)

    if in_there:
        return f'{process_name} terminated.'
    else:
        return f'terminating {process_name} failed.'


def load_vrayspawner(version=None):
    if version == None:
        os.chdir('C:\\Program Files\\Autodesk\\3ds Max 2017')
        os.system('"C:\\Program Files\\Autodesk\\3ds Max 2017\\vrayspawner2017.exe"')
        return True

    else:
        return False


def load_backburner_server(version=None):
    if version == None:
        os.chdir('C:\\Program Files (x86)\Autodesk\\Backburner')
        os.system('"C:\\Program Files (x86)\Autodesk\\Backburner\\server.exe"')
        return True

    else:
        return False

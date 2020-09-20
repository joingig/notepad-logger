from ctypes import windll, CFUNCTYPE, c_bool, c_wchar_p, create_string_buffer, byref
from ctypes.wintypes import HWND, LPARAM, DWORD, HANDLE, MAX_PATH
from sys import getsizeof
from os import path
from datetime import datetime

#msvcrt = cdll.msvcrt
#str_mess = "Hello from MSVCRT!\n"
#msvcrt.printf(str_mess)

#user32.dll  / user32.lib
EnumWindows = windll.user32.EnumWindows
GetWindowText = windll.user32.GetWindowTextA
GetWindowTextLength = windll.user32.GetWindowTextLengthA
GetWindowThreadProcessId = windll.user32.GetWindowThreadProcessId
IsWindowVisible = windll.user32.IsWindowVisible
FindWindowEx = windll.user32.FindWindowExW
SendMessage = windll.user32.SendMessageW
MessageBox = windll.user32.MessageBoxW
#psapi.dll  / psapi.lib
GetProcessImageFileName = windll.psapi.GetProcessImageFileNameA
#kernel32.dll / Kernel32.Lib
OpenProcess = windll.kernel32.OpenProcess
CloseHandle = windll.kernel32.CloseHandle
GetLastError = windll.kernel32.GetLastError

hwnd_note = None

def main():
    print(f"[**] windll.user32 {windll.user32}")
    print(f"[**] windll.psapi {windll.psapi}")
    print(f"[**] windll.kernel32 {windll.kernel32}")
    
    # looks like  note_h = hwnd_note 
    note_h = FindNotepad()
    # if not FindNotepad():
    #     print("Please run notepad.exe")
    # else:
    #     print(f"[**] Notepad window found with HWND {hex(note_h)}")
    #     nlog(note_h, 'log 1','log 2','log 3')
    print("Please run notepad.exe") if not FindNotepad() else nlog(note_h, 'log 1','log 2','log 3')
    return 0


def nlog(hwnd = None,*argv) -> None :
    EM_REPLACESEL = 0x00C2
    edit = HWND()

    #if hwnd == None:
    #    print("Please run notepad.exe")
    #    pass

    # HWND FindWindowExA(
    #     HWND   hWndParent,
    #     HWND   hWndChildAfter,
    #     LPCSTR lpszClass,
    #     LPCSTR lpszWindow
    # );

    edit_id = c_wchar_p('EDIT')
    edit = FindWindowEx(hwnd, None, edit_id, None)
    for arg in argv:
        log = '{} {} {}'.format(datetime.now().ctime(),arg,"\r\n")
        SendMessage(edit, EM_REPLACESEL, True, log)
    

def FindNotepad():
    
    # BOOL EnumWindows(
    #     WNDENUMPROC lpEnumFunc,
    #     LPARAM      lParam
    # );
       
    ENUMFUNC = CFUNCTYPE(c_bool, HWND, LPARAM)
    def EnumWindowsCallback(hwnd, lparam):
         
         global hwnd_note

         hh = c_wchar_p('EnumWindowsCallback')
         tt = c_wchar_p(f'hwnd {hwnd}')
         
        # int MessageBox(
        #   HWND    hWnd,
        #   LPCTSTR lpText,
        #   LPCTSTR lpCaption,
        #   UINT    uType
        # );
         #MessageBox(0,tt,hh,0x00000004 + 0x00000040)

        # int GetWindowTextA(
        #         HWND  hWnd,
        #         LPSTR lpString,
        #         int   nMaxCount
        # );
        
         length = GetWindowTextLength(hwnd) + 1
         buffer = create_string_buffer(length) 
         GetWindowText(hwnd,buffer,length)

        #  BOOL IsWindowVisible(
        #         HWND hWnd
        #  );
         if (IsWindowVisible(hwnd) and length != 0):

             #  DWORD GetWindowThreadProcessId(
             #     HWND    hWnd,
             #     LPDWORD lpdwProcessId
             #  );
             ProcessID = DWORD()
             GetWindowThreadProcessId(hwnd,byref(ProcessID))
                         
            # HANDLE OpenProcess(
            #     DWORD dwDesiredAccess,
            #     BOOL  bInheritHandle,
            #     DWORD dwProcessId
            # );
             PROCESS_ALL_ACCESS = 0x1fffff
             PROCESS_QUERY_INFORMATION = 0x0400
             PROCESS_VM_READ = 0x0010
             hProcess = HANDLE()
             hProcess = OpenProcess(PROCESS_QUERY_INFORMATION
                                    + PROCESS_VM_READ,
                                    False, 
                                    ProcessID.value)
             if (hProcess != 0):
                nameProc = create_string_buffer(MAX_PATH) 
                # DWORD GetProcessImageFileNameA(
                #         HANDLE hProcess,
                #         LPSTR  lpImageFileName,
                #         DWORD  nSize
                # );
                
                if (GetProcessImageFileName(hProcess, nameProc, getsizeof(nameProc)) != 0):
                    exe = path.split(nameProc.value)[1]
                    if exe == b'notepad.exe':
                        print(f'bingo notepad.exe found {exe}')
                        hwnd_note = hwnd
                else:
                    print(f'[**] Error GetProcessImageFileName {hProcess}')
                CloseHandle(hProcess)
             else:
                print(f"[**] GetLastError {GetLastError()}")
                print(f'[**] Error OpenProcess {buffer.value} PID {ProcessID.value}') 
        #return from EnumWindowsCallback
         return True

    EnumFunc = ENUMFUNC(EnumWindowsCallback)
    EnumWindows(EnumFunc,None)

    return hwnd_note

if __name__ == "__main__":
    main()



#https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messagebox
# MB_ABORTRETRYIGNORE 0x00000002L The message box contains three push buttons: Abort, Retry, and Ignore.
# MB_CANCELTRYCONTINUE 0x00000006L The message box contains three push buttons: Cancel, Try Again, Continue. Use this message box type instead of MB_ABORTRETRYIGNORE.
# MB_HELP 0x00004000L Adds a Help button to the message box. When the user clicks the Help button or presses F1, the system sends a WM_HELP message to the owner.
# MB_OK 0x00000000L The message box contains one push button: OK. This is the default.
# MB_OKCANCEL 0x00000001L The message box contains two push buttons: OK and Cancel.
# MB_RETRYCANCEL 0x00000005L The message box contains two push buttons: Retry and Cancel.
# MB_YESNO 0x00000004L The message box contains two push buttons: Yes and No.
# MB_YESNOCANCEL 0x00000003L The message box contains three push buttons: Yes, No, and Cancel.
 
# To display an icon in the message box, specify one of the following values.

# TABLE 2
# Value	Meaning
# MB_ICONEXCLAMATION 0x00000030L An exclamation-point icon appears in the message box.
# MB_ICONWARNING 0x00000030L An exclamation-point icon appears in the message box.
# MB_ICONINFORMATION 0x00000040L An icon consisting of a lowercase letter i in a circle appears in the message box.
# MB_ICONASTERISK 0x00000040L An icon consisting of a lowercase letter i in a circle appears in the message box.
# MB_ICONQUESTION 0x00000020L A question-mark icon appears in the message box. The question-mark message icon is no longer recommended because it does not clearly represent a specific type of message and because the phrasing of a message as a question could apply to any message type. In addition, users can confuse the message symbol question mark with Help information. Therefore, do not use this question mark message symbol in your message boxes. The system continues to support its inclusion only for backward compatibility.
# MB_ICONSTOP 0x00000010L A stop-sign icon appears in the message box.
# MB_ICONERROR 0x00000010L A stop-sign icon appears in the message box.
# MB_ICONHAND 0x00000010L A stop-sign icon appears in the message box.
 
# To indicate the default button, specify one of the following values.

# TABLE 3
# Value	Meaning
# MB_DEFBUTTON1 0x00000000L The first button is the default button.
# MB_DEFBUTTON1 is the default unless MB_DEFBUTTON2, MB_DEFBUTTON3, or MB_DEFBUTTON4 is specified.

# MB_DEFBUTTON2 0x00000100L The second button is the default button.
# MB_DEFBUTTON3 0x00000200L The third button is the default button.
# MB_DEFBUTTON4 0x00000300L The fourth button is the default button.
 
# To indicate the modality of the dialog box, specify one of the following values.

# TABLE 4
# Value	Meaning
# MB_APPLMODAL 0x00000000L The user must respond to the message box before continuing work in the window identified by the hWnd parameter. However, the user can move to the windows of other threads and work in those windows.
# Depending on the hierarchy of windows in the application, the user may be able to move to other windows within the thread. All child windows of the parent of the message box are automatically disabled, but pop-up windows are not.

# MB_APPLMODAL is the default if neither MB_SYSTEMMODAL nor MB_TASKMODAL is specified.

# MB_SYSTEMMODAL 0x00001000L Same as MB_APPLMODAL except that the message box has the WS_EX_TOPMOST style. Use system-modal message boxes to notify the user of serious, potentially damaging errors that require immediate attention (for example, running out of memory). This flag has no effect on the user's ability to interact with windows other than those associated with hWnd.
# MB_TASKMODAL 0x00002000L Same as MB_APPLMODAL except that all the top-level windows belonging to the current thread are disabled if the hWnd parameter is NULL. Use this flag when the calling application or library does not have a window handle available but still needs to prevent input to other windows in the calling thread without suspending other threads.
 
# To specify other options, use one or more of the following values.
# TABLE 5
# Value	Meaning
# MB_DEFAULT_DESKTOP_ONLY 0x00020000L
# Same as desktop of the interactive window station. For more information, see Window Stations.
# If the current input desktop is not the default desktop, MessageBox does not return until the user switches to the default desktop.

# MB_RIGHT 0x00080000L The text is right-justified. 
# MB_RTLREADING 0x00100000L Displays message and caption text using right-to-left reading order on Hebrew and Arabic systems.
# MB_SETFOREGROUND 0x00010000L The message box becomes the foreground window. Internally, the system calls the SetForegroundWindow function for the message box.
# MB_TOPMOST 0x00040000L The message box is created with the WS_EX_TOPMOST window style.
# MB_SERVICE_NOTIFICATION 0x00200000L The caller is a service notifying the user of an event. The function displays a message box on the current active desktop, even if there is no user logged on to the computer.
# Terminal Services: If the calling thread has an impersonation token, the function directs the message box to the session specified in the impersonation token.

# If this flag is set, the hWnd parameter must be NULL. This is so that the message box can appear on a desktop other than the desktop corresponding to the hWnd.
# For information on security considerations in regard to using this flag, see Interactive Services. In particular, be aware that this flag can produce interactive content on a locked desktop and should therefore be used for only a very limited set of scenarios, such as resource exhaustion.

#http://www.codenet.ru/progr/bcb/Handle-Types.php
#HWND == HANDLE == c_void_p
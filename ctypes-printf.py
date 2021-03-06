from ctypes import *
from ctypes.wintypes import *
from sys import getsizeof
from os import path

#msvcrt = cdll.msvcrt
#str_mess = "Hello from MSVCRT!\n"
#msvcrt.printf(str_mess)


#class barley_amount(Union):
#    _fields_ = [
#        ("long", c_long),
#        ("int", c_int),
#        ("char", c_char * 8)
#    ]
#value = input("Enter the amount of barley:")
#my_barley = barley_amount(15)
#print(f"barley amount as a long: {my_barley.long}")
#print(f"barley amount as a int: {my_barley.int}")
#print(f"barley amount as a char: {my_barley.char}")

#user32.dll  / User32.Lib
#FindWindowEx(hNotepad, NULL, "EDIT", NULL);
#SendMessage(edit, EM_REPLACESEL, TRUE, (LPARAM)buf_date);
#enumWindowCallback(HWND hWnd, LPARAM lparam)
#GetWindowText(hWnd, buffer, length + 1);
#GetWindowThreadProcessId(hWnd,&ProcessId);
#EnumWindows



def main():
    print(f"[**] windll.user32 {windll.user32}")
    print(f"[**] windll.psapi {windll.psapi}")
    print(f"[**] windll.kernel32 {windll.kernel32}")
    
    #user32.dll  / user32.lib
    EnumWindows = windll.user32.EnumWindows
    GetWindowText = windll.user32.GetWindowTextA
    GetWindowTextLength = windll.user32.GetWindowTextLengthA
    GetWindowThreadProcessId = windll.user32.GetWindowThreadProcessId
    IsWindowVisible = windll.user32.IsWindowVisible
    FindWindowEx = windll.user32.FindWindowExA
    SendMessage = windll.user32.SendMessageW
    MessageBox = windll.user32.MessageBoxW
    #psapi.dll  / psapi.lib
    GetProcessImageFileName = windll.psapi.GetProcessImageFileNameA
    #kernel32.dll / Kernel32.Lib
    OpenProcess = windll.kernel32.OpenProcess
    CloseHandle = windll.kernel32.CloseHandle
    GetLastError = windll.kernel32.GetLastError


    # int MessageBox(
    #   HWND    hWnd,
    #   LPCTSTR lpText,
    #   LPCTSTR lpCaption,
    #   UINT    uType
    # );

    # BOOL EnumWindows(
    #     WNDENUMPROC lpEnumFunc,
    #     LPARAM      lParam
    # );

       
    #HWND = c_void_p   # classic hwnd = handle
    #HANDLE = c_void_p
    #LPARAM = POINTER(c_long)

    ENUMFUNC = CFUNCTYPE(c_bool, HWND, LPARAM)
    def EnumWindowsCallback(hwnd, lparam):
         #print(f'[*] hwnd {hwnd} lparam {lparam}')
         tt = c_wchar_p('Test text')
         hh = c_wchar_p('Header')
         #MessageBox(0,tt,hh,0x00000004 + 0x00000040)

        # int GetWindowTextA(
        #         HWND  hWnd,
        #         LPSTR lpString,
        #         int   nMaxCount
        # );
        #GetWindowText(hwnd, buffer, length + 1);

         length = GetWindowTextLength(hwnd) + 1
         #print(f'[**] GetWindowTextLength {length}')
         buffer = create_string_buffer(length) 
         GetWindowText(hwnd,buffer,length)
         #print(f'[**] GetWindowText {buffer.value}')

        #  BOOL IsWindowVisible(
        #         HWND hWnd
        #  );
         if (IsWindowVisible(hwnd) and length != 0):
             print(f'[*] hwnd {hwnd} hwnd hex {hex(hwnd)}')
             print(f'[**] GetWindowText {buffer.value}')
             #  DWORD GetWindowThreadProcessId(
             #     HWND    hWnd,
             #     LPDWORD lpdwProcessId
             #  );
             ProcessID = DWORD()
             #print(f'ProcessID2 {type(ProcessID2)} ')
             #ProcessID = GetWindowThreadProcessId(hwnd,None)
             GetWindowThreadProcessId(hwnd,byref(ProcessID))

             print(f'[**] GetWindowThreadProcessId {ProcessID.value}')
             #print(f'[**] ProcessID type {type(ProcessID)}')

            # HANDLE OpenProcess(
            #     DWORD dwDesiredAccess,
            #     BOOL  bInheritHandle,
            #     DWORD dwProcessId
            # );
             PROCESS_ALL_ACCESS = 0x1fffff
             PROCESS_QUERY_INFORMATION = 0x0400
             PROCESS_VM_READ = 0x0010
             hProcess = HANDLE()
             hProcess = OpenProcess(PROCESS_QUERY_INFORMATION +
                            PROCESS_VM_READ,
                            False, 
                            ProcessID.value)
             if (hProcess != 0):
                print(f'[**] ok pid {ProcessID.value} opened, hProcess {hProcess}')
                nameProc = create_string_buffer(MAX_PATH) 
                # DWORD GetProcessImageFileNameA(
                #         HANDLE hProcess,
                #         LPSTR  lpImageFileName,
                #         DWORD  nSize
                # );
                
                if (GetProcessImageFileName(hProcess, nameProc, getsizeof(nameProc)) != 0):
                    print(f'[**] GetProcessImageFileName {nameProc.value}')
                    exe = path.split(nameProc.value)[1]
                    if exe == b'notepad.exe':
                        print(f'bingo notepad.exe found {exe}')
                else:
                    print(f'[**] Error GetProcessImageFileName {hProcess}')
                CloseHandle(hProcess)
             else:
                print(f"[**] GetLastError {GetLastError()}")
                print(f'[**] Error open PID {ProcessID.value}') 

         return True
    
    EnumFunc = ENUMFUNC(EnumWindowsCallback)
    EnumWindows(EnumFunc,None)



    return 0


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
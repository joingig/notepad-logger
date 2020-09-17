from ctypes import *
msvcrt = cdll.msvcrt
str_mess = "Hello from MSVCRT!\n"
msvcrt.printf(str_mess)


class barley_amount(Union):
    _fields_ = [
        ("long", c_long),
        ("int", c_int),
        ("char", c_char * 8)
    ]
value = input("Enter the amount of barley:")
my_barley = barley_amount(int(value))
print(f"barley amount as a long: {my_barley.long}")
print(f"barley amount as a int: {my_barley.int}")
print(f"barley amount as a char: {my_barley.char}")

#user32.dll
#FindWindowEx(hNotepad, NULL, "EDIT", NULL);
#SendMessage(edit, EM_REPLACESEL, TRUE, (LPARAM)buf_date);
#enumWindowCallback(HWND hWnd, LPARAM lparam)
#GetWindowText(hWnd, buffer, length + 1);
#GetWindowThreadProcessId(hWnd,&ProcessId);
#EnumWindows

#psapi.dll
#GetProcessImageFileName


#kernel32.dll
#OpenProcess

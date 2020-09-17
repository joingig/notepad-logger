# notepad-logger

Long, long time ago on Reddit
![reddit](notepad_log.jpeg)

But, when i try
```C
    notepad = FindWindow(NULL,"Безымянный — Блокнот");
```
i get null. Well well, look like there is no short cuts.

Logger find 
- all visible windows ( EnumWindows )
  - get parent process pid ( GetWindowThreadProcessId )
  - get process name ( GetProcessImageFileName )
  - if (strcmp(nameFile,"notepad") got it!
  - use hwnd / pid to send message to notepad (notepad.exe)


Dirty logger to windows notepad.

# notepad-logger

Long, long time ago on Reddit
![reddit](notepad_log.jpeg)

But, when i try
```C
    notepad = FindWindow(NULL,"Безымянный — Блокнот");
```
i get null. Well well, look like there is no short cuts.

to find notepad.exe:
- find all visible windows ( EnumWindows )
  - get parent process pid ( GetWindowThreadProcessId )
  - get process name ( GetProcessImageFileName )
  - if (strcmp(nameFile,"notepad") got it!
  - use hwnd / pid to send message to notepad (notepad.exe)


In [note_logger00.cpp](note_logger00.cpp) i implemented this dirty logger.

In [note_logger00.py](note_logger00.py) clear python implementation notepad logger (temporary with havy comments).

#include <windows.h>
#include <stdarg.h>
#include <WinUser.h>
#include <iostream>
#include <psapi.h>
#include <ctime>

static void nlog(HWND hNotepad,char *str,...){
    HWND edit = NULL;
    va_list ap;
    char buf[250] = {0};
    char buf_date[250] = {0};

    va_start(ap, str);
//    vsprintf_s(buf, 250, str, ap);  #Modern C
    vsprintf(buf, str, ap);
    va_end(ap);
    strcat(buf,"\r\n");
        
    //notepad = FindWindow(NULL,"Безымянный — Блокнот");
    //std::cout << "[**] notepad HWND:" << notepad << std::endl;
    //if(notepad == NULL) {
    //    std::cout << "no notepad found";
    //}

    time_t now = time(0);
    char* dt = ctime(&now);
    
    sprintf(buf_date,"%s %s",dt,buf);

    edit = FindWindowEx(hNotepad, NULL, "EDIT", NULL);
    SendMessage(edit, EM_REPLACESEL, TRUE, (LPARAM)buf_date);

}

HWND npad = NULL;

static BOOL CALLBACK enumWindowCallback(HWND hWnd, LPARAM lparam) {
    int length = GetWindowTextLength(hWnd);
    char* buffer = new char[length + 1];
    DWORD ProcessId = 0;
    GetWindowText(hWnd, buffer, length + 1);
    std::string windowTitle(buffer);
    GetWindowThreadProcessId(hWnd,&ProcessId);

    // List visible windows with a non-empty title
    if (IsWindowVisible(hWnd) && length != 0) {
        //std::cout << hWnd << ":  " << windowTitle << std::endl;
        std::wcout << hWnd << ":" << buffer << std::endl;
        std::wcout << ProcessId << ": pid" << std::endl;

        HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS | PROCESS_QUERY_INFORMATION |
                            PROCESS_VM_READ,
                            FALSE, ProcessId);
        if (NULL != hProcess) {
        std::cout << "hProcess " << hProcess << std::endl;
        TCHAR nameProc[1024];
        TCHAR nameFile[1024];
        if (GetProcessImageFileName(hProcess, nameProc, sizeof(nameProc) / sizeof( * nameProc)) == 0) {
            std::cout << "GetProcessImageFileName Error";
        } else {
      	    _splitpath_s(nameProc, NULL, NULL, NULL, NULL, nameFile, sizeof(nameFile), NULL, NULL);
            std::wcout << "nameProcess " << nameProc << std::endl;
            std::wcout << "nameFile " << nameFile << std::endl;
            if (strcmp(nameFile,"notepad") == 0){
                std::wcout << "[**] notepad found" << std::endl;
                npad = hWnd;
            }
	    }
        } else {
            printf("OpenProcess(%i) failed, error: %i\n",
            ProcessId, (int) GetLastError());
        }

    }
    return TRUE;
}


int main(){

    std::cout << "[**] Notepad logger 0.3v" << std::endl;
    //FindNotepad(); Find notepad window by process name
    EnumWindows(enumWindowCallback, NULL);
    if(!npad){
        std::wcout << "[**] notepad not found." << std::endl;
        return 0;
    }
    nlog(npad, "ch ch pidser!");
    return 0;
}


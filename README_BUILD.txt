========================================
  PREMIUM TIMER APP — Build Instructions
========================================

1. INSTALIRAJ pyinstaller
----------------------------
   U terminalu ili CMD:

   pip install pyinstaller


2. NAPRAVI .EXE FAJL
----------------------
   Pozicioniraj se u folder gdje je timer_app.py:

   cd C:\Users\Sedin\Desktop\TimerApp

   Pa pokreni:

   pyinstaller --onefile --noconsole --name "TimerApp" timer_app.py


3. PRONAĐI GOTOV .EXE
-----------------------
   Gotov fajl je u:

   dist/TimerApp.exe

   Prekopiraj ga u root folder (pored README-a):

   copy dist\TimerApp.exe .


4. ZAPAKUJ ZA KLIJENTA
------------------------
   Napravi ZIP sa:
   - TimerApp.exe
   - README_BUILD.txt (ove instrukcije)

   Klijent samo pokrene .exe, nema potrebe za Python.


========================================
  Za testiranje (prije build-a):
  python timer_app.py
========================================

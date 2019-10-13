rem set wd
cd "C:\Users\steve\Documents\apps\mame-ai"

rem update pip
call pip install -U pip

rem install virtualenv
call pip install virtualenv

rem setup virtual env
rem virtualenv --system-site-packages -p py ./venv  

rem activate it
rem call .\venv\Scripts\activate

rem add tensor flow
call pip install --upgrade tensorflow==2.0.0

rem screenshot library
call python -m pip install -U --user mss

rem numpy
call pip install numpy

call pip install ImageHash

rem open cv
pip install opencv-python

rem auto gui (send mouse and keyboard events)
python -m pip install pyautogui

rem show me what I got
pip list

pause
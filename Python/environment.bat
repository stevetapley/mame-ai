rem set wd
cd "C:\Users\steve\Documents\apps\mame-ai"

rem update pip
pip install -U pip

rem setup virtual env
virtualenv --system-site-packages -p py ./venv  

rem activate it
.\venv\Scripts\activate

rem add tensor flow
pip install --upgrade tensorflow==2.0.0-rc0

rem screenshot library
python -m pip install -U --user mss

rem numpy
pip install numpy

rem open cv
pip install opencv-python

rem auto gui (send mouse and keyboard events)
python -m pip install pyautogui

rem show me what I got
pip list
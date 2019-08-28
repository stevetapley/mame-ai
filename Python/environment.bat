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

rem show me what I got
pip list
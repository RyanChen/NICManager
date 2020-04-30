# NICManager
## How to run in develop environment (Windows)
1. Activate your virtual environemt
```
> virtualenv venv
```
2. Install requirements
```
(venv) > pip install -r requirements.txt
```
3. Run main.py
```
(venv) > python main.py
```

## How to pack to an application
1. Install Pyinstaller
```
(venv) > pip install Pyinstaller
```
2. Pack application with .spec file (remember to modify `pathex` path in .spec to your `project_root`)
```
(venv) > pyinstaller.exe --onefile main.spec
```
You can generate .spec by following command and then add the lost of `/ui/` folder 
(Add a.datas += Tree('./ui', prefix='ui') in .spec file)
```
(venv) > pyinstaller.exe --onefile --add-data="icon.ico;." --add-data="config.json;." -i icon.ico --clean --noconsole main.py
```
3. Your executable application file will generate at `project_root/dist/`

## Features
In this simple tool:
1. [Tab:Networl Card] Check your Network interface Card (NIC) status. (If strikethrough that means you do not have this NIC on your computer)
2. [Tab:Networl Card] Check or uncheck the checkbox to enable/disable the network interface.
3. [Tab:Wifi Setting] Set your hotspot SSID and Password.
4. [Tab:Wifi Setting] Start / Stop your wifi hotspot.
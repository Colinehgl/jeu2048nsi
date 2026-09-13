@echo off
REM Ce script installe pyinstaller puis construit un .exe du jeu 2048.
REM A lancer sur une machine Windows qui a Python installe (avec tkinter,
REM inclus par defaut dans Python sous Windows).
REM Il faut que jeu2048.py et interface2048.py soient dans le meme dossier
REM que ce fichier .bat.

echo Installation de pyinstaller...
pip install pyinstaller

echo.
echo Construction du .exe...
pyinstaller --onefile --windowed --name jeu2048 interface2048.py

echo.
echo Termine ! Le fichier jeu2048.exe se trouve dans le dossier "dist".
pause
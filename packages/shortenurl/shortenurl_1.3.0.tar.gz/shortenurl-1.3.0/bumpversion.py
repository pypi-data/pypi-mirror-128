import os

currentVersion = str(input("Current version: "))

os.system("bumpversion --current-version " + currentVersion + " minor setup.py __init__.py")
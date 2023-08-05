import os

os.system("twine upload dist/*")
print("Finished")
input("Press Enter or Ctrl+Z to close")
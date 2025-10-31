import subprocess
import sys

python_path = sys.executable

subprocess.run([python_path, "script/script2.py"])
subprocess.run([python_path, "script/script.py"])
subprocess.run([python_path, "script/script3.py"])
subprocess.run([python_path, "script/script4.py"])
subprocess.run([python_path, "script/script5.py"])
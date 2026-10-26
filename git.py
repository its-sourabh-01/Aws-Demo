#run script for git add,commit and push
import subprocess

subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "Automated commit"])
subprocess.run(["git", "push"]) 
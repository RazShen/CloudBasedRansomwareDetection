import subprocess
kp = subprocess.Popen(["ps", "-ef"], stdout=subprocess.PIPE)
grep = subprocess.Popen(["grep", "cuckoo"], stdin=kp.stdout, stdout=subprocess.PIPE)
awk = subprocess.Popen(["awk", "{print $2}"], stdin=grep.stdout, stdout=subprocess.PIPE)
kill = subprocess.Popen(["xargs", "kill"], stdin=awk.stdout, stdout=subprocess.PIPE)
kp.stdout.close()
grep.stdout.close()
awk.stdout.close()
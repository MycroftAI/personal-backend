import os, subprocess, signal

try:
    p = subprocess.run("python3 start_backend.py & python3 start_frontend.py", shell=True)
except (KeyboardInterrupt, SystemExit):
    print("Exiting...")
    
    p = subprocess.Popen(['ps', '-s'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        line = line.decode("utf-8")
        line = line.strip()
        line = line.split("  ", 1)[1]
        #print(str(line))
        try:
            if 'start_backend.py' in str(line):
                pid = int(line.split(None, 1)[0])
                #print("pid = " + str(pid))
                os.kill(pid, signal.SIGKILL)
            if 'start_frontend.py' in str(line):
                pid = int(line.split(None, 1)[0])
                #print("pid = " + str(pid))
                os.kill(pid, signal.SIGKILL)
        except:
            print("error killing process")
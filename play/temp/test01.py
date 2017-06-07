from multiprocessing import Process
from subprocess import Popen, PIPE
from ptpython.repl import embed
import os, signal
import time

def thepro(num):
    #cmd = [ 'while', 'true;', 'do', 'sleep', str(num)+';', 'echo', '"what";', 'done' ]
    cmd = [ 'sleep', str(num) ]
    #cmd = [ 'recordmydesktop', '--windowid', '0x3800d26']
    encoder = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    while True:
        if encoder.poll() == 0:
            print "it's been done well."
            break;
        elif encoder.poll() == 1:
            print "it's been gone wrong."
            break;
        else:
            time.sleep(1)

p1 = Process(target=thepro, args=(30,))
embed(globals(), locals())

# p1.start()
# os.kill(p1.pid, signal.SIGKILL)
# os.kill(25028, signal.SIGKILL)
# p1.terminate()
# p = Process(target=thepro, args=(1,))
#
#
#
#
# p.join()

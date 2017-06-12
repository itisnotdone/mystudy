import os, time
import re
from ptpython.repl import embed
from subprocess import Popen, PIPE
#http://stackoverflow.com/questions/14796323/input-using-backspace-and-arrow-keys
import readline #It automatically wraps stdin.
import sys, select

def check_dir(dir):
    if not os.path.exists(dir):
        print "Creating "+dir+" directory.."
        os.makedirs(dir)

def want_to_redo():
    print "If you want to redo it, enter 'y'. Waiting for 10 seconds.."
    i, o, e = select.select( [sys.stdin], [], [], 10 )
    if (i):
        answer = sys.stdin.readline().strip()
        print "You said", answer
        if answer == 'y':
            return True
        else:
            return False

def record(temp_dir, file_path, layout):
    cmd = [ 'recordmydesktop',
           '-x', layout['xx'],
           '-y', layout['yy'],
           '--width', layout['wid'],
           '--height', layout['hei'],
           '--fps', '15',
           '--channels', '2',
           '--freq', '22050',
           '--device', 'default',
           '--v_quality', '63',
           '--s_quality', '10',
           '--workdir', temp_dir,
           '-o', file_path ]
    recoder = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return recoder

def encode_all_in_one(file, path):
    cmd = 'recordmydesktop --rescue '+path
    encoder = Popen(cmd, shell=True, executable="/bin/bash", stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return encoder

def get_urls():
    file = 'to_record.urls'
    with open(file) as f:
            lines = f.read().splitlines()

def string_handler(string):
    if isinstance(string, unicode):
        result = string.encode('utf-8')
    else:
        result = string
    result = result.lower()
    result = re.sub(': |/|, |;| - |-| |\(|\)', '_', result)
    result = re.sub("\?|'|\.|\$'", '', result)
    result = re.sub('&', '_and_', result)
    return result

#other = { 'xx': '12', 'yy': '450', 'wid': '1482', 'hei': '820' }   # other

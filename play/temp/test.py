# -*- coding: utf-8 -*-
import sys, select
from ptpython.repl import embed

print "If you want to redo it, enter 'y'."
i, o, e = select.select( [sys.stdin], [], [], 10 )
if (i):
    answer = sys.stdin.readline().strip()
    print "You said", answer
    if answer == 'y':
        blahblah

else:
    print "You said nothing!"
embed(globals(), locals())

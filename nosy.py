#!/usr/bin/env python
# By Jeff Winkler, http://jeffwinkler.net
# By Jerome Lacoste, jerome@coffeebreaks.org

import glob,os,stat,time,os.path
import pynotify

pwd = os.path.abspath(".")

paths = glob.glob ('*.txt') + glob.glob ('data/*.txt') + glob.glob ('*.py') + glob.glob ('tests/*.py') + glob.glob ('*.kid')

'''
Watch for changes in all .py files. If changes, run nosetests. 
'''
def checkSum():
    ''' Return a long which can be used to know if any files from the paths variable have changed.'''
    val = 0

    for f in paths:
        stats = os.stat (f)
        val += stats [stat.ST_SIZE] + stats [stat.ST_MTIME]

    return val

def notify(msg1,msg2):
    if not pynotify.init("Markup"):
        return
    n = pynotify.Notification(msg1, msg2)
    if not n.show():
        print "Failed to send notification"

def notifyFailure():
    notify(os.path.basename(pwd) + " build failed.", pwd + ": nosetests failed")

def notifySuccess():
    notify(os.path.basename(pwd) + " build successfull.", pwd + ": nosetests success")

def run():
  val=0
  oldRes = 0
  firstBuild = True
  while (True):
    keepOnNotifyingFailures = True
    if checkSum() != val:
      val=checkSum()
      res = os.system ('nosetests')
#        print "res:" + str(res)
      if (res != 0):
        if (oldRes == 0 or keepOnNotifyingFailures):
          notifyFailure()
      else:
        if (oldRes != 0 or firstBuild):
          notifySuccess()
      firstBuild = False
  time.sleep(1)
  oldRes = res

if __name__ == '__main__':
  run()

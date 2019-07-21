
import sys
# TODO this is still hacky and makes no sense obviously
sys.path.append('../libresign')
import unoremote

control = Libo()
uno = unoremote.UNOClient(control)
uno.start(True)


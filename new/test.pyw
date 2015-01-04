from tkinter import *
from mssgboxes import *
from download import *
import threading
root=Tk()
root.title('pyDM')
temp=[]
obj=SOMEMSG(root,'Enter URL',temp)
root.withdraw()
root.wait_window(obj.top)
uri=temp[0]

temp=[]
obj=SOMEMSG(root,'Save as ?',temp)

root.wait_window(obj.top)
name=temp[0]

t=threading.Thread(target=interact,args=(uri,name))
t.start()
t.join()
root.destroy()

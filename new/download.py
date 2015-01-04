import urllib.request
import sys
import os
import time
import threading
from tkinter import *
re=None
nocompl=0
notr=7
def guiclt(goturi,gotname):
    def myexit():
        pass
    try:
        root=Tk()
        root.title('downloader')
        root.protocol("WM_DELETE_WINDOW", myexit)
        ##    info=Text(root,height=15,width=30,state=DISABLED)
        ##    info.pack()
        lab=Label(root,text="Wait...",fg="red")
        per=Label(root,text="Please Wait..",fg="blue")
        
        lab.pack()
        per.pack()
        

        def printgui(text,k):
            text=text
            k['text']=text
            print(text)
        def reqfunc(a,b):
            global re
            re=urllib.request.Request(a)
        class downloadfile:
            def __init__(self,uri):
                self.maxi=10
                i=0
                self.error=False
                self.size=0
                self.filename=''
                self.parts={}
                self.chunk=0
                self.uri=uri
                printgui("Connecting..",lab)
                while i<self.maxi:
                    try:
                        self.url=urllib.request.urlopen(uri)
                    except:
                        i=i+1
                        print(i)
                        continue
                    break
                if i==self.maxi:
                    printgui("Umm something unexpected happened!:/",lab)
                    self.error=True
                    return
                printgui("Connected",lab)

            def namesize(self,tempn):
               # self.filename=input("Save as ? \n")
                global notr
                self.filename=tempn
                try:
                    self.size=int(self.url.getheader('Content-Length',None))
                except:

                    printgui("No file found here!._.",lab)
                    self.error=True
                    return
                self.chunk=int(self.size/notr)
            def downl(self,start,randomargument):
                req=None
                global re
                i=0
                req=re
                while i<self.maxi:
                    try:
                        req.headers['Range']='bytes=%s-%s'% (start,start+self.chunk)
                    except:
                        i=i+1
                        continue
                    break
                if i==self.maxi:
                    printgui("Bad Header!:/",lab)
                    self.error=True
                    return
                i=0
                while i<self.maxi:
                    try:
                        f=urllib.request.urlopen(req)
                    except:
                        i=i+1
                        continue
                    break
                if i==self.maxi:
                    printgui("No response!:/",lab)
                    self.error=True
                    return
                self.parts[start]=f.read()
                global nocompl,notr
                nocompl=nocompl+1
                printgui(str(nocompl*100/notr)+" completed! :D",per)
                return
            def er(self):
                return self.error
            def savefile(self):
                f=open(self.filename,"wb")
                ch=''
                i=1
                while ch!=None:
                    k=i*self.chunk
                    if k in self.parts:
                        ch=self.parts[i*self.chunk]
                        self.parts[0]=self.parts[0]+self.parts[i*self.chunk]
                        i=i+1
                    else:
                        break
                f.write(self.parts[0])
                f.close()
                printgui('size- '+str(os.path.getsize(self.filename)),lab)
            def schnk(self):
                return self.chunk
                
        def downsome(uri,tempna):
              
            temp=threading.Thread(target=reqfunc,args=(uri,"random"))
            temp.start()
            code='404'
            d=downloadfile(uri)
            threads=[]
            if d.er():
                printgui("Try again later!:/",lab)
                return code
            
            d.namesize(tempna)
            if d.er():
                printgui("Try again later!:/",lab)
                return code
            temp.join()
            starttime=time.time()
            global notr
            for i in range(0,notr):
                t=threading.Thread(target=d.downl,args=(i*d.schnk(),"RANDOM"))
                t.start()
                printgui("started"+str(i),per)
                threads.append(t)
            printgui("0% Completed :/",per)
            for i in threads:
                i.join()
                root.protocol("WM_DELETE_WINDOW", root.destroy)
            endtime=time.time()
            if d.er():
                printgui("Try again later!:/",lab)
                return code
            d.savefile()
            time.sleep(2)
            printgui("Time Taken-"+str(endtime-starttime),per)
            time.sleep(2)
            root.destroy()
            return '400'
        stop_threads = False
        t=threading.Thread(target=downsome,args=(goturi,gotname)  )
        t.start()
            
        root.mainloop()
    except:
        print('ERROR')

def interact(u,n):
    guiclt(u,n)

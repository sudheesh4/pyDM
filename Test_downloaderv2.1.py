import urllib.request
import urllib.parse
import sys
import random
import os
import time 
import threading
    
uri=input("Enter url\n")
i=0
maxi=10
re=None
def reqthre(a,b):
    global re
    re=urllib.request.Request(uri)
    
tempr = threading.Thread(target=reqthre,args=("requeststuff","justrandom"))
tempr.start()
while i<maxi:
    try:
        url = urllib.request.urlopen(uri)
        
    except:
        i=i+1
        continue
    break
if i==maxi:
    print("Umm something unexpected happened :/ Aborting!")
    exit()
print("Connected!")


def namesize():
    met=url.info()#meta tag info;for fun :P
    try:
        size=int(url.getheader('Content-Length',None))#content-length - number of bytes in body of file;stored in header
    except:
        print("It seems that there is no file here!._. Aborting!")
        exit()
    filename=input("Save as ? ")
##    i=0
##    temp=url.getheader('Content-Disposition')#works with git site only
##    for c in temp:
##        if c=='=':
##            break
##        i=i+1
##    filename=temp[i+1:]
##    print(filename)
##    filename="random.png"
    return [filename,size]
details=namesize()

threads = []
parts = {}
chunk_size = 8192
# Initialize threads
k=details[1]
notr_list=[11,7,13,19,17,23,21]
random.shuffle(notr_list)

notr=notr_list[random.randint(0,6)]#no of thread
notr=5
chunk_size=k/notr

nodo=0#no of chunks done ; to monitor speed
#chunk_size=(k/20)
def monitor_speed():
    global nodo
    nodo+=1
    percen=int((nodo/notr)*100)
    if percen > 100:
        print("Downloaded!")
    else:
        print(str(percen-1) + "% Downloaded\n")
    
        
def download(start,sumthng):
    i=0
    maxi=2
##    while i<maxi:
##        try:
##            req = urllib.request.Request(uri)
##        except:
##            i=i+1
##            
##            continue
##        break
    req=None
    global re
    req=re
    
    while i<maxi:
        try:
            req.headers['Range'] = 'bytes=%s-%s' % (start, start+chunk_size)
        except:
            i=i+1
            continue
        break
    if i==maxi:
        print("Bad Header! :/")
        exit()
    i=0
    while i<maxi:
        try:
            f = urllib.request.urlopen(req)
        except:
            i=i+1
            continue
        break
    if i==maxi:
        print("No response! :/")
        exit()

    try:
        parts[start] = f.read()
        print(int(nodo)," Completed! :D")
        monitor_speed()
    except:
        print("Network Error while downloading!\n")
        exit()

#numberofthreads
print("size- ",k)
#print("Chunk Size- ",chunk_size)
print("Downloading")
tempr.join()
startt=time.time()
for i in range(0,notr):
    t = threading.Thread(target=download,args=(i*chunk_size,"justrandom"))
    t.start()
    print("started ",i)
    threads.append( t)

print("0% Downloaded")
for i in threads:
    i.join()
endt=time.time()
result = ''
chunk = ''
i=1
print("Joining please wait! ")
while chunk!= None:
    key=i*chunk_size
    if key in parts:
        chunk = parts[i*chunk_size]
        parts[0]=parts[0]+parts[i*chunk_size]
       # result = result + chunk
        i = i + 1
    else:
        break
#print(result)
try:
    f = open(details[0],"wb")
except:
    print("invalid file name ! giving name -DEFAULT")
    f=open("DEFAULT","wb")
f.write(parts[0])
f.close()
print("Completed! :)")
print(os.path.getsize(details[0]))
print("Time taken-",endt-startt)

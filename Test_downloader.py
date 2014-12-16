import urllib.request
import urllib.parse
import sys
import random
import threading
    
uri=input("Enter url")
try:
    url = urllib.request.urlopen(uri)
   
except:
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
notr=3
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
        print(str(percen) + "% Downloaded")
    
        
def download(start):
##    try:
##        req = urllib.request.Request(uri)
##        req.headers['Range'] = 'bytes=%s-%s' % (start, start+chunk_size)
##        f = urllib.request.urlopen(req)
##        monitor_speed()
##        parts[start] = f.read()
##    except:
##        print("Unkown Error! ")
##        exit()
    req = urllib.request.Request(uri)
    req.headers['Range'] = 'bytes=%s-%s' % (start, start+chunk_size)
    f = urllib.request.urlopen(req)#is pretty fast as compared to read!
  #  print("done")
    parts[start] = f.read()#takes time;blocking method
    monitor_speed()
#numberofthreads
print("size- ",k)
#print("Chunk Size- ",chunk_size)
print("Downloading")
print("0% Downloaded")
for i in range(0,notr):
    t = threading.Thread(download(i*chunk_size))
    t.start()
    print("1")
    threads.append( t)


for i in threads:
    i.join()

chunk = ''
i=1
print("Joining please wait! ")
while chunk!= None:
    key=i*chunk_size
    if key in parts:
        chunk = parts[i*chunk_size]
        parts[0]=parts[0]+parts[i*chunk_size]
 
        i = i + 1
    else:
        break

try:
    f = open(details[0],"wb")
except:
    print("invalid file name ! giving name -DEFAULT")
    f=open("DEFAULT","wb")
f.write(parts[0])
f.close()
print("Completed! :)")

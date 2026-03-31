import sys
def main():
 if len(sys.argv)<2:
  sys.exit(1)
 try:
  f=open(sys.argv[1],"r")
  c=f.read()
  f.close()
 except:
  sys.exit(1)
 m={'>':0,'<':1,'+':2,'-':3,'.':4,',':5,'[':6,']':7,'*':8,'&':9,'i':10,'o':11,'!':12}
 for x in c:
  if x in m:
   v=m[x]
   sys.stdout.write("\u3000" if (v>>3)&1 else " ")
   sys.stdout.write("\u3000" if (v>>2)&1 else " ")
   sys.stdout.write("\u3000" if (v>>1)&1 else " ")
   sys.stdout.write("\u3000" if v&1 else " ")
if __name__=="__main__":
 main()

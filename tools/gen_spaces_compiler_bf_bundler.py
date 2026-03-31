import sys
class VM:
 def __init__(s):
  s.c=""; s.p=0
 def g(s,n):
  if n>s.p: s.c+=">"*(n-s.p)
  elif n<s.p: s.c+="<"*(s.p-n)
  s.p=n
 def a(s,n,v): s.g(n); s.c+="+"*v
 def d(s,n,v): s.g(n); s.c+="-"*v
 def z(s,n): s.g(n); s.c+="[-]"
 def cp(s,src,dst,t):
  s.z(dst); s.z(t); s.g(src); s.c+="["
  s.g(dst); s.c+="+"; s.g(t); s.c+="+"
  s.g(src); s.c+="-]"; s.g(t); s.c+="["
  s.g(src); s.c+="+"; s.g(t); s.c+="-]"
 def jz(s,v,f,cb):
  s.z(f); s.a(f,1); s.g(v); s.c+="["
  s.z(f); s.z(v); s.c+="]"; s.g(f); s.c+="["
  cb(); s.z(f); s.c+="]"
 def sa(s,b,v,t1,t2):
  s.z(t1); s.g(b); s.c+="["; s.g(t1); s.c+="+"; s.g(b); s.c+="-]"
  s.g(t1); s.c+="["; s.g(b); s.c+="++"; s.g(t1); s.c+="-]"
  s.cp(v,t1,t2)
  s.g(t1); s.c+="["; s.g(b); s.c+="+"; s.g(t1); s.c+="-]"
v=VM()

# === Void Engine: 16-bit MBR Spaces Interpreter ===
mbr=[0]*512
m=[
 0xFA,0x31,0xC0,0x8E,0xD8,0x8E,0xC0,0x8E,0xD0,0xBC,0x00,0x7C,
 0xB4,0x02,0xB0,0x10,0xB5,0x00,0xB1,0x02,0xB6,0x00,0xBB,0x00,0x7E,0xCD,0x13,
 0xBE,0x00,0x7E,0xBF,0x00,0x10,
 0x8A,0x04,0x08,0xC0,0x74,0x26,0x3C,0x05,0x75,0x08,0x8A,0x05,0xB4,0x01,0xBA,
 0x00,0x00,0xCD,0x14,0x3C,0x03,0x75,0x02,0xFE,0x05,0x3C,0x04,0x75,0x02,0xFE,
 0x0D,0x3C,0x01,0x75,0x01,0x47,0x3C,0x02,0x75,0x01,0x4F,0x46,0xEB,0xD4,0xF4,
 0xEB,0xFD
]
for i in range(len(m)): mbr[i]=m[i]
mbr[510]=0x55; mbr[511]=0xAA # MBR Boot Signature

for b in mbr:
 v.z(20); v.a(20,b); v.g(20); v.c+="."

# === 4-bit Spaces v2.0 Decoder ===
v.z(2); v.z(3)
v.g(1); v.c+=",["
v.z(4); v.z(5)
# 半角判定 (0x20)
v.cp(1,6,7); v.d(6,32)
def os(): v.z(4); v.a(4,1); v.z(5)
v.jz(6,8,os)
# 全角判定 (0xE3 0x80 0x80)
v.cp(1,6,7); v.d(6,227)
def of(): v.c+="[-],[-],"; v.z(4); v.a(4,1); v.z(5); v.a(5,1)
v.jz(6,8,of)
# 4ビットシフト演算
v.g(4); v.c+="["
v.sa(3,5,6,7)
v.a(2,1)
v.cp(2,6,7); v.d(6,4)
def o4():
 v.a(3,1) # 0x00 (EOF) 判定を避けるため +1 シフト
 v.g(3); v.c+="."; v.z(2); v.z(3)
v.jz(6,8,o4)
v.z(4); v.c+="]"
v.g(1); v.c+="[-],]"

sys.stdout.write(v.c)

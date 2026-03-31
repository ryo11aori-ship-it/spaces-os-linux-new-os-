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

# === VoidOS Bootloader (MBR 512 bytes) ===
# 16bit ASM: COM1ポート(0x3F8)に "VOID\n" を直接書き込み、無限ループで待機する
mbr=[0]*512
m=[0xBA,0xF8,0x03,0xB0,0x56,0xEE,0xB0,0x4F,0xEE,0xB0,0x49,0xEE,0xB0,0x44,0xEE,0xB0,0x0A,0xEE,0xEB,0xFE]
for i in range(len(m)): mbr[i]=m[i]
mbr[510]=0x55; mbr[511]=0xAA # ブートシグネチャ

# MBRをBrainfuckコードとして出力
for b in mbr:
 v.z(20); v.a(20,b); v.g(20); v.c+="."

# === 4ビット Spaces v2.0 デコーダ ===
v.z(2); v.z(3)
v.g(1); v.c+=",["
v.z(4); v.z(5)
# 半角判定
v.cp(1,6,7); v.d(6,32)
def os(): v.z(4); v.a(4,1); v.z(5)
v.jz(6,8,os)
# 全角判定
v.cp(1,6,7); v.d(6,227)
def of(): v.c+="[-],[-],"; v.z(4); v.a(4,1); v.z(5); v.a(5,1)
v.jz(6,8,of)
# 4ビットシフト演算
v.g(4); v.c+="["
v.sa(3,5,6,7)
v.a(2,1)
v.cp(2,6,7); v.d(6,4)
def o4(): v.a(3,1); v.g(3); v.c+="."; v.z(2); v.z(3)
v.jz(6,8,o4)
v.z(4); v.c+="]"
v.g(1); v.c+="[-],]"

sys.stdout.write(v.c)

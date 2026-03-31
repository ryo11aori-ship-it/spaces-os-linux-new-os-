#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#define TAPE_SIZE 1048576
#define MAX_FILE_SIZE 1048576
unsigned char tape[TAPE_SIZE];
int ptr=0;
int saved_ptr=0;
char op_map[16]={'>','<','+','-','.',',','[',']','*','&','i','o','!','?','?','?'};
void panic(const char *msg){fprintf(stderr,"[VM Error] %s\n",msg);exit(1);}
int is_full_space(const unsigned char *s,int idx,int len){
if(idx+2>=len)return 0;
if(s[idx]==0xE3&&s[idx+1]==0x80&&s[idx+2]==0x80)return 1;
return 0;}
int parse_line(const char *in,int in_len,char *out,int max_out){
int out_idx=0;int bit_buf=0;int bit_cnt=0;
for(int i=0;i<in_len&&in[i]!=0;i++){
int bit=-1;unsigned char uc=(unsigned char)in[i];
if(uc==0x20){bit=0;}
else if(uc==0xE3){if(is_full_space((const unsigned char*)in,i,in_len)){bit=1;}i+=2;}
if(bit!=-1){
bit_buf=(bit_buf<<1)|(bit&1);bit_cnt++;
if(bit_cnt==4){
if(out_idx>=max_out-1)panic("Out buf overflow");
out[out_idx++]=(char)op_map[bit_buf&0xF];
bit_buf=0;bit_cnt=0;}}}
out[out_idx]=0;return out_idx;}
void run_bf(char *code){
char *pc=code;memset(tape,0,sizeof(tape));ptr=0;
while(*pc){
switch(*pc){
case '>':ptr++;if(ptr>=TAPE_SIZE)panic("OOB Right");break;
case '<':ptr--;if(ptr<0)panic("OOB Left");break;
case '+':tape[ptr]++;break;
case '-':tape[ptr]--;break;
case '.':putchar(tape[ptr]);break;
case ',':{int c=getchar();tape[ptr]=(c==EOF)?0:(unsigned char)c;}break;
case '[':if(!tape[ptr]){int l=1;while(l>0){pc++;if(!*pc)panic("Unmatched [");if(*pc=='[')l++;if(*pc==']')l--;}}break;
case ']':if(tape[ptr]){int l=1;while(l>0){if(pc==code)panic("Unmatched ]");pc--;if(*pc=='[')l--;if(*pc==']')l++;}}break;
case '*':saved_ptr=ptr;ptr=(tape[ptr]|(tape[ptr+1]<<8));if(ptr>=TAPE_SIZE)ptr=0;break;
case '&':ptr=saved_ptr;break;
case 'i':fprintf(stderr,"[VM] IN Port %d\n",tape[ptr]);tape[ptr+1]=0;break;
case 'o':fprintf(stderr,"[VM] OUT Port %d, Val %d\n",tape[ptr],tape[ptr+1]);break;
case '!':fprintf(stderr,"[VM] INT 0x%02x\n",tape[ptr]);break;
default:break;
}pc++;}}
void process_buffer(unsigned char *in,size_t n){
size_t bc_cap=n+128;if(bc_cap<4096)bc_cap=4096;
char *bc=malloc(bc_cap);if(!bc)panic("Alloc fail");
int parsed=parse_line((const char*)in,(int)n,bc,(int)bc_cap);
if(parsed>0)run_bf(bc);
free(bc);}
int main(int argc,char **argv){
setbuf(stdout,NULL);
if(argc>1){
FILE *f=fopen(argv[1],"rb");if(!f){perror("File err");return 1;}
if(fseek(f,0,SEEK_END)!=0)panic("fseek err");
long s=ftell(f);if(s<0||s>MAX_FILE_SIZE)panic("Size err");
if(fseek(f,0,SEEK_SET)!=0)panic("fseek err");
unsigned char *in=malloc((size_t)s+1);if(!in)panic("Alloc fail");
size_t n=fread(in,1,(size_t)s,f);fclose(f);in[n]=0;
process_buffer(in,n);free(in);return 0;}
return 0;}

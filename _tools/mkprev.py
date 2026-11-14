import re,base64,os,sys
s=open(sys.argv[2] if len(sys.argv)>2 else 'index.html',encoding='utf-8').read()
s=re.sub(r'<link rel="stylesheet" href="assets/qeye-shell.css[^"]*">',lambda m:'<style>'+open('assets/qeye-shell.css').read()+'</style>',s)
s=re.sub(r'<script([^>]*) src="assets/qeye-shell.js[^"]*"([^>]*)></script>',lambda m:'<script>'+open('assets/qeye-shell.js').read()+'</script>',s)
c={}
def u(m):
    f=m.group(0)
    if not os.path.exists(f): return f
    if f not in c: c[f]='data:image/%s;base64,'%f.rsplit('.',1)[1].replace('jpg','jpeg').replace('svg','svg+xml')+base64.b64encode(open(f,'rb').read()).decode()
    return c[f]
s=re.sub(r'images/[A-Za-z0-9_./-]+\.(?:webp|png|jpe?g|svg)',u,s)
assert 'assets/' not in s
open(sys.argv[1],'w',encoding='utf-8').write(s)

import sys, re
tpl, css, bundle, out_frag, out_full = sys.argv[1:6]
t=open(tpl).read(); c=re.sub(r'/\*.*?\*/','',open(css).read(),flags=re.S)
frag=t.replace('__LEAFLET_CSS__',c).replace('__BUNDLE__',open(bundle).read())
open(out_frag,'w').write(frag)
head,body=frag.split('<div class="wrap">',1)
full=('<!doctype html>\n<html lang="id">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
 '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}[hidden]{display:none!important}</style>\n'
 +head+'</head>\n<body>\n<div class="wrap">'+body+'\n</body>\n</html>\n')
open(out_full,'w').write(full); print(len(frag))

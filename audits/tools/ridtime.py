"""Decode Anthropic request/message IDs (req_01 or msg_01 + base58 of 16 bytes; first 6 bytes = unix ms) to local MST times.
Usage: python ridtime.py FILE [FILE...]  -> first/last call per file, and per top-level-key prefix (first '|' field) if -k given."""
import json, re, sys, os, datetime as dt
A='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
TZ=dt.timezone(dt.timedelta(hours=-7))
pat=re.compile(r'(?:req|msg)_01[1-9A-HJ-NP-Za-km-z]{20,24}')
def rid_ms(r):
    v=0
    for c in r[6:]: v=v*58+A.index(c)
    b=v.to_bytes(16,'big')
    return int.from_bytes(b[:6],'big')
def fmt(ms): return dt.datetime.fromtimestamp(ms/1000,TZ).strftime('%m-%d %H:%M:%S')
if __name__=='__main__':
    bykey='-k' in sys.argv
    for f in [a for a in sys.argv[1:] if a!='-k']:
        s=open(f).read(); ids=pat.findall(s)
        if not ids: continue
        ms=[rid_ms(r) for r in ids]
        print(f"{os.path.basename(f):42s} n={len(ids):6d} first {fmt(min(ms))}  last {fmt(max(ms))}")
        if bykey:
            d=json.loads(s); groups={}
            items=d.items() if isinstance(d,dict) else enumerate(d)
            for k,v in items:
                g=str(k).split('|')[0]
                for r in pat.findall(json.dumps(v)): groups.setdefault(g,[]).append(rid_ms(r))
            for g,m in sorted(groups.items(), key=lambda x:min(x[1])):
                print(f"     {g:20s} n={len(m):5d} {fmt(min(m))} .. {fmt(max(m))}")

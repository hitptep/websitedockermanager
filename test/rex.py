# coding: GB2312
import os,re,sys


# execute command, and return the output
def execShell(shell):
    r = os.popen(shell)
    text = r.read()
    r.close()
    return text

# 获取计算机MAC地址和IP地址
if __name__ == '__main__':
    shell = "docker port "+sys.argv[1]
    result = execShell(shell)
    pat = "Physical Address[\. ]+: ([\w-]+)"
    MAC = re.findall(pat, result)[0]
    print("MAC=%s, IP=%s" %(MAC, IP))
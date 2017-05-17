import os
import re
import json

os.chdir('D:/Android/sdk/build-tools/25.0.2')
return_code = os.popen('dir')
aa = return_code.readlines()[-1]
isSuccess = re.search('测试', aa, re.S)
if isSuccess is not None:
    print('success')
else:
    print('fail')

project_dir = os.path.dirname(os.path.abspath(__file__))

d = dict(sdkPath='Bob', apkPath='aaa', signPath='sdf', password='1231131', channel='A0004')
dj = json.dumps(d)
with open(os.path.abspath(project_dir + '/config'), 'w') as f:
    f.write(dj)

with open(os.path.abspath(project_dir + '/config'), 'r') as f:
    content = f.read()
print(content)
d = json.loads(content)
print(d['password'])


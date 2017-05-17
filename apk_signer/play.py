import json
from tkinter.filedialog import *
import tkinter.messagebox as messagebox


class Application(Frame):
    zipAlignApkPath = ''
    finalApkPath = ''
    project_dir = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        self.init_data()

    def create_widgets(self):
        self.sdkPath = StringVar()
        self.apkPath = StringVar()
        self.signPath = StringVar()
        self.password = StringVar()
        self.channel = StringVar()

        Label(self, text="选择SDK路径:").grid(row=0, column=0)
        Entry(self, state='readonly', textvariable=self.sdkPath).grid(row=0, column=1)
        Button(self, text=" ... ", command=self.pickSdkPath).grid(row=0, column=2, pady=5)

        Label(self, text="APK源文件:").grid(row=1, column=0)
        Entry(self, state='readonly', textvariable=self.apkPath).grid(row=1, column=1)
        Button(self, text=" ... ", command=self.pickApkPath).grid(row=1, column=2, pady=5)

        Label(self, text="签名文件:").grid(row=2, column=0)
        Entry(self, state='readonly', textvariable=self.signPath).grid(row=2, column=1)
        Button(self, text=" ... ", command=self.pickSignPath).grid(row=2, column=2, pady=5)

        Label(self, text="签名密码:").grid(row=3, column=0)
        Entry(self, show='*', textvariable=self.password).grid(row=3, column=1, columnspan=2, sticky=E + W, pady=5)

        Label(self, text="渠道名称:").grid(row=4, column=0)
        Entry(self, textvariable=self.channel).grid(row=4, column=1, pady=5)

        Button(self, text="保存", command=self.save_data).grid(row=5, column=2, pady=10, padx=10)
        Button(self, text="执行", command=self.process).grid(row=5, column=3, pady=10)

    def pickSdkPath(self):
        self.sdkPath.set(askdirectory())

    def pickApkPath(self):
        self.apkPath.set(askopenfilename(filetypes=[('apk files', '.apk')]))

    def pickSignPath(self):
        self.signPath.set(askopenfilename(filetypes=[('jks files', '.jks')]))

    def process(self):
        os.chdir(self.sdkPath.get())
        self.zipAlignApkPath = self.apkPath.get().replace('.apk', '_zipalign.apk')
        cmd = 'zipalign -v 4 ' + self.apkPath.get() + ' ' + self.zipAlignApkPath
        print(cmd)
        return_code = os.popen(cmd)
        for line in return_code.readlines():
            print(line)
        is_success = re.search('succesful', line, re.S)
        if is_success is None:
            messagebox.showinfo('消息', 'Zip对齐失败')
            return
        cmd = 'apksigner sign --ks ' + self.signPath.get() + ' ' + self.zipAlignApkPath + ' '
        print(cmd)
        cmd_in = os.popen(cmd, 'w')
        cmd_in.write(self.password.get())
        cmd_in.flush()
        cmd_in.close()

        os.chdir(self.project_dir)
        cmd = 'java -jar CheckAndroidV2Signature.jar ' + self.zipAlignApkPath
        print(cmd)
        return_code = os.popen(cmd)
        result_dict = json.loads(return_code.read())
        is_success = result_dict['isV2OK']
        if is_success is False:
            messagebox.showinfo('消息', '签名失败')
            os.remove(self.zipAlignApkPath)
            return

        self.finalApkPath = self.zipAlignApkPath.replace('_zipalign.apk', '_' + self.channel.get() + '_final.apk')
        cmd = 'java -jar walle-cli-all.jar put -c ' + self.channel.get() + ' ' + self.zipAlignApkPath + ' ' + \
              self.finalApkPath
        return_code = os.popen(cmd)
        print(return_code.read())
        os.remove(self.zipAlignApkPath)
        messagebox.showinfo('消息', '打包完成')

    def init_data(self):
        with open(os.path.abspath(self.project_dir + '/config'), 'r') as f:
            content = f.read()
        d = json.loads(content)
        self.sdkPath.set(d['sdkPath'])
        self.apkPath.set(d['apkPath'])
        self.signPath.set(d['signPath'])
        self.password.set(d['password'])
        self.channel.set(d['channel'])

    def save_data(self):
        d = dict(sdkPath=self.sdkPath.get(), apkPath=self.apkPath.get(), signPath=self.signPath.get(),
                 password=self.password.get(), channel=self.channel.get())
        dj = json.dumps(d)
        with open(os.path.abspath(self.project_dir + '/config'), 'w') as f:
            f.write(dj)


if __name__ == '__main__':
    app = Application()
    # 设置窗口标题:
    app.master.title('APK签名渠道打包工具')
    # 主消息循环:
    app.mainloop()

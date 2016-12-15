from tkinter.filedialog import *
import tkinter.messagebox as messagebox
import requests


class Application(Frame):
    baseUrl = 'http://www.atool.org/'
    filenames = {}

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.helloLabel = Label(self, text='点击按钮，选取要压缩的图片!')
        self.helloLabel.pack()
        self.pickButton = Button(self, text='选图', command=self.pickFile)
        self.pickButton.pack()
        self.compressButton = Button(self, text='压缩', command=self.compressPics)
        self.compressButton.pack()

    def pickFile(self):
        self.filenames = askopenfilenames(filetypes= [('png files', '.png'),('jpg files', '.jpg')])
        print(self.filenames)

    def compressPics(self):
        url = self.baseUrl + 'pngcompression.php'
        payloads = {'rate': '10', 'action': 'make'}
        for filename in self.filenames:
            files = {'pic': open(filename, 'rb')}
            html = requests.post(url, data=payloads, files=files)
            image_path = re.search('一个小时</span><br><a href="(.*?)" target="_blank">点击查看并下载</a>', html.text, re.S).group(
                1)
            ir = requests.get(self.baseUrl + image_path)
            if ir.status_code == 200:
                compressed_pic = filename.replace(".", "_compressed.")
                open(compressed_pic, 'wb').write(ir.content)
            messagebox.showinfo('消息', '照片压缩完成')

if __name__ == '__main__':
    app = Application()
    # 设置窗口标题:
    app.master.title('JPG、PNG无损压缩器')
    # 主消息循环:
    app.mainloop()

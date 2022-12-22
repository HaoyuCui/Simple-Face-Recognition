import os
import struct
import tkinter as tk
import sklearn
from tkinter import ttk, filedialog
from tkinter import Menu


from PIL import Image, ImageTk
from utils import generate_file, load_params, evaluate, test_image

train_dir = os.listdir('gt_db/')
clf = None


class MainWindows(tk.Tk):
    def __init__(self):
        super().__init__()  # 初始化基类

        self.title("Face Recognition Master")
        self.resizable(width=False, height=False)
        self.minsize(640, 320)

        self.tabControl = ttk.Notebook(self)  # 创建标签栏整体
        self.tab1 = ttk.Frame(self.tabControl)  # 创建标签栏1
        self.tab2 = ttk.Frame(self.tabControl)  # 创建标签栏2
        self.tab3 = ttk.Frame(self.tabControl)  # 创建标签栏3

        self.menu_bar = Menu(self)  # 创建菜单栏

        self.init_ui()

        self.selected_files = []  # 被选中的文件，获取识别结果被使用
        self.photo_libs = []  # 本地图片库
        self.feature_libs = []  # 本地特征向量库
        self.lib_path = 'gt_db/'  # 本地库文件路径

        self.update_treeview()

    def init_ui(self):  # 初始化 UI界面
        self.tabControl.add(self.tab1, text='model')  # Add the tab
        self.tabControl.add(self.tab2, text='face recognition')  # Make second tab visible
        self.tabControl.add(self.tab3, text='database')  # Make second tab visible
        self.tabControl.pack(expand=1, fill="both")  # Pack to make visible

        self.init_tab1()
        self.init_tab2()
        self.init_tab3()

        self.config(menu=self.menu_bar)
        self.init_menu()

    def init_tab1(self):  # 初始化标签
        mighty = ttk.LabelFrame(self.tab1, text='')
        mighty.pack()
        btn1 = ttk.Button(mighty, text="📥 Generate feature file", command=self.select_btn_tab1)
        btn2 = ttk.Button(mighty, text="📑 Fit model & Evaluate", command=self.get_result1)
        btn1.grid(column=0, row=1, sticky='W')
        btn2.grid(column=0, row=2, sticky='W')
        self.name = tk.StringVar()
        name_entered = ttk.Entry(mighty, width=40, textvariable=self.name)
        name_entered.grid(column=0, row=3, sticky='W')  # align left/West

    def init_tab2(self):  # 初始化标签
        mighty2 = ttk.LabelFrame(self.tab2, text='')
        mighty2.pack()

        self.label_rec = tk.Label(mighty2, text='Pictures to be handles', bg="Silver", padx=15, pady=15)
        self.label_rec.grid(column=0, row=0, sticky='W')
        btn_sel = ttk.Button(mighty2, text="📂 Select files", command=self.select_btn_tab2)
        btn2_res = ttk.Button(mighty2, text="🎯 predict", command=self.get_result2)
        btn_sel.grid(column=0, row=1, sticky='W')
        btn2_res.grid(column=0, row=2, sticky='W')
        label_res = tk.Label(mighty2, text='results')
        label_res.grid(column=0, row=3, sticky='W')
        self.name2 = tk.StringVar()
        name_entered2 = ttk.Entry(mighty2, width=40, textvariable=self.name2)
        name_entered2.grid(column=0, row=20, sticky='W')  # align left/West

    def init_tab3(self):  # 初始化标签
        mighty3 = ttk.LabelFrame(self.tab3, text='local data')
        mighty3.pack()
        self.tree = ttk.Treeview(mighty3, height=4, columns=('name'))  # 表格
        self.tree.grid(row=0, column=0, sticky='nsew')
        # Setup column heading
        self.tree.heading('0', text='name', anchor='center')
        self.tree.column('name', anchor='center', width=100)
        s = ttk.Style()
        s.configure('Treeview', rowheight=80)
        s.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))  # Modify the font of the body
        s.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # Modify the font of the headings
        s.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders
        newb3 = ttk.Button(mighty3, text='🔄 Refresh', width=20, command=self.update_treeview)
        newb3.grid(row=2, column=0, sticky='nsew')

    def init_menu(self):  # 初始化菜单
        # Add menu items
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Add another Menu to the Menu Bar and an item
        help_menu = Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About")
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

    def show_img(self, labels, filename, length=1):
        if len(filename) < 1:
            return
        for i in range(length):
            img = Image.open(filename[i])
            half_size = (256, 256)
            img.thumbnail(half_size, Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            labels[i].configure(image=photo)
            labels[i].image = photo

    def select_file(self):  # 选择文件进行测试
        self.selected_files = []
        ftypes = [('Image Files', '*.tif *.jpg *.png')]
        dlg = filedialog.Open(filetypes=ftypes, multiple=True)
        filename = dlg.show()
        self.selected_files = filename
        return filename

    def select_btn_tab1(self):  # 交互操作反馈
        self.name.set('Coding... don\'t exit.')
        generate_file(train_dir)
        self.name.set('Coding done.')

    def get_result1(self):  # 交互返回
        encodings, names = load_params(re_generate=False)
        global clf
        score_test, scores_cv, clf = evaluate(encodings, names)
        # self.name.set("🚀[Test score]:{}; 📊[Cross validation scores]:{}".format(score_test, scores_cv))
        self.name.set("🚀[Cross validation scores]:{}".format(scores_cv))

    def select_btn_tab2(self):  # 交互操作反馈（返回图片）
        self.show_img([self.label_rec], self.select_file())

    def get_result2(self):  # 返回结果（预测值）
        global clf
        if clf is None:
            self.name2.set('⚠️ Please train a model first! (go to <model> page)')
        if len(self.selected_files) >= 1 and clf is not None:
            file = self.selected_files[0]
            names = test_image(clf, image_loc=file)
            list_ = ' '.join(str(name) for name in names)
            self.name2.set(list_)

    def get_lib(self, suffix='jpg'):  # 获取文件列表
        ret = []
        for root, dirs, files in os.walk(self.lib_path):
            for file in files:
                # 获取文件名, 文件路径
                suf = file.split('.')[-1]
                if suf == suffix:
                    if suffix == 'jpg':
                        ret.append([str(os.path.join(root, file)).split('/')[1], os.path.join(root, file)])
                    else:
                        ret.append(os.path.join(root, file))
        return ret

    def delete_all_treeview(self):  # 用于文件列表更新操作
        for row in self.tree.get_children():
            self.tree.delete(row)

    def update_treeview(self):  # 文件列表更新操作
        self.photo_libs = []
        self.delete_all_treeview()

        libs_img = self.get_lib()
        libs_len = len(libs_img)
        count = 0

        for i in range(libs_len):
            cur_pair = libs_img[i]
            # print(cur_pair)
            img = Image.open(cur_pair[1])
            thumbnail_size = (50, 50)
            img.thumbnail(thumbnail_size, )
            photo = ImageTk.PhotoImage(img)
            self.photo_libs.append(photo)
            self.tree.insert('', count, text="", image=self.photo_libs[-1], value=(cur_pair[0]))
            count += 1

        # 更新特征向量库
        self.get_features_vec_lib()

    def get_features_vec_lib(self):  # 文件列表获取标签信息
        self.feature_libs = []
        files = self.get_lib('fea')
        for file in files:
            # 读取本地数据
            read_result = []
            fmt = str(512) + 'd'
            with open(file, 'rb') as binfile:
                data = binfile.read()
                a = struct.unpack(fmt, data)
                # print(a)
                read_result.append(a)
            self.feature_libs.append([file.split('/')[-1].split('.')[0], read_result])

    def _quit(self):
        self.quit()
        self.destroy()
        exit()


if __name__ == '__main__':
    app = MainWindows()
    app.mainloop()

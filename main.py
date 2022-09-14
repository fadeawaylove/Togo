import os
import threading
from tkinter.filedialog import askdirectory
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import utility
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

from api import get_gitee_client
from utils import ConfigUtil


def prepare() -> int:
    """
    :return: 0-ok 1-没有token 2-没有缓存目录 3-没有设置默认展示的仓库
    """
    gitee_client = get_gitee_client()
    succ, user_info = gitee_client.get_user_info()
    if not succ:
        return 1
    ConfigUtil.set_gitee_user_info(user_info)

    if not ConfigUtil.get_cache_dir():
        return 2

    if not ConfigUtil.get_default_repo():
        return 3
    return 0


class LoginPage:
    """登陆页面"""

    def __init__(self, master):
        self.master = master
        f1 = ttk.Frame(master, bootstyle=LIGHT)
        f1.place(anchor="c", relx=.5, rely=.5, bordermode=OUTSIDE, width=300)

        l1 = ttk.Label(f1, text="输入gitee token登录")
        l1.pack(pady=5, side=TOP, anchor=N)

        e1 = ttk.Entry(f1, text="登录", show="*")
        e1.pack(pady=5, side=TOP, anchor=N)

        def login():
            val = e1.get()
            client = get_gitee_client(val)
            succ, user_info = client.get_user_info()
            if succ:
                ConfigUtil.set_gitee_token(val)
                ConfigUtil.set_gitee_user_info(user_info)
                f1.place_forget()
                CacheDirPage(master)
            else:
                Messagebox.show_warning("token错误，请重新输入", "登录失败")

        b1 = ttk.Button(f1, text="登录", command=login)
        b1.pack(pady=5, side=TOP, anchor=N)

        master.mainloop()


class CacheDirPage:
    """选择cache文件夹"""

    def __init__(self, master):
        self.master = master
        self.path_var = ttk.StringVar(value="")

        self.fm = ttk.Frame(master, bootstyle=LIGHT)
        self.fm.place(anchor="c", relx=.5, rely=.5, bordermode=OUTSIDE)

        option_text = "设置本地文件保存路径"
        self.option_lf = ttk.Labelframe(self.fm, text=option_text, padding=15)
        self.option_lf.pack(fill=X, expand=YES, anchor=N)

        path_row = ttk.Frame(self.option_lf)
        path_row.pack(fill=X, expand=YES)
        path_lbl = ttk.Label(path_row, text="文件缓存目录")
        path_lbl.pack(side=LEFT, padx=(6, 0))
        path_ent = ttk.Entry(path_row, textvariable=self.path_var)
        path_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)
        browse_btn = ttk.Button(
            master=path_row,
            text="选择",
            command=self.on_browse,
            width=8
        )
        browse_btn.pack(side=LEFT, padx=5)

        confirm_btn = ttk.Button(
            master=self.option_lf,
            text="确认",
            command=self.set_cache_dir
        )
        confirm_btn.pack(side=TOP, pady=(18, 0))

        master.mainloop()

    def on_browse(self):
        path = askdirectory(title="选择目录")
        if path:
            self.path_var.set(path)

    def set_cache_dir(self):
        p = self.path_var.get()
        if not p or not os.path.exists(p):
            Messagebox.show_warning("请选择有效目录", "目录错误")
            return
        print(self.path_var.get())
        ConfigUtil.set_cache_dir(p)
        self.fm.place_forget()
        self.go_to_home_page()

    def go_to_home_page(self):
        HomePage(self.master)


class ChooseRepoPage:
    """选择默认展示的仓库"""

    def __init__(self, master):
        self.master = master
        self.repo_name = ttk.StringVar(value="")

        self.show_loading()
        self.master.mainloop()

    def show_loading(self):
        loading_frame = ttk.Frame(self.master, padding=20)
        loading_frame.place(anchor="c", relx=.5, rely=.5, bordermode=OUTSIDE)
        loading_label = ttk.Label(loading_frame)
        loading_label.pack()
        loading_label.config(text="加载中...")
        loading_label.update_idletasks()
        self.show_repo_selector()
        loading_label.config(text="I'm done doing...")
        loading_frame.place_forget()

    def show_repo_selector(self):
        gitee_client = get_gitee_client()
        succ, repos = gitee_client.get_user_repos()
        if not succ:
            Messagebox.show_error(f"获取用户仓库错误，错误代码【{repos}】", "错误")
            return
        human_name_list = [repo["human_name"] for repo in repos]
        human_name_map = {repo["human_name"]: repo for repo in repos}
        fm = ttk.Labelframe(self.master, text="选择默认仓库", padding=20)
        fm.place(anchor="c", relx=.5, rely=.5, bordermode=OUTSIDE)
        repo_cbo = ttk.Combobox(
            master=fm,
            values=human_name_list,
            width=30,
            exportselection=True
        )
        repo_cbo.pack(side=LEFT)
        repo_cbo.current(0)

        def select_repo():
            ConfigUtil.set_default_repo(human_name_map[repo_cbo.get()])
            fm.place_forget()
            HomePage(self.master)

        btn = ttk.Button(fm, text="确定", command=select_repo)
        btn.pack(side=RIGHT, padx=(10, 0))


class HomePage:

    def __init__(self, master):
        self.master = master
        self.body = ttk.Frame(master, bootstyle=LIGHT)
        self.body.pack(fill="both", expand=True, )

        self.frame_navigator = tk.PanedWindow(self.body, orient=HORIZONTAL, sashpad=1)
        self.frame_navigator.pack_propagate(0)

        self.file_tree = None
        self.show_left_file_tree()

        self.content_navigator = ttk.Frame(self.frame_navigator)
        self.show_text_btn()

        self.frame_navigator.add(self.content_navigator, minsize=200)

        self.frame_navigator.pack(side=tk.TOP, expand=True, fill=BOTH)

        master.mainloop()

    def show_left_file_tree(self):
        self.file_tree = ttk.Treeview(self.frame_navigator, bootstyle=INFO,
                                      columns=[0, 1, 2, 3, 4],
                                      show=TREEHEADINGS
                                      )
        self.file_tree.bind("<<TreeviewSelect>>", self.choose_file)

        vsb = ttk.Scrollbar(self.file_tree, orient=VERTICAL, command=self.file_tree.yview, bootstyle=ROUND)
        vsb.pack(side=RIGHT, fill=Y)
        self.file_tree.configure(yscroll=vsb.set)

        self.file_tree.pack(fill=BOTH, )
        self.frame_navigator.add(self.file_tree, minsize=60, width=180)

    def choose_file(self, event):
        print("选中文件", event.widget.selection())

    def show_text_btn(self):
        def test():
            self.file_tree.insert("", 'end', text="文件夹1", open=True)

        ttk.Button(self.content_navigator, text="123123123", command=test).pack()


def main():
    root = ttk.Window(title="Togo", size=(900, 600))
    root.place_window_center()
    p = prepare()
    if p == 1:
        LoginPage(root)
        return
    if p == 2:
        CacheDirPage(root)
        return
    if p == 3:
        ChooseRepoPage(root)
    HomePage(root)


if __name__ == '__main__':
    main()

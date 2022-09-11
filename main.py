import os
from tkinter.filedialog import askdirectory
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

from api import GiteeApi
from utils import ConfigUtil


def prepare() -> int:
    """
    :return: 0-ok 1-没有token 2-没有缓存目录
    """
    succ, user_info = GiteeApi(ConfigUtil.get_gitee_token() or "").get_user_info()
    if not succ:
        return 1
    ConfigUtil.set_gitee_user_info(user_info)

    if not ConfigUtil.get_cache_dir():
        return 2

    return 0


class LoginPage:

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
            succ, user_info = GiteeApi(val).get_user_info()
            if succ:
                ConfigUtil.set_gitee_token(val)
                ConfigUtil.set_gitee_user_info(user_info)
                f1.place_forget()
                HomePage(master)
            else:
                Messagebox.show_warning("token错误，请重新输入", "登录失败")

        b1 = ttk.Button(f1, text="登录", command=login)
        b1.pack(pady=5, side=TOP, anchor=N)

        master.mainloop()


class HomePage:

    def __init__(self, master):
        self.master = master

        self.body = ttk.Frame(master, bootstyle=LIGHT)
        self.body.pack(fill="both", expand=True,
                       # padx=5, pady=5
                       )

        frame_navigator = tk.PanedWindow(self.body, orient=HORIZONTAL, sashpad=1,
                                         sashrelief=GROOVE, borderwidth=1)
        frame_navigator.pack_propagate(0)

        file_navigator = ttk.Frame(frame_navigator, width=180)
        frame_navigator.add(file_navigator, minsize=60)

        content_navigator = ttk.Frame(frame_navigator)
        frame_navigator.add(content_navigator, minsize=200)

        frame_navigator.pack(side=tk.TOP, expand=10, fill=tk.BOTH)

        master.mainloop()


class GuidPage:

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


def main():
    root = ttk.Window(title="Togo", size=(900, 600))
    root.place_window_center()
    p = prepare()
    if p == 1:
        LoginPage(root)
        return
    if p == 2:
        GuidPage(root)
        return
    HomePage(root)


if __name__ == '__main__':
    main()

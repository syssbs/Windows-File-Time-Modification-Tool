import os
import sys
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
import subprocess
import platform


# 检查是否具有管理员权限(仅限Windows)
def is_admin():
    if platform.system() != "Windows":
        return True  # 非 Windows 系统默认返回 True
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# 运行命令的函数
def run_command(cmd):
    try:
        if platform.system() == "Windows":
            # 在 Windows 系统运行 PowerShell 命令
            subprocess.run(["powershell.exe", "-Command", cmd], check=True, stderr=subprocess.PIPE)
        else:
            # 在其他系统上运行 shell 命令
            subprocess.run(cmd, shell=True, check=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        # 捕获并显示命令执行错误
        messagebox.showerror("错误", e.stderr.decode())
    except Exception as e:
        # 捕获并显示其他错误
        messagebox.showerror("错误", str(e))


# 选择文件的函数
def select_files():
    # 打开文件选择对话框
    file_paths = filedialog.askopenfilenames()
    # 将选择的文件路径添加到文本框
    current_paths = path_text.get('1.0', tk.END).strip().split('\n')
    if current_paths == ['']:
        current_paths = []
    current_paths.extend(file_paths)
    path_text.delete('1.0', tk.END)
    path_text.insert('1.0', '\n'.join(current_paths))


# 选择文件夹的函数
def select_folder():
    # 打开文件夹选择对话框
    folder_path = filedialog.askdirectory()
    # 将选择的文件夹路径添加到文本框
    current_paths = path_text.get('1.0', tk.END).strip().split('\n')
    if current_paths == ['']:
        current_paths = []
    current_paths.append(folder_path)
    path_text.delete('1.0', tk.END)
    path_text.insert('1.0', '\n'.join(current_paths))


# 修改文件时间的函数
def change_times(attribute):
    # 获取输入的时间字符串
    time_str = time_entry.get()
    # 获取选择的路径
    paths = path_text.get('1.0', tk.END).strip().split('\n')
    if not paths or paths == ['']:
        # 如果没有选择路径，显示警告
        messagebox.showwarning("警告", "请先选择文件或文件夹")
        return
    if not time_str:
        # 如果没有输入时间，显示警告
        messagebox.showwarning("警告", "请先输入时间")
        return

    try:
        # 验证时间格式是否正确
        datetime.strptime(time_str, "%m/%d/%Y %H:%M:%S")
    except ValueError:
        # 如果时间格式不正确，显示错误
        messagebox.showerror("错误", "时间格式不正确，请使用 MM/DD/YYYY HH:MM:SS 格式")
        return

    # 询问是否更改文件夹的时间戳
    change_folder_time = messagebox.askyesno("更改文件夹时间", "是否更改所选文件夹的时间戳？")

    if platform.system() == "Windows":
        # 在 Windows 系统上构建 PowerShell 脚本
        powershell_script = ""
        for path in paths:
            if os.path.isdir(path):
                if change_folder_time:
                    powershell_script += f"Get-Item -LiteralPath '{path}' | %{{ $_.{attribute} = Get-Date '{time_str}' }};"
                if not only_folders_var.get():
                    powershell_script += f"Get-ChildItem -LiteralPath '{path}' -Recurse | %{{ $_.{attribute} = Get-Date '{time_str}' }};"
            else:
                powershell_script += f"Get-Item -LiteralPath '{path}' | %{{ $_.{attribute} = Get-Date '{time_str}' }};"
        run_command(powershell_script)
    else:
        # 在其他系统上构建 shell 命令
        unix_command = ""
        for path in paths:
            if os.path.isdir(path):
                if change_folder_time:
                    unix_command += f"touch -d '{time_str}' '{path}';"
                if not only_folders_var.get():
                    for root, dirs, files in os.walk(path):
                        for name in dirs + files:
                            unix_command += f"touch -d '{time_str}' '{os.path.join(root, name)}';"
            else:
                unix_command += f"touch -d '{time_str}' '{path}';"
        run_command(unix_command)

    # 显示成功信息
    messagebox.showinfo("成功", f"{attribute} 时间已更改")


# 设置主题颜色和字���
BG_COLOR = "#f0f0f0"
FG_COLOR = "#333333"
FONT_NORMAL = ("Arial", 10)
FONT_BOLD = ("Arial", 10, "bold")


# 在当前文件夹和子文件夹中寻找icon.ico
def find_icon():
    for root_dir, _, files in os.walk(os.getcwd()):
        if "icon.ico" in files:
            return os.path.join(root_dir, "icon.ico")
    return None


# 创建主窗口
root = tk.Tk()
root.title("文件时间修改酱")
root.configure(bg=BG_COLOR)
# 设置窗口图标
if platform.system() == "Windows":
    icon_path = find_icon()
    if icon_path:
        root.iconbitmap(icon_path)
    else:
        messagebox.showerror("错误", "未找到icon.ico文件")
        sys.exit()

# 配置样式
style = ttk.Style()
style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR, font=FONT_NORMAL)
style.configure("TButton", font=FONT_NORMAL)
style.configure("TEntry", font=FONT_NORMAL)

# 创建并放置标签、文本框和按钮
path_label = ttk.Label(root, text="选择的路径:")
path_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

path_text = tk.Text(root, height=10, width=50)
path_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

time_label = ttk.Label(root, text="输入时间 (MM/DD/YYYY HH:MM:SS):")
time_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")

time_entry = ttk.Entry(root)
time_entry.grid(row=2, column=1, padx=10, pady=(10, 0), sticky="ew")

select_files_button = ttk.Button(root, text="选择文件", command=select_files)
select_files_button.grid(row=3, column=0, padx=10, pady=10)

select_folder_button = ttk.Button(root, text="选择文件夹", command=select_folder)
select_folder_button.grid(row=3, column=1, padx=10, pady=10)

change_creation_button = ttk.Button(root, text="修改创建时间", command=lambda: change_times('CreationTime'))
change_creation_button.grid(row=4, column=0, padx=10, pady=5)

change_modification_button = ttk.Button(root, text="修改修改时间", command=lambda: change_times('LastWriteTime'))
change_modification_button.grid(row=4, column=1, padx=10, pady=5)

change_access_button = ttk.Button(root, text="修改访问时间", command=lambda: change_times('LastAccessTime'))
change_access_button.grid(row=5, column=0, padx=10, pady=(5, 10))

# 添加"只修改文件夹"复选框
only_folders_var = tk.BooleanVar()
only_folders_check = ttk.Checkbutton(root, text="只修改文件夹", variable=only_folders_var)
only_folders_check.grid(row=5, column=1, padx=10, pady=(5, 10))

# 获取当前系统信息
system_info = platform.system()

# 创建并放置系统信息标签
system_label = ttk.Label(root, text=f"当前系统: {system_info}")
system_label.grid(row=6, column=1, padx=10, pady=(5, 10), sticky="se")

# 配置列的权重
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# 检查并请求管理员权限
if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()

# 运行主循环
root.mainloop()

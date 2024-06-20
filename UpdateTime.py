import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
import subprocess

def run_powershell_command(cmd):
    try:
        subprocess.run(["powershell.exe", "-Command", cmd], check=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("错误", e.stderr.decode())
    except Exception as e:
        messagebox.showerror("错误", str(e))

def select_files():
    file_paths = filedialog.askopenfilenames()
    folder_paths = filedialog.askdirectory()
    all_selected_paths = list(file_paths) + [folder_paths]
    path_text.delete('1.0', tk.END)
    path_text.insert('1.0', '\n'.join(all_selected_paths))

def change_times(attribute):
    time_str = time_entry.get()
    paths = path_text.get('1.0', tk.END).strip().split('\n')
    if not paths or paths == ['']:
        messagebox.showwarning("警告", "请先选择文件或文件夹")
        return
    if not time_str:
        messagebox.showwarning("警告", "请先输入时间")
        return

    try:
        datetime.strptime(time_str, "%m/%d/%Y %H:%M:%S")
    except ValueError:
        messagebox.showerror("错误", "时间格式不正确，请使用 MM/DD/YYYY HH:MM:SS 格式")
        return

    # 弹窗询问用户是否更改所选文件夹的时间戳
    change_folder_time = messagebox.askyesno("更改文件夹时间", "是否更改所选文件夹的时间戳？")
    
    # 构建PowerShell命令
    powershell_script = ""
    for path in paths:
        # 检查路径是否为文件夹
        if os.path.isdir(path):
            # 根据用户选择决定是否包括父文件夹本身
            if change_folder_time:
                powershell_script += f"Get-Item -LiteralPath '{path}' | %{{ $_.{attribute} = Get-Date '{time_str}' }};"
            powershell_script += f"Get-ChildItem -LiteralPath '{path}' -Recurse | %{{ $_.{attribute} = Get-Date '{time_str}' }};"
        else:
            powershell_script += f"Get-Item -LiteralPath '{path}' | %{{ $_.{attribute} = Get-Date '{time_str}' }};"
    
    # 执行PowerShell命令
    run_powershell_command(powershell_script)
    messagebox.showinfo("成功", f"{attribute} 时间已更改")


# 设置主题颜色和字体
BG_COLOR = "#f0f0f0"
FG_COLOR = "#333333"
FONT_NORMAL = ("Arial", 10)
FONT_BOLD = ("Arial", 10, "bold")

root = tk.Tk()
root.title("文件时间修改器")
root.configure(bg=BG_COLOR)

style = ttk.Style()
style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR, font=FONT_NORMAL)
style.configure("TButton", font=FONT_NORMAL)
style.configure("TEntry", font=FONT_NORMAL)

# 使用grid布局
path_label = ttk.Label(root, text="选择的路径:")
path_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

path_text = tk.Text(root, height=10, width=50)
path_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

time_label = ttk.Label(root, text="输入时间 (MM/DD/YYYY HH:MM:SS):")
time_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")

time_entry = ttk.Entry(root)
time_entry.grid(row=2, column=1, padx=10, pady=(10, 0), sticky="ew")

select_button = ttk.Button(root, text="浏览选择", command=select_files)
select_button.grid(row=3, column=0, padx=10, pady=10)

change_creation_button = ttk.Button(root, text="修改创建时间", command=lambda: change_times('CreationTime'))
change_creation_button.grid(row=4, column=0, padx=10, pady=5)

change_modification_button = ttk.Button(root, text="修改修改时间", command=lambda: change_times('LastWriteTime'))
change_modification_button.grid(row=4, column=1, padx=10, pady=5)

change_access_button = ttk.Button(root, text="修改访问时间", command=lambda: change_times('LastAccessTime'))
change_access_button.grid(row=5, column=0, padx=10, pady=(5, 10))

# 让第一列和第二列的宽度相等
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()

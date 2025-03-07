import json
import time
import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import os
import winsound
import keyboard
import sys
import io
import threading
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD


class CreateToolTip:
    """
    创建一个工具提示类
    """

    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.widget.bind('<Enter>', self.on_enter)
        self.widget.bind('<Leave>', self.on_leave)

    def showtip(self, text, x, y):
        "显示提示信息"
        if self.tipwindow or not text:
            return
        x = self.widget.winfo_rootx() + x
        y = self.widget.winfo_rooty() + y + 20  # 在鼠标位置的正下方显示
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw,
                         text=text,
                         justify=tk.LEFT,
                         background="#F1F1F1",
                         relief=tk.SOLID,
                         borderwidth=1,
                         font=("tahoma", "12", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

    def on_enter(self, event):
        # 当鼠标进入按钮区域时显示提示信息
        self.widget['cursor'] = 'question_arrow'
        self.showtip(self.text, event.x, event.y)

    def on_leave(self, event):
        # 当鼠标离开按钮区域时隐藏提示信息
        self.hidetip()
        self.widget['cursor'] = ''


class Home:

    def __init__(self, root):
        self.root = root
        self.config_file = './Python_Clipboard_to_File_project_config.json'
        self.settings = self.load_settings()
        self.key_bind = self.settings['Quick Save']
        self.shortcut_entries = {}
        self.init_ui()
        self.bind_shortcuts(self.key_bind)
        self.init_clipboard()
        # 绑定拖拽事件
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop_filePath)

    def load_settings(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            default_settings = {
                'Default file path':
                os.path.join(os.path.expanduser('~'), 'Desktop',
                             'clipboard.md'),
                'Quick Save':
                'Ctrl+3',
                '快捷键2':
                '',
                'script':
                "import time\nimport winsound\nimport sys\n\n# 设置蜂鸣声的频率和持续时间（单位：毫秒）\nfrequency = 2500  # 频率\nduration = 1000  # 持续时间\n\n# 每十分钟触发一次蜂鸣声\ninterval = 10 * 60  # 10分钟的秒数\n\ndef StarAnimation(duration, stop_event):\n    # 定义旋转字符数组\n    spinner = ['*', '/', '|', '\\\\', '+']\n    spinner_index = 0\n\n    # 设置动画持续时间\n    end_time = time.time() + duration\n\n    while time.time() < end_time and not stop_event.is_set():\n        # 显示当前的旋转字符\n        sys.stdout.write(spinner[spinner_index])\n        sys.stdout.flush()\n\n        # 显示剩余时间\n        remaining_time = end_time - time.time()\n        sys.stdout.write(f\" {int(remaining_time // 60):02}:{int(remaining_time % 60):02}\")\n        sys.stdout.flush()\n\n        # 等待100毫秒\n        time.sleep(0.1)\n\n        # 将光标移回到前一个字符位置\n        sys.stdout.write('\\r')\n        sys.stdout.flush()\n\n        # 更新旋转字符索引\n        spinner_index = (spinner_index + 1) % len(spinner)\n\n    # 清除最后一个旋转字符和倒计时\n    sys.stdout.write('       ')\n    sys.stdout.flush()\n\nwhile not stop_event.is_set():\n    # 发出蜂鸣声\n    winsound.Beep(frequency, duration)\n\n    # 开始动画\n    StarAnimation(interval, stop_event)"
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_settings, f)
            return default_settings

    def init_ui(self):
        self.create_notebook()
        self.create_home_frame()
        self.create_settings_frame()

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.frame_home = ttk.Frame(self.notebook)
        self.frame_setting = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_home, text='Home')
        self.notebook.add(self.frame_setting, text='Settings')
        self.notebook.pack(expand=True, fill='both')

    def drop_filePath(self, event):
        file_path = event.data.strip('{}')
        # file_name = file_path.split("/")[-1]  # 获取文件名称
        self.file_path_entry.delete(0, tk.END)  # 清空输入框
        self.file_path_entry.insert(0, file_path)  # 插入路径

    def create_home_frame(self):
        self.current_text_label = tk.Label(self.frame_home,
                                           text="The currently selected text",
                                           font=("Helvetica", 14))
        self.current_text_label.pack(pady=10)
        self.text_area = tk.Text(
            self.frame_home,
            wrap='word',
            width=50,  # Adjusted width
            height=10)
        self.text_area.insert(tk.END, self.root.clipboard_get())
        self.text_area.config(state=tk.DISABLED)
        self.text_area.pack(padx=10, pady=10, expand=True, fill='both')

        self.file_path_label = tk.Label(self.frame_home, text="File Path:")
        self.file_path_label.pack(pady=5)
        self.file_path_entry = tk.Entry(self.frame_home, width=50)
        self.file_path_entry.insert(0, self.settings.get('Default file path'))
        self.file_path_entry.pack(pady=5)

        self.button_frame = tk.Frame(self.frame_home)
        self.button_frame.pack(pady=10)

        self.button_select_window = tk.Button(self.button_frame,
                                              text="Select Window")
        self.button_select_window.pack(side=tk.LEFT, padx=10)
        self.tooltip = CreateToolTip(self.button_select_window,
                                     "不知道如何实现让鼠标选取窗口读取窗口内文档地址址")

        self.button_select_file = tk.Button(self.button_frame,
                                            text="Select File",
                                            command=self.file_path)
        self.button_select_file.pack(side=tk.LEFT, padx=10)

        self.button_save = tk.Button(self.button_frame,
                                     text="Save Clipboard Text to File",
                                     command=self.save_clipboard_to_file)
        self.button_save.pack(side=tk.LEFT, padx=10)

        self.help_text = "Select the text, then press the shortcut key to save it to a file."
        self.toggle_frame_help = ToggleFrame(
            self.frame_home,
            label_text=self.help_text,
            button_text="How to use? - Fold / Unfold",
            content_frame_height=50)

    def file_path(self):
        self.path = filedialog.askopenfilename()
        if self.path == '':
            return
        self.file_path_entry.delete(0, tk.END)
        return self.file_path_entry.insert(tk.END, self.path)

    def create_settings_frame(self):
        self.title_label = tk.Label(self.frame_setting,
                                    text="Shortcut Configurator",
                                    font=("Helvetica", 18))
        self.title_label.pack(pady=10)
        self.settings_frame = ttk.Frame(self.frame_setting)
        self.settings_frame.pack(padx=10, pady=10, expand=True, fill='both')
        self.add_path_setting_ui('Default file path')
        self.add_shortcut_setting_ui('Quick Save', ' ')
        self.add_shortcut_setting_ui('快捷键2', ' ')

        self.save_button = tk.Button(self.frame_setting,
                                     text="Save configuration",
                                     command=self.save_settings)
        self.save_button.pack(pady=10)
        self.toggle_frame_code = ToggleFrame(
            self.frame_setting,
            label_text=self.help_text,
            button_text="Custom scripts  - Fold / Unfold",
            content_frame_height=450,
            tk_status='code',
            script=self.settings.get('script'))

    def bind_shortcuts(self, key_bind):
        keyboard.add_hotkey(key_bind, self.save_clipboard_to_file)

    def add_path_setting_ui(self, label_text):
        path_label = tk.Label(self.settings_frame, text=label_text)
        path_label.pack()
        self.path_entry = tk.Entry(self.settings_frame, width=100)
        self.path_entry.insert(
            0,
            self.settings.get('Default file path', self.file_path_entry.get()))
        self.path_entry.pack()

    def add_shortcut_setting_ui(self, label_text, default_shortcut):
        shortcut_label = tk.Label(self.settings_frame, text=label_text)
        shortcut_label.pack()
        shortcut_entry = tk.Entry(self.settings_frame)
        shortcut_entry.insert(0, self.settings.get(label_text,
                                                   default_shortcut))
        shortcut_entry.pack()
        self.shortcut_entries[label_text] = shortcut_entry

    def save_settings(self):
        self.settings['Default file path'] = self.path_entry.get()
        self.settings['Quick Save'] = self.shortcut_entries['Quick Save'].get()
        self.settings['快捷键2'] = self.shortcut_entries['快捷键2'].get()
        self.settings['script'] = self.toggle_frame_code.code.text.get(
            "1.0", tk.END).strip()
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=4, ensure_ascii=False)
        self.bind_shortcuts(self.settings['Quick Save'])
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, self.settings['Default file path'])

    def save_clipboard_to_file(self):
        try:
            keyboard.send('ctrl+c')
            time.sleep(0.2)
            clipboard_text = self.root.clipboard_get()
            file_path = self.file_path_entry.get()
            if file_path:
                mode = 'a+' if os.path.exists(file_path) and os.path.getsize(
                    file_path) > 0 else 'w'
                with open(file_path, mode, encoding='utf-8') as file:
                    file.write('\n' + '\n' + '-\t' + clipboard_text)
                winsound.Beep(1000, 500)
            else:
                messagebox.showwarning("Warning", "No file path specified")
        except tk.TclError:
            messagebox.showwarning("Warning", "No text in clipboard")

    def init_clipboard(self):
        try:
            self.last_clipboard_content = self.root.clipboard_get()
        except tk.TclError:
            self.last_clipboard_content = ""
        self.update_clipboard_content()

    def update_clipboard_content(self):
        try:
            current_clipboard_content = self.root.clipboard_get()
            if current_clipboard_content != self.last_clipboard_content:
                self.last_clipboard_content = current_clipboard_content
                self.text_area.config(state=tk.NORMAL)
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, current_clipboard_content)
                self.text_area.config(state=tk.DISABLED)
        except tk.TclError:
            pass
        self.root.after(1000, self.update_clipboard_content)


class CodeExecutorApp:

    def __init__(self, root, script):
        self.root = root
        self.script = script
        self.execution_thread = None
        self.is_executing = False
        self.stop_event = threading.Event()

        self.create_widgets()

    def create_widgets(self):
        self.text = scrolledtext.ScrolledText(self.root,
                                              wrap=tk.WORD,
                                              width=300,
                                              height=15)
        self.text.insert(tk.END, self.script)
        self.text.pack(padx=10, pady=10)
        self.execute_button = tk.Button(self.root,
                                        text="Execute",
                                        command=self.toggle_execution)
        self.execute_button.pack(side=tk.BOTTOM, pady=10)
        self.output_text = scrolledtext.ScrolledText(self.root,
                                                     wrap=tk.WORD,
                                                     width=300,
                                                     height=5)
        self.output_text.pack(padx=10, pady=10)

    def toggle_execution(self):
        if self.is_executing:
            self.stop_execution()
        else:
            self.start_execution()

    def start_execution(self):
        self.is_executing = True
        self.execute_button.config(bg="light blue")
        self.stop_event.clear()
        self.execution_thread = threading.Thread(target=self.execute_code)
        self.execution_thread.daemon = True
        self.execution_thread.start()

    def stop_execution(self):
        """Stops the execution of the code."""
        self.is_executing = False
        self.execute_button.config(bg="SystemButtonFace")
        self.stop_event.set()
        if self.execution_thread and self.execution_thread.is_alive():
            self.execution_thread.join(timeout=1)

    def execute_code(self):
        code = self.text.get("1.0", tk.END)
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            exec(code, {'stop_event': self.stop_event})
            output = sys.stdout.getvalue()
        except Exception as e:
            output = f"Error: {e}"
        finally:
            sys.stdout = old_stdout
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, output)
        self.stop_execution()


class ToggleFrame:

    def __init__(self,
                 root,
                 label_text="这是一个可以折叠的内容区域",
                 button_text="折叠/展开",
                 content_frame_height=200,
                 tk_status='normal',
                 script=''):
        self.root = root
        self.script = script
        self.content_frame_height = content_frame_height
        self.expanding = False
        self.content_frame = tk.Frame(root, height=content_frame_height)
        self.content_frame.pack_propagate(False)
        self.content_frame.pack(fill='both', expand=True)
        self.toggle_button = tk.Button(root,
                                       text=button_text,
                                       command=self.toggle_visibility,
                                       anchor='w')
        self.toggle_button.pack(fill='x')
        self.collapse()
        if tk_status == 'code':
            self.code = CodeExecutorApp(self.content_frame, self.script)
        else:
            self.text_box = tk.Label(self.content_frame,
                                     text=label_text,
                                     height=10)
            self.text_box.pack()

    def toggle_visibility(self):
        if self.expanding:
            self.collapse()
        else:
            self.expand()

    def expand(self):
        self.expanding = True
        self.content_frame.pack(fill='both', expand=True)
        self.content_frame.config(height=self.content_frame_height)

    def collapse(self):
        self.expanding = False
        self.content_frame.pack_forget()


if __name__ == "__main__":
    # root = tk.Tk()
    root = TkinterDnD.Tk()
    root.title("Clipboard to File")
    initial_width = 450
    initial_height = 650
    root.geometry(f"{initial_width}x{initial_height}")
    window_width = initial_width
    window_height = initial_height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(
        f"{window_width}x{window_height}+{position_right}+{position_top}")
    root.resizable(True, True)
    app = Home(root)
    root.mainloop()

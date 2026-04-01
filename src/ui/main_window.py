"""
OxFlow - Main Window
Universal Downloader built with CustomTkinter.
"""

# Force imports for PyInstaller discovery
import requests
import psutil
import PIL.Image
import certifi
import yt_dlp

import customtkinter as ctk
import psutil
import threading
import os
import sys
import time
import logging
from tkinter import filedialog, messagebox, Menu

from utils.i18n import I18nManager
from core.downloader import DownloadEngine
from utils.config import ConfigManager

logger = logging.getLogger(__name__)

ACCENT   = "#00e5ff"
BG_MAIN  = "#0f0f0f"
BG_PANEL = "#121212"
BG_CARD  = "#161616"
BG_ENTRY = "#1a1a1a"
BG_BTN   = "#1e1e1e"
BORDER   = "#2a2a2a"
TEXT_PRI = "#f0f0f0"
TEXT_SEC = "#888888"
TEXT_DIM = "#444444"
GREEN    = "#3fb950"
RED      = "#f85149"
ORANGE   = "#e3b341"

RESOLUTIONS = ["2160p", "1440p", "1080p", "720p", "480p", "360p"]

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.i18n = parent.i18n
        self.title(f"{self.i18n.get('settings')} — OxFlow")
        self.geometry("600x740")
        self.resizable(False, False)
        self.configure(fg_color=BG_MAIN)
        self.attributes("-topmost", True)
        self.after(200, self.focus_force)
        self._build()

    def _build(self):
        # Scrollable frame for settings
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", width=580, height=660)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))

        ctk.CTkLabel(self.scroll_frame, text=self.i18n.get("pref_title"), font=("Helvetica", 22, "bold"), text_color=ACCENT).pack(pady=(20, 20))
        
        # --- Appearance Section ---
        self._section_label(self.i18n.get("appearance"))
        app_frame = ctk.CTkFrame(self.scroll_frame, fg_color=BG_CARD, corner_radius=10); app_frame.pack(fill="x", padx=40, pady=(4, 16))
        
        # Theme
        ctk.CTkLabel(app_frame, text=self.i18n.get("theme"), font=("Helvetica", 12), text_color=TEXT_SEC).pack(anchor="w", padx=20, pady=(10, 0))
        self.theme_var = ctk.StringVar(value=self.parent.app_config.settings.get("appearance_mode", "System"))
        theme_map = {self.i18n.get("theme_light"): "Light", self.i18n.get("theme_dark"): "Dark", self.i18n.get("theme_system"): "System"}
        theme_values = [self.i18n.get("theme_light"), self.i18n.get("theme_dark"), self.i18n.get("theme_system")]
        
        display_theme = "System"
        for k, v in theme_map.items():
            if v == self.theme_var.get(): display_theme = k
            
        self.theme_menu = ctk.CTkOptionMenu(app_frame, values=theme_values, width=440, height=38, fg_color=BG_ENTRY, button_color=ACCENT, text_color=TEXT_PRI, command=self._update_theme_preview)
        self.theme_menu.set(display_theme)
        self.theme_menu.pack(pady=(4, 10), padx=20)

        # Opacity
        ctk.CTkLabel(app_frame, text=self.i18n.get("opacity"), font=("Helvetica", 12), text_color=TEXT_SEC).pack(anchor="w", padx=20, pady=(10, 0))
        self.opacity_var = ctk.DoubleVar(value=self.parent.app_config.settings.get("window_opacity", 1.0))
        self.opacity_slider = ctk.CTkSlider(app_frame, from_=0.4, to=1.0, number_of_steps=60, variable=self.opacity_var, fg_color=BG_ENTRY, progress_color=ACCENT, button_color=ACCENT, command=self._update_opacity_preview)
        self.opacity_slider.pack(pady=(4, 16), padx=20, fill="x")

        self._section_label(self.i18n.get("lang_label"))
        self.lang_var = ctk.StringVar(value=self.parent.app_config.settings["language"])
        ctk.CTkOptionMenu(self.scroll_frame, values=["en", "zh_CN", "ja"], variable=self.lang_var, width=480, height=38, fg_color=BG_ENTRY, button_color=ACCENT, text_color=TEXT_PRI).pack(pady=(4, 16))
        
        self._section_label(self.i18n.get("path_label"))
        pf = ctk.CTkFrame(self.scroll_frame, fg_color="transparent"); pf.pack(fill="x", padx=50, pady=(4, 16))
        self.path_var = ctk.StringVar(value=self.parent.app_config.settings["download_path"])
        ctk.CTkEntry(pf, textvariable=self.path_var, width=380, height=38, fg_color=BG_ENTRY, text_color=TEXT_PRI, border_color=BORDER).pack(side="left", padx=(0, 10))
        ctk.CTkButton(pf, text=self.i18n.get("browse"), width=72, height=38, fg_color=BG_BTN, border_width=1, border_color=BORDER, command=self._browse_path).pack(side="left")
        
        self._section_label(self.i18n.get("ffmpeg_label"))
        ff = ctk.CTkFrame(self.scroll_frame, fg_color="transparent"); ff.pack(fill="x", padx=50, pady=(4, 16))
        self.ffmpeg_var = ctk.StringVar(value=self.parent.app_config.settings.get("ffmpeg_path", ""))
        ctk.CTkEntry(ff, textvariable=self.ffmpeg_var, width=380, height=38, fg_color=BG_ENTRY, text_color=TEXT_PRI, border_color=BORDER).pack(side="left", padx=(0, 10))
        ctk.CTkButton(ff, text=self.i18n.get("browse"), width=72, height=38, fg_color=BG_BTN, border_width=1, border_color=BORDER, command=self._browse_ffmpeg).pack(side="left")
        
        self._section_label(self.i18n.get("proxy_label"))
        self.proxy_var = ctk.StringVar(value=self.parent.app_config.settings.get("proxy_url", ""))
        ctk.CTkEntry(self.scroll_frame, textvariable=self.proxy_var, width=480, height=38, fg_color=BG_ENTRY, text_color=ACCENT, border_color=BORDER, placeholder_text="http://127.0.0.1:7890").pack(pady=(4, 16))

        self._section_label(self.i18n.get("cookies_label"))
        self.cookies_var = ctk.StringVar(value=self.parent.app_config.settings.get("cookies_browser", "none"))
        # 增加 None 选项
        cookie_options = ["none", "chrome", "safari", "edge", "firefox", "opera", "vivaldi"]
        self.cookies_menu = ctk.CTkOptionMenu(self.scroll_frame, values=cookie_options, variable=self.cookies_var, width=160, height=38, fg_color=BG_ENTRY, button_color=ACCENT, text_color=TEXT_PRI)
        self.cookies_menu.pack(pady=(4, 16), anchor="w", padx=60)

        self._section_label(self.i18n.get("quality_label"))
        self.quality_var = ctk.StringVar(value=self.parent.app_config.settings.get("default_quality", "1080p"))
        ctk.CTkOptionMenu(self.scroll_frame, values=RESOLUTIONS, variable=self.quality_var, width=160, height=38, fg_color=BG_ENTRY, button_color=ACCENT, text_color=TEXT_PRI).pack(pady=(4, 16), anchor="w", padx=60)
        
        lp_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent"); lp_frame.pack(fill="x", padx=60, pady=(0, 24))
        self.low_power_var = ctk.BooleanVar(value=self.parent.app_config.settings.get("low_power_mode", False))
        ctk.CTkCheckBox(lp_frame, text=self.i18n.get("low_power"), variable=self.low_power_var, fg_color=ACCENT, text_color=TEXT_PRI).pack(side="left")
        
        ctk.CTkButton(self.scroll_frame, text=self.i18n.get("save_apply"), height=52, width=320, fg_color=ACCENT, text_color="#000000", font=("Helvetica", 16, "bold"), corner_radius=26, command=self._apply).pack(pady=(30, 60))

    def _section_label(self, text): ctk.CTkLabel(self.scroll_frame, text=text, font=("Helvetica", 13, "bold"), text_color=TEXT_SEC).pack(anchor="w", padx=60, pady=(15, 5))
    
    def _update_theme_preview(self, val):
        theme_map = {self.i18n.get("theme_light"): "Light", self.i18n.get("theme_dark"): "Dark", self.i18n.get("theme_system"): "System"}
        ctk.set_appearance_mode(theme_map.get(val, "System"))
        
    def _update_opacity_preview(self, val):
        self.parent.attributes("-alpha", float(val))
        self.attributes("-alpha", float(val))

    def _browse_path(self):
        path = filedialog.askdirectory(initialdir=self.path_var.get())
        if path: self.path_var.set(path)
    def _browse_ffmpeg(self):
        path = filedialog.askdirectory(title="Select FFmpeg bin directory", initialdir=self.ffmpeg_var.get() or "/usr/local/bin")
        if path: self.ffmpeg_var.set(path)
    def _apply(self):
        theme_map = {self.i18n.get("theme_light"): "Light", self.i18n.get("theme_dark"): "Dark", self.i18n.get("theme_system"): "System"}
        self.parent.app_config.save({
            "language": self.lang_var.get(), 
            "download_path": self.path_var.get(), 
            "ffmpeg_path": self.ffmpeg_var.get(), 
            "proxy_url": self.proxy_var.get(),
            "cookies_browser": self.cookies_var.get(),
            "default_quality": self.quality_var.get(), 
            "low_power_mode": self.low_power_var.get(),
            "appearance_mode": theme_map.get(self.theme_menu.get(), "System"),
            "window_opacity": self.opacity_var.get()
        })
        self.parent.update_global_config()
        self.destroy()

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        try:
            self._init_state()
            self._init_window()
            self._load_icon()
            self._build_ui()
            self._create_menus()
            self._refresh_texts()
            self._start_monitor()
            self.after(400, self._force_focus)
        except Exception as e:
            logger.exception("Startup error")
            messagebox.showerror("OxFlow — Error", str(e))

    def _init_state(self):
        self.app_config = ConfigManager()
        self.i18n = I18nManager(lang=self.app_config.settings["language"])
        self.engine = DownloadEngine(
            progress_callback=self._on_progress, 
            log_callback=self._on_log, 
            ffmpeg_path=self.app_config.settings.get("ffmpeg_path"), 
            max_retries=self.app_config.settings.get("max_retries", 10), 
            concurrent_fragments=self.app_config.settings.get("concurrent_fragments", 4),
            proxy=self.app_config.settings.get("proxy_url"),
            cookies_browser=self.app_config.settings.get("cookies_browser")
        )
        self.selected_res = self.app_config.settings.get("default_quality", "1080p")
        self.video_info = None
        self.is_downloading = False
        self.is_analyzing = False
        self.current_percent = "0%"
        self._monitor_running = True
        self._download_start_time = None

    def _init_window(self):
        self.title("OxFlow")
        self.geometry("1140x820")
        self.minsize(900, 680)
        self.configure(fg_color=BG_MAIN)
        ctk.set_appearance_mode(self.app_config.settings.get("appearance_mode", "Dark"))
        self.attributes("-alpha", self.app_config.settings.get("window_opacity", 1.0))

    def _load_icon(self):
        try:
            icon_path = "icon.png"
            if hasattr(sys, "_MEIPASS"):
                icon_path = os.path.join(sys._MEIPASS, "icon.png")
            else:
                icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "icon.png")

            if os.path.exists(icon_path):
                from PIL import Image
                img = ctk.CTkImage(Image.open(icon_path), size=(32, 32))
                self.after(250, lambda: self.wm_iconphoto(True, img._light_image))
        except Exception as e:
            logger.error(f"Failed to load icon: {e}")

    def _create_menus(self):
        menubar = Menu(self); self.configure(menu=menubar)
        em = Menu(menubar, tearoff=0, background="#1a1a1a", foreground="white"); menubar.add_cascade(label="Edit", menu=em)
        em.add_command(label="Cut", accelerator="Cmd+X", command=self._cut)
        em.add_command(label="Copy", accelerator="Cmd+C", command=self._copy)
        em.add_command(label="Paste", accelerator="Cmd+V", command=self._paste)
        em.add_separator()
        em.add_command(label="Select All", command=self._select_all)

    def _show_context_menu(self, event):
        self.url_entry.focus_set()
        m = Menu(self, tearoff=0, background=BG_CARD, foreground=TEXT_PRI, activebackground=ACCENT, activeforeground="#000000")
        m.add_command(label=f"✂  {self.i18n.get('cut')}", command=self._cut)
        m.add_command(label=f"⎘  {self.i18n.get('copy')}", command=self._copy)
        m.add_command(label=f"⏎  {self.i18n.get('paste')}", command=self._paste)
        m.add_separator()
        m.add_command(label=f"☰  {self.i18n.get('select_all')}", command=self._select_all)
        m.tk_popup(event.x_root, event.y_root)

    def _select_all(self, event=None):
        self.url_entry.focus_set()
        self.url_entry.select_range(0, "end")
        self.url_entry.icursor("end")
        self.url_entry.xview("end")
        return "break"

    def _build_ui(self):
        self._build_topbar()
        self._build_url_bar()
        self._build_main_area()
        self._build_status_bar()

    def _build_topbar(self):
        tb = ctk.CTkFrame(self, height=60, fg_color=BG_CARD, corner_radius=0); tb.pack(fill="x"); tb.pack_propagate(False)
        left = ctk.CTkFrame(tb, fg_color="transparent"); left.pack(side="left", padx=24, pady=10)
        self.brand_lbl = ctk.CTkLabel(left, text="OXFLOW", font=("Helvetica", 19, "bold"), text_color=ACCENT); self.brand_lbl.pack(side="left")
        self.ver_lbl = ctk.CTkLabel(left, text=f"  {self.i18n.version}", font=("Helvetica", 11), text_color=TEXT_DIM); self.ver_lbl.pack(side="left", pady=(3, 0))
        right = ctk.CTkFrame(tb, fg_color="transparent"); right.pack(side="right", padx=20)
        self.open_folder_btn = ctk.CTkButton(right, text="📂", width=40, height=36, fg_color=BG_BTN, border_width=1, border_color=BORDER, command=self._open_download_folder); self.open_folder_btn.pack(side="left", padx=(0, 10))
        self.settings_btn = ctk.CTkButton(right, text="⚙️", width=40, height=36, font=("Helvetica", 18), fg_color=BG_BTN, border_width=1, border_color=BORDER, text_color=TEXT_PRI, command=self._open_settings); self.settings_btn.pack(side="left")
        self.path_lbl = ctk.CTkLabel(tb, text="", font=("Helvetica", 12), text_color=TEXT_SEC, cursor="hand2"); self.path_lbl.pack(side="left", padx=25); self.path_lbl.bind("<Button-1>", lambda _: self._open_settings())

    def _build_url_bar(self):
        frame = ctk.CTkFrame(self, fg_color="transparent"); frame.pack(fill="x", padx=40, pady=(20, 12))
        self.url_entry = ctk.CTkEntry(frame, height=52, fg_color=BG_ENTRY, border_color=BORDER, text_color=ACCENT, font=("Helvetica", 14)); self.url_entry.pack(side="left", fill="x", expand=True)
        self.url_entry.bind("<Return>", lambda _: self._start_analyze())
        self.url_entry.bind("<Button-2>", self._show_context_menu)
        self.url_entry.bind("<Button-3>", self._show_context_menu)
        self.url_entry.bind("<Command-a>", self._select_all)
        self.url_entry.bind("<Control-a>", self._select_all)
        self.analyze_btn = ctk.CTkButton(frame, text="ANALYZE", width=140, height=52, fg_color=ACCENT, text_color="#000000", font=("Helvetica", 13, "bold"), command=self._start_analyze); self.analyze_btn.pack(side="right", padx=(14, 0))

    def _build_main_area(self):
        mc = ctk.CTkFrame(self, fg_color="transparent"); mc.pack(fill="both", expand=True, padx=40, pady=0)
        mc.columnconfigure(0, weight=3); mc.columnconfigure(1, weight=2)
        panel = ctk.CTkFrame(mc, fg_color=BG_PANEL, border_width=1, border_color=BORDER, corner_radius=12); panel.grid(row=0, column=0, sticky="nsew", padx=(0, 16), pady=(0, 16))
        self.thumb_frame = ctk.CTkFrame(panel, fg_color="transparent", height=160); self.thumb_frame.pack(fill="x", padx=24, pady=(24, 0)); self.thumb_frame.pack_propagate(False)
        self.thumb_lbl = ctk.CTkLabel(self.thumb_frame, text="", text_color=TEXT_DIM); self.thumb_lbl.pack(expand=True)
        self.video_lbl = ctk.CTkLabel(panel, text="", font=("Helvetica", 15, "bold"), text_color=TEXT_DIM, wraplength=460); self.video_lbl.pack(pady=(10, 4), padx=24)
        self.meta_lbl = ctk.CTkLabel(panel, text="", font=("Helvetica", 11), text_color=TEXT_SEC); self.meta_lbl.pack(pady=(0, 16))
        ctk.CTkFrame(panel, height=1, fg_color=BORDER).pack(fill="x", padx=24, pady=(0, 16))
        rg = ctk.CTkFrame(panel, fg_color="transparent"); rg.pack()
        self.res_btns = {}
        for i, res in enumerate(RESOLUTIONS):
            r, c = divmod(i, 3)
            btn = ctk.CTkButton(rg, text=res, width=108, height=46, fg_color=BG_BTN, border_width=1, border_color=BORDER, text_color=TEXT_SEC, state="disabled", command=lambda v=res: self._select_res(v))
            btn.grid(row=r, column=c, padx=8, pady=6); self.res_btns[res] = btn
        self.audio_btn = ctk.CTkButton(panel, text="MP3", width=340, height=46, fg_color=BG_BTN, border_width=1, border_color=BORDER, text_color=TEXT_SEC, state="disabled", command=lambda: self._select_res("mp3")); self.audio_btn.pack(pady=(6, 20))
        log_panel = ctk.CTkFrame(mc, fg_color=BG_PANEL, border_width=1, border_color=BORDER, corner_radius=12); log_panel.grid(row=0, column=1, sticky="nsew", pady=(0, 16))
        self.log_box = ctk.CTkTextbox(log_panel, fg_color="#0a0a0a", text_color=GREEN, font=("Courier", 11)); self.log_box.pack(fill="both", expand=True, padx=10, pady=10)

    def _build_status_bar(self):
        sb = ctk.CTkFrame(self, height=76, fg_color=BG_CARD, corner_radius=0); sb.pack(side="bottom", fill="x"); sb.pack_propagate(False)
        self.prog_bar = ctk.CTkProgressBar(sb, height=6, progress_color=ACCENT, fg_color="#222222"); self.prog_bar.pack(fill="x", padx=40, pady=(14, 4)); self.prog_bar.set(0)
        br = ctk.CTkFrame(sb, fg_color="transparent"); br.pack(fill="x", padx=40)
        self.stats_lbl = ctk.CTkLabel(br, text="IDLE", font=("Helvetica", 11), text_color=TEXT_DIM); self.stats_lbl.pack(side="left")
        self.eta_lbl = ctk.CTkLabel(br, text="", font=("Helvetica", 11), text_color=TEXT_SEC); self.eta_lbl.pack(side="left", padx=20)
        self.download_btn = ctk.CTkButton(br, text="DOWNLOAD", width=170, height=40, fg_color=ACCENT, text_color="#000000", font=("Helvetica", 13, "bold"), state="disabled", command=self._handle_download_action); self.download_btn.pack(side="right")

    def _refresh_texts(self):
        self.title(self.i18n.get("title")); self.brand_lbl.configure(text=self.i18n.get("brand").upper()); 
        self.url_entry.configure(placeholder_text=self.i18n.get("placeholder")); self.analyze_btn.configure(text=self.i18n.get("analyze"))
        self.download_btn.configure(text=self.i18n.get("cancel") if self.is_downloading else self.i18n.get("download"))
        self.audio_btn.configure(text=self.i18n.get("audio_only"))
        self.path_lbl.configure(text=f"📂  {self.app_config.settings['download_path']}")
        if not self.video_info: self.video_lbl.configure(text=self.i18n.get("ready"))
        self.ver_lbl.configure(text=f"  {self.i18n.version}")

    def update_global_config(self):
        s = self.app_config.settings
        self.i18n.set_language(s["language"])
        self.engine.ffmpeg_path = s.get("ffmpeg_path") or self.engine.ffmpeg_path
        self.engine.proxy = s.get("proxy_url")
        self.engine.cookies_browser = s.get("cookies_browser")
        ctk.set_appearance_mode(s.get("appearance_mode", "Dark"))
        self.attributes("-alpha", s.get("window_opacity", 1.0))
        self._refresh_texts()
        self._on_log(f"[CONFIG] Sync: {s['language']} " + (f"(Proxy: ON)" if self.engine.proxy else "") + f" (Opacity: {s.get('window_opacity', 1.0)})")

    def _open_settings(self): SettingsWindow(self)
    def _open_download_folder(self):
        p = self.app_config.settings.get("download_path")
        if os.path.isdir(p):
            import subprocess, platform
            if platform.system() == "Darwin": subprocess.Popen(["open", p])
            elif platform.system() == "Windows": subprocess.Popen(["explorer", p])
            else: subprocess.Popen(["xdg-open", p])

    def _cut(self): self._copy(); self.url_entry.delete(0, "end")
    def _copy(self):
        try: self.clipboard_clear(); self.clipboard_append(self.url_entry.get())
        except: pass
    def _paste(self):
        try:
            t = self.clipboard_get().strip()
            if t: self.url_entry.delete(0, "end"); self.url_entry.insert(0, t); self._clean_pasted_url()
        except: pass
    def _clean_pasted_url(self):
        t = self.url_entry.get().strip()
        if "youtube.com/watch?v=" in t and "&list=" in t:
            t = t.split("&list=")[0]; self.url_entry.delete(0, "end"); self.url_entry.insert(0, t)

    def _start_analyze(self):
        u = self.url_entry.get().strip()
        if not u or self.is_analyzing: return
        self._clean_pasted_url(); u = self.url_entry.get().strip()
        self.is_analyzing = True; self.video_info = None
        self.analyze_btn.configure(state="disabled", text=self.i18n.get("parsing")); self.video_lbl.configure(text=self.i18n.get("parsing"), text_color=ACCENT); self.meta_lbl.configure(text=""); self.thumb_lbl.configure(image=None)
        self._on_log(f"[ANALYZE] {u}")
        threading.Thread(target=self._run_analyze, args=(u,), daemon=True).start()

    def _run_analyze(self, url):
        try:
            info = self.engine.get_info(url); self.video_info = info
            self.after(0, lambda: self._display_info(info))
        except Exception as e:
            self._on_log(f"[ERROR] {e}"); self.after(0, lambda: self.analyze_btn.configure(state="normal", text=self.i18n.get("analyze")))
        finally: self.is_analyzing = False

    def _display_info(self, info):
        self.analyze_btn.configure(state="normal", text=self.i18n.get("analyze"))
        t = info.get("title", "File")
        if info.get("is_direct"):
            sz = self.engine.format_size(info.get("filesize", 0)) if info.get("filesize") else self.i18n.get("size_unknown")
            self.video_lbl.configure(text=t, text_color=TEXT_PRI); self.meta_lbl.configure(text=f"{info.get('ext','').upper()} · {sz}")
        else:
            d = self.engine.format_eta(info.get("duration")) if info.get("duration") else ""
            self.video_lbl.configure(text=t[:80], text_color=TEXT_PRI); self.meta_lbl.configure(text=f"{info.get('uploader','')} · {d}")
            tu = info.get("thumbnail")
            if tu: threading.Thread(target=self._load_thumbnail, args=(tu,), daemon=True).start()
        self._activate_format_ui(info)

    def _load_thumbnail(self, url):
        try:
            import requests as req; from PIL import Image; import io
            r = req.get(url, timeout=10); img = Image.open(io.BytesIO(r.content)); img.thumbnail((300, 168), Image.LANCZOS)
            ctk_img = ctk.CTkImage(img, size=(img.width, img.height))
            self.after(0, lambda: self.thumb_lbl.configure(image=ctk_img, text=""))
        except: pass

    def _activate_format_ui(self, info):
        self.download_btn.configure(state="normal")
        if info.get("is_direct"):
            for b in self.res_btns.values(): b.configure(state="disabled", text="—")
            ext = info.get("ext", "FILE").upper()
            fb = list(self.res_btns.values())[0]; fb.configure(state="normal", text=ext, border_color=ACCENT, text_color=ACCENT)
            self.audio_btn.configure(state="normal", text=self.i18n.get("direct_download"), border_color=BORDER, text_color=TEXT_PRI)
            self.selected_res = "direct"
        else:
            for r, b in self.res_btns.items(): b.configure(state="normal", text=r, border_color=BORDER, text_color=TEXT_PRI)
            self.audio_btn.configure(state="normal", text=self.i18n.get("audio_only"), border_color=BORDER, text_color=TEXT_PRI)
            if self.selected_res in ("direct", "mp3"): self.selected_res = self.app_config.settings.get("default_quality", "1080p")
            self._select_res(self.selected_res)

    def _select_res(self, res):
        if self.video_info and self.video_info.get("is_direct"): return
        self.selected_res = res
        for b in self.res_btns.values(): b.configure(border_color=BORDER, text_color=TEXT_PRI)
        self.audio_btn.configure(border_color=BORDER, text_color=TEXT_PRI)
        if res == "mp3": self.audio_btn.configure(border_color=ACCENT, text_color=ACCENT)
        elif res in self.res_btns: self.res_btns[res].configure(border_color=ACCENT, text_color=ACCENT)

    def _handle_download_action(self):
        if self.is_downloading: self.engine.cancel(); self._reset_download_ui()
        else: self._start_download()

    def _start_download(self):
        if not self.video_info: return
        self.is_downloading = True; self._download_start_time = time.monotonic()
        # 优化：开始下载后释放解析按钮，允许连续添加任务
        self.analyze_btn.configure(state="normal")
        self.download_btn.configure(text=self.i18n.get("cancel"), fg_color=BG_BTN, hover_color=BG_ENTRY, text_color=TEXT_PRI)
        opts = {"outtmpl": os.path.join(self.app_config.settings["download_path"], "%(title)s.%(ext)s"), "resolution": self.selected_res, "audio_only": (self.selected_res == "mp3"), "is_direct": self.video_info.get("is_direct", False), "title": self.video_info.get("title", "file")}
        self.engine.download(self.url_entry.get().strip(), opts)

    def _on_progress(self, d):
        try:
            p = float(d.get("_percent_str", "0%").replace("%",""))
            self.after(0, lambda: self.prog_bar.set(p / 100))
            self.after(0, lambda: self.stats_lbl.configure(text=f"CPU: {psutil.cpu_percent():.0f}% MEM: {psutil.virtual_memory().percent:.0f}% ↓ {d.get('_speed_str','—')} {p:.1f}%"))
            if d.get("_eta_str"): self.after(0, lambda: self.eta_lbl.configure(text=f"ETA {d['_eta_str']}"))
        except: pass

    def _reset_download_ui(self):
        self.is_downloading = False; self.download_btn.configure(text=self.i18n.get("download"), fg_color=ACCENT)
        self.prog_bar.set(0); self.eta_lbl.configure(text="")

    def _on_log(self, msg):
        self.after(0, lambda: (self.log_box.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n"), self.log_box.see("end")))
        if "[SUCCESS]" in msg: self._reset_download_ui(); self.prog_bar.set(1.0); self.eta_lbl.configure(text="✓", text_color=GREEN); self._save_history()
        elif "[ERROR]" in msg: self._reset_download_ui(); self.eta_lbl.configure(text="✗", text_color=RED)

    def _save_history(self):
        if self.video_info: self.app_config.add_history({"title": self.video_info.get("title", "Unknown"), "url": self.url_entry.get().strip(), "resolution": self.selected_res, "time": time.strftime("%Y-%m-%d %H:%M:%S")})

    def _start_monitor(self):
        def _loop():
            while self._monitor_running:
                if not self.is_downloading:
                    self.after(0, lambda: self.stats_lbl.configure(text=f"CPU: {psutil.cpu_percent():.0f}% MEM: {psutil.virtual_memory().percent:.0f}% — IDLE"))
                time.sleep(5.0 if self.app_config.settings.get("low_power_mode") else 2.0)
        threading.Thread(target=_loop, daemon=True).start()

    def _force_focus(self): self.focus_force(); self.url_entry.focus_set()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = MainWindow(); app.mainloop()

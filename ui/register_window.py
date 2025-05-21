import tkinter as tk
from tkinter import messagebox, font
from utils.styles import COLORS

class RegisterWindow:
    def __init__(self, parent_frame, show_login_callback, controller):
        self.parent_frame = parent_frame
        self.show_login_callback = show_login_callback
        self.controller = controller
        self.title_font = font.Font(family="Helvetica", size=22, weight="bold")
        self.subtitle_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=10)
        self.create_register_widgets()

    def create_register_widgets(self):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        title_frame = tk.Frame(self.parent_frame, bg=COLORS['fondo'])
        title_frame.pack(pady=20)
        tk.Label(title_frame, text="NutriPlan", font=self.title_font, 
                 bg=COLORS['fondo'], fg=COLORS['morado']).pack()

        # Formulario de registro
        register_frame = tk.Frame(self.parent_frame, bg=COLORS['blanco'], padx=30, pady=30,
                                  relief=tk.RIDGE, bd=1)
        register_frame.pack(expand=True, padx=50, fill=tk.BOTH)  
        tk.Label(register_frame, text="Crear una cuenta", font=self.subtitle_font,
                 bg=COLORS['blanco'], fg=COLORS['texto_oscuro']).pack(pady=(0, 20))

        labels = [
            "Nombre completo:",
            "Correo electrónico:",
            "Nombre de usuario:",
            "Contraseña:",
            "Confirmar contraseña:"
        ]
        entries = []
        for idx, text in enumerate(labels):
            tk.Label(register_frame, text=text, anchor=tk.W,
                     bg=COLORS['blanco'], fg=COLORS['texto_oscuro']).pack(fill=tk.X)
            if "contraseña" in text.lower():
                entry = tk.Entry(register_frame, font=self.normal_font, show="•")
            else:
                entry = tk.Entry(register_frame, font=self.normal_font)
            entry.pack(
                fill=tk.X,
                pady=(0, 10) if idx < len(labels) - 1 else (0, 20)
            )
            entries.append(entry)

        (self.fullname_entry,
         self.email_entry,
         self.reg_username_entry,
         self.reg_password_entry,
         self.confirm_password_entry) = entries

        buttons_frame = tk.Frame(register_frame, bg=COLORS['blanco'])
        buttons_frame.pack(fill=tk.X, pady=10)

        back_button = tk.Button(buttons_frame, text="Volver", font=self.normal_font,
                                bg=COLORS['borde'], fg=COLORS['texto_oscuro'],
                                relief=tk.FLAT, padx=15, pady=8,
                                command=self.show_login_callback)
        back_button.pack(side=tk.LEFT, padx=(0, 10))

        register_button = tk.Button(buttons_frame, text="Registrar usuario", font=self.normal_font,
                                    bg=COLORS['morado'], fg=COLORS['texto_claro'],
                                    activebackground=COLORS['morado'], activeforeground=COLORS['texto_claro'],
                                    relief=tk.FLAT, padx=15, pady=8,
                                    command=self.register)
        register_button.pack(side=tk.RIGHT)

    def register(self):
        fullname = self.fullname_entry.get()
        email = self.email_entry.get()
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not all([fullname, email, username, password, confirm_password]):
            messagebox.showerror("Error", "Por favor completa todos los campos")
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        self.controller.register_user(fullname, email, username, password)

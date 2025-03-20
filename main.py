# © 2025 B0rx. All rights reserved.
# Version: 1.0.0 Beta / 20.03.2025 /

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import subprocess

class FirewallRuleCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Firewall Rule Creator")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.exe_path = ctk.StringVar()
        self.rule_name = ctk.StringVar()
        self.direction = ctk.StringVar(value="both")
        self.action = ctk.StringVar(value="block")
        self.domain = ctk.BooleanVar(value=True)
        self.private = ctk.BooleanVar(value=True)
        self.public = ctk.BooleanVar(value=True)
        self.create_widgets()

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        title_label = ctk.CTkLabel(
            main_frame,
            text="Firewall Rule Creator",
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"))
        title_label.pack(pady=(0, 20))

        program_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        program_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(program_frame, text="Select Program:").pack(anchor="w")
        entry = ctk.CTkEntry(program_frame, textvariable=self.exe_path, width=350)
        entry.pack(side="left", pady=5, padx=(0, 10))
        ctk.CTkButton(program_frame, text="Browse", command=self.browse_exe, width=100).pack(side="left")

        name_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(name_frame, text="Rule Name:").pack(anchor="w")
        ctk.CTkEntry(name_frame, textvariable=self.rule_name, width=350).pack(pady=5, anchor="w")

        action_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        action_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(action_frame, text="Action:").pack(anchor="w")
        ctk.CTkRadioButton(action_frame, text="Block", value="block", variable=self.action).pack(anchor="w", pady=5)
        ctk.CTkRadioButton(action_frame, text="Allow", value="allow", variable=self.action).pack(anchor="w", pady=5)

        combined_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        combined_frame.pack(fill="x", pady=10)

        direction_frame = ctk.CTkFrame(combined_frame, fg_color="transparent")
        direction_frame.pack(side="left", fill="y", padx=(0, 20))

        ctk.CTkLabel(direction_frame, text="Direction:").pack(anchor="w")
        ctk.CTkRadioButton(direction_frame, text="Inbound", value="in", variable=self.direction).pack(anchor="w", pady=5)
        ctk.CTkRadioButton(direction_frame, text="Outbound", value="out", variable=self.direction).pack(anchor="w", pady=5)
        ctk.CTkRadioButton(direction_frame, text="Both", value="both", variable=self.direction).pack(anchor="w", pady=5)

        profile_frame = ctk.CTkFrame(combined_frame, fg_color="transparent")
        profile_frame.pack(side="right", fill="y")

        ctk.CTkLabel(profile_frame, text="Profiles:").pack(anchor="w")
        ctk.CTkCheckBox(profile_frame, text="Domain", variable=self.domain).pack(anchor="w", pady=5)
        ctk.CTkCheckBox(profile_frame, text="Private", variable=self.private).pack(anchor="w", pady=5)
        ctk.CTkCheckBox(profile_frame, text="Public", variable=self.public).pack(anchor="w", pady=5)

        ctk.CTkButton(
            main_frame,
            text="Create Rule",
            command=self.create_rule,
            fg_color="#2b2b2b",
            hover_color="#424242",
            border_color="#1f538d",
            border_width=2,
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            height=40).pack(pady=15)

    def browse_exe(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")])
        if file_path:
            self.exe_path.set(file_path)
            default_name = os.path.splitext(os.path.basename(file_path))[0]
            self.rule_name.set(default_name)

    def check_rule_exists(self, name, direction):
        """Check if a rule with the given name and direction already exists."""
        try:
            cmd = f'netsh advfirewall firewall show rule name="{name}" dir={direction}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if "No rules match the specified criteria" not in result.stdout:
                return True
            return False
        except subprocess.CalledProcessError:
            return False

    def create_rule(self):
        if not self.exe_path.get():
            messagebox.showerror("Error", "Please select an EXE file!", parent=self.root)
            return
        if not self.rule_name.get():
            messagebox.showerror("Error", "Please enter a rule name!", parent=self.root)
            return
        if not (self.domain.get() or self.private.get() or self.public.get()):
            messagebox.showerror("Error", "Please select at least one profile!", parent=self.root)
            return

        try:
            direction = self.direction.get()
            action = self.action.get()
            program = self.exe_path.get()
            name = self.rule_name.get()

            if not os.path.exists(program):
                messagebox.showerror("Error", f"The file {program} does not exist!", parent=self.root)
                return
            
            program = program.replace("/", "\\")
            base_cmd = 'netsh advfirewall firewall add rule'
            delete_cmd = 'netsh advfirewall firewall delete rule'

            profiles = []
            if self.domain.get():
                profiles.append("domain")
            if self.private.get():
                profiles.append("private")
            if self.public.get():
                profiles.append("public")
            profiles_str = ",".join(profiles)

            rule_exists = False
            directions_to_check = []
            if direction in ["in", "both"]:
                directions_to_check.append("in")
            if direction in ["out", "both"]:
                directions_to_check.append("out")
            for dir in directions_to_check:
                if self.check_rule_exists(name, dir):
                    rule_exists = True
                    break

            if rule_exists:
                response = messagebox.askyesno(
                    "Rule Exists",
                    f"A rule with the name '{name}' already exists. Do you want to overwrite it?",
                    parent=self.root)
                
                if not response:
                    messagebox.showinfo("Info", "Please choose a different rule name.", parent=self.root)
                    return

                for dir in directions_to_check:
                    subprocess.run(f'{delete_cmd} name="{name}" dir={dir}', shell=True, check=False)

            if direction in ["in", "both"]:
                cmd_in = f'{base_cmd} name="{name}" dir=in action={action} program="{program}" profile={profiles_str}'
                subprocess.run(cmd_in, shell=True, check=True)

            if direction in ["out", "both"]:
                cmd_out = f'{base_cmd} name="{name}" dir=out action={action} program="{program}" profile={profiles_str}'
                subprocess.run(cmd_out, shell=True, check=True)

            messagebox.showinfo("Success", "Firewall rule(s) successfully created!", parent=self.root)
            
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error creating rule: {str(e)}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Unknown error: {str(e)}", parent=self.root)

def main():
    root = ctk.CTk()
    app = FirewallRuleCreator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
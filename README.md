# 🔥 FirewallRuleCreator

**FirewallRuleCreator** is a simple Windows tool that allows you to quickly add or remove firewall rules without manually navigating through advanced firewall settings.

## 🚀 Features
✅ Block or allow connections for any `.exe` file  
✅ Supports **inbound**, **outbound**, or **both** directions  
✅ Choose profiles: **Domain, Private, Public**  
✅ Prevents duplicate rules by checking existing ones  
✅ Simple & clean UI using `CustomTkinter`  
✅ No installation required – just run the `.exe`  

## 📥 Download & Installation
1. **Download** `FirewallRuleCreator.exe` from the [Releases](https://github.com/b0rx/FirewallRuleCreator/releases) page.  
2. Run the `.exe` – **No installation required!**  

🔴 **Note:** You must run the program as **Administrator** to modify firewall rules.

## 🎮 How to Use
1. Open the program and **select an `.exe` file** you want to block/allow.  
2. Choose the **rule name**, **action (Allow/Block)**, and **direction (Inbound/Outbound)**.  
3. Click **"Create Rule"** – Done! 🎉  

## 🛠 Building from Source
If you want to modify or compile the program yourself, follow these steps:

### 1️⃣ Install Dependencies:
```bash
pip install customtkinter

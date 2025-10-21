## 💡 waybar-pomodoro-rgb-sync
Synchronization of the HP Omen keyboard's RGB backlighting with the Pomodoro timer state in Waybar.

The project uses a simple Python script to monitor flag files managed by Waybar and change the keyboard's backlight color

🔴 — Work

🟢 — Break

🟡 — Inactive/Reset).

-----

## 🚀 Features

  * **Visual Cue:** Instant keyboard color change based on the Pomodoro mode.
    
  * **Flexibility:** Uses a flag file mechanism (`/tmp/pomodoro_*_flag`) for reliable communication between the Waybar module and the backlight controller.
    
  * **Compatibility:** Developed for Waybar (Hyprland/Sway) and HP OMEN laptops with the system driver `/sys/devices/platform/hp-wmi/rgb_zones/zone00`.

-----

## ⚙️ Requirements

1.  **Waybar** (Wayland Bar)
2.  **waybar-module-pomodoro** (Installed and compiled).
3.  **Python 3** and **Bash**.
4.  **Sudoers Rights:** Your user must have **passwordless sudo** rights to write to `/sys/devices/platform/hp-wmi/rgb_zones/zone00`.

-----

## 💾 Installation

### 1\. Prepare the Pomodoro Module

Install necessary dependencies (`rust`, `base-devel`, etc.) and build the module from [Andeskjerf/waybar-module-pomodoro](https://github.com/Andeskjerf/waybar-module-pomodoro).

```bash
# Clone and compile the module
git clone https://github.com/Andeskjerf/waybar-module-pomodoro.git
cd waybar-module-pomodoro
cargo build --release

# Install the binary to $PATH
cp target/release/waybar-module-pomodoro ~/.local/bin/
```

### 2\. Install Synchronization Scripts

Create two files (`.py` and `.sh`) in the `~/.local/bin/` directory to manage the backlight and flags.

#### 2.1. RGB Controller (Python): `~/.local/bin/pomodoro_rgb_ctl.py`

#### 2.2. Toggle Script (Bash): `~/.local/bin/pomodoro_flag_toggle.sh`

*Create these files and paste the code that manages the Pomodoro state switching and creates/deletes the flag files.*

#### 2.3. Permissions

Make both scripts executable:

```bash
chmod +x ~/.local/bin/pomodoro_rgb_ctl.py
chmod +x ~/.local/bin/pomodoro_flag_toggle.sh
```

-----

### 3\. Waybar Configuration

#### 3.1. `~/.config/waybar/config`

Add the `custom/pomodoro` module definition and include it in the desired section (`modules-center`).

Note that `on-click` and `on-click-right` now call the scripts to manage the flags.

```json
// --- Module Definition ---
"custom/pomodoro": {
    "format": "{}",
    "return-type": "json",
    
    "exec": "waybar-module-pomodoro --autob --autow",
    "on-click": "~/.local/bin/pomodoro_flag_toggle.sh",
    "on-click-right": "waybar-module-pomodoro reset; rm -f /tmp/pomodoro_work_flag /tmp/pomodoro_break_flag /tmp/pomodoro_pause_flag",
    "tooltip": true
},

// --- Example placement in the modules-center section ---
"group/pill#center": {
    "orientation": "inherit",
    "modules": [
        // ... other modules ...
        "custom/pomodoro", 
        // ... other modules ...
    ]
},
```

#### 3.2. `~/.config/waybar/user-style.css`

Add styles to change the color of the text in the Pomodoro module to synchronize with the keyboard colors.

```css
/* ============================================== */
/* Pomodoro Module Styling (TEXT COLOR ONLY) */
/* ============================================== */

/* Base style (YELLOW - reset/inactive state) */
#custom-pomodoro { 
    color: #FEE715; 
}

/* Style for the work cycle (RED) */
#custom-pomodoro.work { 
    color: #FF6347; 
}

/* Style for the break cycle (GREEN) */
#custom-pomodoro.break { 
    color: #3CB371; 
}

/* Pause */
#custom-pomodoro.pause {
    color: #FFC0CB;
}
```

### 4\. Autostart the Controller

Add the Python controller to the autostart of your Hyprland (`~/.config/hypr/hyprland.conf`) for continuous flag monitoring:

```bash
# In file ~/.config/hypr/hyprland.conf
exec-once = ~/.local/bin/pomodoro_rgb_ctl.py &
```

-----

## 🚀 Usage

1.  **Restart** Waybar or the compositor.
2.  **Left-click** on the Pomodoro module:
      * Starts the timer.
      * Keyboard turns **RED** (Work).
3.  **Automatic transition:**
      * When the timer switches to break mode, the keyboard turns **GREEN**.
4.  **Right-click** on the Pomodoro module:
      * Resets the timer.
      * Keyboard turns **YELLOW** (Inactive).

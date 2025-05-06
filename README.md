# notiPy

**notiPy** is a Python 3-based command-line notification and reminder tool that uses `notify-send` to display desktop notifications.

Easily schedule one-time, daily, or weekly reminders directly from your terminal.

> ⚠️ This tool is developed and tested on GNOME desktop environments. Compatibility with other Linux desktop environments may vary.

---

## 🔧 Requirements

- Python 3
- `notify-send` utility (usually included in the `libnotify-bin` package)

### Install `notify-send` (Debian/Ubuntu):

```bash
sudo apt install libnotify-bin
```

---

## Usage

### Add a Reminder

```bash
notipy --add 'Message' 'YYYY-MM-DD HH:MM:SS' [--type single|daily|weekly]
```

**Arguments:**

- `'Message'`: The text you want to appear in the notification.
- `'YYYY-MM-DD HH:MM:SS'`: The exact time to trigger the notification.
- `--type` *(optional)*: The reminder type:
  - `single` *(default)* — One-time notification.
  - `daily` — Repeats every day at the same time.
  - `weekly` — Repeats every week on the same weekday and time.

**Examples:**

```bash
notipy --add 'Submit project' '2025-05-08 14:30:00'
notipy --add 'Drink water!' '2025-05-06 09:00:00' --type daily
notipy --add 'Team meeting' '2025-05-07 10:00:00' --type weekly
```

---

### View All Reminders

```bash
notipy --list
```

Lists all currently scheduled reminders along with their type and next scheduled time.

---

## How It Works

- `notiPy` schedules your reminders in a background process.
- It uses `notify-send` to deliver notifications at the scheduled times.
- Repeating reminders automatically re-schedule themselves after firing.

---

# Quiz-App-with-Timer-Sound-Category-Selection
A colorful, interactive Tkinter-based Quiz Application that fetches live multiple-choice questions from a free trivia API (Open Trivia DB)

# 🧠 Quiz App with Timer, Sound & Category Selection

A colorful, interactive Tkinter-based **Quiz Application** that fetches **live multiple-choice questions** from a free trivia API (Open Trivia DB). This app features:

* 🗂️ Category selection (AI, GK, Computers, etc.)
* ⏱️ Countdown timer per question
* 🔔 Sound alert when only 5 seconds remain
* 📊 Score calculation and CSV export
* 🎨 Stylish dark-themed GUI using Tkinter

---

## 🚀 Features

| Feature                   | Description                                                     |
| ------------------------- | --------------------------------------------------------------- |
| 🧠 Mixed Questions        | From general knowledge, tech, coding, AI, etc. (via online API) |
| 🕒 Countdown Timer        | 20 seconds per question, visible in GUI                         |
| 🔊 Sound Alerts           | Beeps every second from 5s to 0s                                |
| 🗃️ Category Selection    | User can choose from categories via dropdown                    |
| ↔️ Navigation             | Move between questions with Next/Previous buttons               |
| ✅ Answer Selection        | 4 options per question, auto-checked on submit                  |
| 📈 CSV Score Export       | Appends performance data to `score.csv` file                    |
| 🖼️ Dark Themed Interface | Clean, styled GUI using colors and fonts                        |

---

## 📦 Installation

```bash
# 1. Clone the repository
https://github.com/your-username/quiz-app-tkinter.git

# 2. Install dependencies
pip install requests

# 3. Run the app
python quiz_app.py
```

> ✅ Make sure you're using **Python 3.6+** and are on **Windows** to hear the sound alert via `winsound`.

---

## 📸 Screenshots

> Coming soon (you can capture using Snipping Tool or use `Tkinter` screenshot capture)

---

## 🧱 Project Structure

```
quiz-app/
├── quiz_app.py        # Main application
├── requirements.txt   # Required libraries
└── README.md          # Project overview
```

---

## 📊 CSV Export Format

When you complete a quiz, your score is stored in `score.csv` with this format:

| Category | Questions | Correct | Percent |
| -------- | --------- | ------- | ------- |
| Science  | 10        | 7       | 70.0%   |

---

## 📚 Trivia API Used

[Open Trivia DB](https://opentdb.com/api_config.php)

* Free and public trivia question database
* Categories: Science, Technology, History, Computers, etc.

---

## 🙋‍♂️ Author

**Jatin Kumar**
B.Tech CSE
Passionate about educational software and intelligent applications

---

## 💡 Future Ideas

* Add text-to-speech for questions
* Add user login and history tracking
* Create a leaderboard
* Convert to Android app with Kivy or Flutter

---

> 🔗 Feel free to fork and improve. Contributions are welcome!

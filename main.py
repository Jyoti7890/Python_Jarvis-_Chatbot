import ctypes
import datetime
import time
import webbrowser
import os
import pyttsx3
import random
import wikipedia
import pyautogui
import psutil


def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 50)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume + 0.25)
    return engine


def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()


def set_volume(level):
    volume = int(level * 0xFFFF)
    ctypes.windll.winmm.waveOutSetVolume(0, volume | (volume << 16))


def increase_volume():
    set_volume(0.8)
    speak("Volume increased")


def decrease_volume():
    set_volume(0.3)
    speak("Volume decreased")


def mute_volume():
    set_volume(0)
    speak("Volume muted")


def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday"
    }
    return day_dict.get(day, "Unknown")


def wish_me():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M %p")
    day = cal_day()
    if (hour >= 0) and (hour < 12):
        speak(f"Good morning, it's {day} and the time is {t}")
    elif (hour >= 12) and (hour < 18):
        speak(f"Good afternoon, it's {day} and the time is {t}")
    else:
        speak(f"Good evening, it's {day} and the time is {t}")


def social_media(command):
    if 'linkedin' in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com")
    elif 'youtube' in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif 'discord' in command:
        speak("Opening Discord")
        webbrowser.open("https://discord.com/")
    elif 'dei website' in command:
        speak("Opening the DEI website")
        webbrowser.open("https://www.dei.ac.in/dei/")
    elif 'google classroom' in command:
        speak("Opening Google Classroom")
        webbrowser.open("https://classroom.google.com/u/0/h?hl=en")
    else:
        speak("No result found")


def schedule():
    day = cal_day().lower()
    speak("Today's schedule is:")
    week = {
        'monday': "You have a meeting at 10 AM.",
        'tuesday': "You have a project deadline.",
        'wednesday': "You have a seminar at 2 PM.",
        'thursday': "You have classes in the morning.",
        'friday': "You have a group study at 3 PM.",
        'saturday': "It's a free day!",
        'sunday': "It's a free day!"
    }
    if day in week:
        speak(week[day])


def display_tasks():
    if os.path.exists("todo.txt"):
        with open("todo.txt", "r") as file:
            tasks = file.readlines()
        print("Current tasks:")
        for index, task in enumerate(tasks, 1):
            print(f"{index}. {task.strip()}")
        return tasks
    else:
        print("No tasks found.")
        return []


def search_wikipedia(query):
    search_term = query.replace("search wikipedia", "").strip()
    try:
        result = wikipedia.summary(search_term, sentences=2)
        print("Wikipedia Summary:")
        for line in result.split('. '):
            print(line)
            speak(line)
    except wikipedia.exceptions.DisambiguationError as e:
        speak("Multiple results found. Please be more specific.")
        print("Disambiguation error:", e.options)
    except wikipedia.exceptions.PageError:
        speak("No results found for this term.")
        print("Page not found.")
    except Exception as e:
        print("An unexpected error occurred:", e)
        speak("Couldn't fetch the information due to an unexpected error.")


def close_application(app_name):
    """Closes the application with the specified name."""
    for proc in psutil.process_iter():
        if app_name.lower() in proc.name().lower():
            proc.kill()
            speak(f"{app_name} closed successfully.")
            return
    speak(f"{app_name} is not running or could not be found.")


if __name__ == "__main__":
    speak("Hello, I'm JARVIS")
    wish_me()

    while True:
        try:
            query = input("Enter command: ")
            speak(f"You said: {query}")

            if "hello" in query:
                speak("Welcome, how can I help you?")
            elif "new task" in query:
                task = query.replace("new task", "").strip()
                if task:
                    speak("Adding task: " + task)
                    with open("todo.txt", "a") as file:
                        file.write(task + "\n")
            elif "show task" in query:
                tasks = display_tasks()
                if tasks:
                    task_list = "\n".join(task.strip() for task in tasks)
                    print("Tasks:\n" + task_list)
                    speak("Here are your tasks.")
                    for task in tasks:
                        speak(task.strip())
                else:
                    speak("You have no tasks added yet.")
            elif "remove task" in query:
                tasks = display_tasks()
                if tasks:
                    task_number = int(input("Enter the task number to remove: "))
                    if 1 <= task_number <= len(tasks):
                        task_to_remove = tasks[task_number - 1].strip()
                        tasks.pop(task_number - 1)
                        with open("todo.txt", "w") as file:
                            file.writelines(tasks)
                        speak(f"Task '{task_to_remove}' removed.")
                    else:
                        print("Invalid task number.")
            elif "search wikipedia" in query:
                search_wikipedia(query)
            elif "search google" in query:
                search_term = query.replace("search google", "").strip()
                url = f"https://www.google.com/search?q={search_term}"
                webbrowser.open(url)
                speak(f"Searching Google for {search_term}")
            elif "volume up" in query or "increase volume" in query:
                increase_volume()
            elif "volume down" in query or "decrease volume" in query:
                decrease_volume()
            elif "volume mute" in query or "mute the sound" in query:
                mute_volume()
            elif "open" in query:
                app_name = query.replace("open", "").strip()
                pyautogui.press("win")
                pyautogui.typewrite(app_name)
                pyautogui.sleep(2)
                pyautogui.press("enter")
            elif "close" in query:
                app_name = query.replace("close", "").strip()
                close_application(app_name)
            elif "play music" in query:
                speak("Playing music")
                songs = [
                    "https://www.youtube.com/watch?v=ol4Q1tK0z4g&list=PLfP6i5T0-DkJXsZPmlxlyJuGxsS5_Vii8",
                    "https://www.youtube.com/watch?v=98IJZ__ws_g",
                    "https://www.youtube.com/shorts/phVBNxIHhos",
                    "https://www.youtube.com/watch?v=SQYbYW0KSXM",
                    "https://www.youtube.com/watch?v=_Dukw36Wy24"
                ]
                webbrowser.open(random.choice(songs))
            elif "schedule" in query:
                schedule()
                speak("Schedule")
            elif "exit" in query:
                speak("Exiting JARVIS. Goodbye!")
                break
        except KeyboardInterrupt:
            speak("Exiting JARVIS. Goodbye!")
            break

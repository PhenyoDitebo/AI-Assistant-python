import openai
#used to manage environment variables in python projects
#find and load are used for loading env variables from 
#a .env file into applications environment.

#find_dotenv - Searches for a .env file in the current directory or its parent directories.
#load_dotenv - Reads the .env file and loads its key-value pairs as environment variables into the process's environment.
from dotenv import find_dotenv, load_dotenv

#used to read environment variables from .env files and load them into python apps
#allows us to access the values from the .env file using "os.getenv()" or "os.environ"
load_dotenv()
import time
import logging
from datetime import datetime
import pyttsx3
import speech_recognition as sr
from tkinter import *
from tkinter import ttk
import threading

#We should be able to call the OpenAI assistant with this
client = openai.OpenAI()
#we can also do "openai.api_key = os.environ.get("OPENAI_API_KEY2")"
#this is how the OpenAI Python library authenticates API requests.
#This is more secure, apparently. But it works either way.
#another way: client = OpenAI(api_key=os.environ.get("CUSTOM_ENV_NAME") 

#this is the model we can use.
#Of course, we can always just change this to gpt 4o later down the line
Model = "gpt-4o"
#try to make the variables easy to tell apart.

# ====== Create Assistant, client/application ======

#the assistant API is in beta for this tutorial. We can change it later.
#The assistant has been made, so we don't need this anymore - commented out.
'''help_bot = client.beta.assistants.create(
    name = "0-2",
    instructions = """You are a personal tutor who helps Engineering students manage their homework and assignments. You've helped many students and you are among the best tutors. Users may address you as "Baymax".""",
    model = Model
)

#assistant_id = help_bot.id
print(assistant_id)#'''

#===== Hardcode the IDs, they have been created. ====
Assistant_id = #your own api assistant id
Thread_id = #your own api thread id


# ===== Create the Thread, where all messages will be =====
'''thread = client.beta.threads.create(
    messages = [
        {
            "role": "user",
            "content": "Lets work with the variable e!"
            #this will be the first message sent by user.
        }
    ]
)
print(Thread_id)
'''

# ==== initialize TTS engine ====
tts_engine = pyttsx3.init()


# ==== TEXT - TO - SPEECH FUNCTION ====
def speak_text(text):
    #convert text to speech
    tts_engine.say(text)
    tts_engine.runAndWait()


# ==== initialize STT engine ====
r = sr.Recognizer()

# ==== creating the MAIN BAYMAX DISPLAY window. ====
root = Tk() #creates the main window.
root.title("Baymax V1.2") #Sets title

#baymax is this image, this loads the image
baymax = PhotoImage(file = #pathway to the image file you wish to use)

#We want to put the image inside the tk window - define the label first.
label = ttk.Label(root, image = #name)

#this places the label widget inside the window.
label.pack()

# === SPEECH TO TEXT FUNCTION
def record_text():
    # Show window as soon as Baymax starts speaking because the program is running other tasks in the background.
    root.update()  # Ensure window is updated immediately when Baymax starts speaking
    #acts as a "kickstarter" to make sure the window refreshes at this specific point in time

    tts_engine.say("I'm listening.")
    tts_engine.runAndWait()
    #loop in case of errors.
    while(1):
        try:
            with sr.Microphone() as source2:
                print("Listening...")
                r.adjust_for_ambient_noise(source2, duration=0.2)

                audio2 = r.listen(source2)

                Mytext = r.recognize_google(audio2)

                return Mytext

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("Unknown error occurred. Maybe try speaking louder.")


# ===== helper function to help with the waiting and stuff.
def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """

    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=Thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                print(f"")
                logging.info(f"Run completed in {formatted_elapsed_time}")

                # Get messages here once Run is completed
                messages = client.beta.threads.messages.list(thread_id=Thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"B-2's Response: {response}")
                print(f"")
                speak_text(response) #convert text to speech
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)

#main loop to keep baymax listening and responding
def main_loop():
    while True:
        try:
            user_input = record_text()

            #check for exit commands
            if user_input.lower() in ["quit", "exit", "bye", "goodbye"]:
                print("Exiting Program.")
                speak_text("Goodbye. Have a good day!")
                root.destroy() #close window
                return

            #sends user input to assistant
            message = client.beta.threads.messages.create(
                thread_id = Thread_id,
                role = "user", 
                content=user_input
            )

            #run assistant
            run = client.beta.threads.runs.create(
            thread_id = Thread_id,
            assistant_id = Assistant_id,
            instructions = "Please address the user as 'your name'"
        )

            #wait for assistant response
            wait_for_run_completion(client= client, thread_id = Thread_id, run_id = run.id)

        except Exception as e:
            print(f"An error occured: {e}")
            speak_text("There seems to be an error. Please try again.")


#start main loop in a separate thread, think parallel processing.
#Runs the GUI and assistant logic at the same time.
if __name__ == "__main__":
    app_thread = threading.Thread(target=main_loop, daemon=True)
    app_thread.start()
    root.mainloop()  # Keep the Tkinter GUI open



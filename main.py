import openai
import os
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime

load_dotenv()

#Can call the openai assistant through the client, since we have created this class.
#can also write it like openai.api_key = os.environ.get("OPENAI_API_KEY")
news_api_key = os.environ.get("NEWS_API_KEY")
client = openai.OpenAI()
model = "gpt-3.5-turbo-16k"

# ---- Create our assistant ---- Commented out, since we made it already.
'''ava = client.beta.assistants.create (
    name = "Ava", 
    instructions = "You are an advanced AI assistant for mechatronics & software engineering students. You help them understand material quickly and easily, and help with tasks like emails and projects. Yet you are also compassionate, and help with emotions. Your name when talking to the user is "Ava",
    model = model
)

#making assistant ID
assistant_id = ava.id
print(assistant_id)
'''

# ----- create a thread -----
'''thread = client.beta.threads.create(
    messages = [
        {
            "role": "user",
            "content": "How do I get started working on a coding project for Tesla to see?"
        }
    ]
)

#Creating the thread ID. Remember the flow of an AI | Input -> Run -> Output.
#This is already ran, you don't need to run it again - it'll just make another assistant.
thread_id = thread.id
print(thread_id)
'''

# ----- hardcode our ids, these are from the assistant we created before ------
assistant_id = "asst_9oHjmVRFnHNM9DhZYwiXKmQG"
thread_id = "thread_HON8c8wYRobODhNYZUCWPzy5"

# ----- create a message -----
Message = input("What's your question? ")
message = Message
message = client.beta.threads.messages.create(
    thread_id = thread_id,
    role = "user",
    content = message
)

# ---- to run assistant ----
run = client.beta.threads.runs.create(
    thread_id = thread_id,
    assistant_id=assistant_id,
    instructions = "Please address the user as Phenyo"
)

#helper function
def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """

    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Ava's Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)

# ---- run ---- 
wait_for_run_completion(client=client, thread_id=thread_id, run_id = run.id)

# ---- run steps --- logs
run_steps = client.beta.threads.runs.steps.list(
    thread_id = thread_id,
    run_id = run.id
)

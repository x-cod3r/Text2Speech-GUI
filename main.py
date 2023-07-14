import tkinter as tk
import pyttsx3

engine = None
stop_flag = False

def initialize_engine():
    global engine
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()
    engine.connect('started-utterance', on_start)
    engine.connect('finished-utterance', on_end)

def on_start(name, location, length):
    # Disable the "Speak" button when speech starts
    speak_button.config(state=tk.DISABLED)

def on_end(name, completed):
    # Enable the "Speak" button when speech ends
    speak_button.config(state=tk.NORMAL)

def stop_speech():
    global stop_flag
    if engine is not None:
        # Set the stop flag to interrupt speech playback
        stop_flag = True

def text_to_speech():
    global stop_flag
    # Reset the stop flag
    stop_flag = False

    # Get the selected voice
    voice = int(voice_var.get())

    # Get the speech speed
    speed = speed_slider.get()

    # Get the text from the input field
    text = text_entry.get("1.0", tk.END).strip()

    if text:
        if engine is not None:
            # Stop any ongoing speech playback
            stop_speech()

            # Set the voice
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[voice].id)

            # Adjust the speech rate based on speed
            rate = engine.getProperty('rate')
            engine.setProperty('rate', int(rate * speed))

            # Convert the text to speech
            engine.say(text)
            engine.runAndWait()

            # Check the stop flag periodically during speech synthesis
            while engine.isBusy():
                if stop_flag:
                    engine.stop()
                    break

# Create the main application window
window = tk.Tk()
window.title("Text-to-Speech Application")

# Create the text input field
text_entry = tk.Text(window, width=50, height=10)
text_entry.pack(pady=10)

# Create the voice selection dropdown menu
voice_var = tk.StringVar()
voice_label = tk.Label(window, text="Select Voice:")
voice_label.pack()
voice_dropdown = tk.OptionMenu(window, voice_var, *range(len(pyttsx3.init().getProperty('voices'))))
voice_var.set(0)  # Default voice
voice_dropdown.pack(pady=5)

# Create the speech speed slider
speed_label = tk.Label(window, text="Speech Speed:")
speed_label.pack()
speed_slider = tk.Scale(window, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL)
speed_slider.set(1.0)  # Default speed
speed_slider.pack(pady=5)

# Create the "Speak" button
speak_button = tk.Button(window, text="Speak", command=text_to_speech)
speak_button.pack(pady=5)

# Create the "Stop" button
stop_button = tk.Button(window, text="Stop", command=stop_speech)
stop_button.pack(pady=5)

# Initialize the engine
initialize_engine()

# Start the main event loop
window.mainloop()

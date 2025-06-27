import random
import re
import speech_recognition as sr
import pyttsx3


class SmartChatBot:
    def __init__(self, name):
        self.name = name
        self.user_name = ""
        self.memory = {}

        self.responses = {
            r"hello|hi|hey": ["Hi there!", "Hello!", "Hey, good to see you!"],
            r"how are you|how you doing": ["I'm doing great, thanks!",
                                           "Good, how about you?",
                                           "As an AI, I'm always good!"],
            r"bye|goodbye|see you": ["Goodbye!", "See you later!", "Take care!"],
            r"what is your name|who are you": [f"I'm Naveen!",
                                               f"My name is naveen, nice to meet you!"],
            r"my name is (\w+)|i am (\w+)": ["Nice to meet you, {}!",
                                             "Hello {}, how can I assist you?"],
            r"what can you do": ["I can chat with you about almost anything!",
                                 "I'm here to answer questions and have conversations!"],
            r"thank you|thanks": ["You're welcome!", "My pleasure!", "Anytime!"]
        }

        self.default_responses = ["I'm not sure I understand.",
                                  "Can you tell me more?",
                                  "Interesting, what do you mean?"]

        # Initialize TTS engine
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)  # Set speaking speed

    def speak(self, text):
        print(f"{self.name}: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio = recognizer.listen(source, timeout=5)
                user_input = recognizer.recognize_google(audio)
                print(f"You: {user_input}")
                return user_input
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that.")
                return ""
            except sr.WaitTimeoutError:
                self.speak("No input detected.")
                return ""
            except sr.RequestError:
                self.speak("Speech recognition service is unavailable.")
                return ""

    def get_response(self, user_input):
        user_input = user_input.lower().strip()

        name_match = re.search(r"my name is (\w+)|i am (\w+)", user_input)
        if name_match:
            self.user_name = name_match.group(1) or name_match.group(2)
            return random.choice(self.responses[r"my name is (\w+)|i am (\w+)"]).format(self.user_name)

        for pattern, responses in self.responses.items():
            if re.search(pattern, user_input):
                return random.choice(responses)

        return random.choice(self.default_responses)

    def chat(self):
        self.speak(f"Hi! I'm {self.name}. How can I help you today? Say 'quit' to exit.")

        while True:
            user_input = self.listen()
            if not user_input:
                continue

            if 'quit' in user_input.lower():
                farewell = "Goodbye" + (f", {self.user_name}" if self.user_name else "") + "!"
                self.speak(farewell)
                break

            response = self.get_response(user_input)
            self.speak(response)


# Run the chatbot with voice
if __name__ == "__main__":
    bot = SmartChatBot("naveen")
    bot.chat()

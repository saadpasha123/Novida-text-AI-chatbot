from flask import Flask, render_template, request
from datetime import datetime
import pytz
import webbrowser
import requests

app = Flask(__name__)

def date_time():
    """Returns the current date and time in Karachi."""
    dt = datetime.now(pytz.timezone('Asia/Karachi'))
    return dt.strftime("%d-%m-%Y %H:%M:%S")

def news():
    """Fetches top news headlines."""
    try:
        api_key = "b893487258624a0086e2704bd7953cf6"
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if 'articles' in data:
                headlines = [article['title'] for article in data['articles'][:5]]
                return "Top Headlines:\n" + "\n".join(headlines)
            else:
                return "No articles found in the response."
        else:
            return "Failed to fetch news. Please try again later."

    except Exception as e:
        print(f"Error fetching news: {e}")
        return "An error occurred while fetching the news. Please try again later."

def get_weather(city):
    """Fetches weather information for the provided city."""
    api_key = "39c04d159e4a07b5af607b21a742f02d"
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather_descr = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"The weather in {city.title()} is {weather_descr} with {temperature}°C."
    else:
        return "Invalid city name."

def chatbot_response(user_message):
    """Generates a response from the chatbot."""
    user_message = user_message.lower()

    if "date" in user_message or "time" in user_message:
        return f"The current date and time is {date_time()}"

    elif "weather" in user_message:
        if "weather in" in user_message:
            city = user_message.split("weather in")[-1].strip()
            return get_weather(city)
        else:
            return "Please provide the city like this: 'weather in London'."

    elif "news" in user_message:
        return news()

    elif "youtube" in user_message:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube..."

    elif "google" in user_message:
        webbrowser.open("https://www.google.com")
        return "Opening Google..."

    responses = {
        "hi": "Hi! How can I assist you?",
        "how are you": "I'm fine, but I'm a chatbot so I have no feelings.",
        "goodbye": "Goodbye! Have a nice day!",
        "what is your name": "My name is Novida.",
        "who created you": "I was created by Saad Pasha, a student at SSUET University.",
        "default": "I don't understand what you're saying."
    }

    return responses.get(user_message, responses["default"])

@app.route("/", methods=["GET", "POST"])
def home():
    """Handles chat and displays responses."""
    if 'chat_history' not in request.cookies:
        chat_history = []  
    else:
        chat_history = eval(request.cookies['chat_history'])  

    if request.method == "POST":
        user_message = request.form["user_input"].strip()

        if user_message:
            bot_reply = chatbot_response(user_message)
            chat_history.append({"text": f"You: {user_message}", "user": True})
            chat_history.append({"text": f"Novida: {bot_reply}", "user": False})

            response = app.make_response(render_template("index.html", chat_history=chat_history))
            response.set_cookie('chat_history', str(chat_history))
            return response

    return render_template("index.html", chat_history=chat_history)

if __name__ == "__main__":
    app.run(debug=True)

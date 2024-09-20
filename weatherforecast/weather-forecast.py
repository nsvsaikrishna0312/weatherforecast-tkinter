import requests
from tkinter import *
import PySimpleGUI as sg

def get_weather_data(location):
    api_key = '0f348c72acbbdcd0fd010e046069ea69'
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    complete_url = base_url + 'appid=' + api_key + '&q=' + location

    response = requests.get(complete_url)

    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        temperature = temperature - 273.15
        return weather_description, temperature, humidity
    else:
        return None

def display_weather_data(weather_data):
    if weather_data is not None:
        description, temperature, humidity = weather_data
        layout = [[sg.Text(f'Weather Description: {description}', font=("Helvetica", 12))],
                  [sg.Text(f'Temperature: {temperature:.2f}°C', font=("Helvetica", 12))],
                  [sg.Text(f'Humidity: {humidity}%', font=("Helvetica", 12))],
                  [sg.Button('Exit', size=(10, 2), font=("Helvetica", 12))]]
        window = sg.Window('Weather Report', layout, element_justification='c')

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Exit':
                break

        window.close()
    else:
        print('Failed to fetch weather data.')

def show_output():
    location = entry_location.get()
    weather_data = get_weather_data(location)

    if weather_data:
        description, temperature, humidity = weather_data
        result_text = f"Weather Description: {description}\nTemperature: {temperature:.2f}°C\nHumidity: {humidity}%"

        # Set background color based on weather conditions
        if 'rain' in description.lower():
            output_label.configure(bg='#4E70A9')  # Blue for rain
        elif 'cloud' in description.lower():
            output_label.configure(bg='#A9A9A9')  # Gray for clouds
        elif 'clear' in description.lower() or 'sunny' in description.lower():
            output_label.configure(bg='#FFD700')  # Yellow for clear/sunny
        elif 'cool' in description.lower():
            output_label.configure(bg='#00BFFF')  # Deep Sky Blue for cool weather
        elif 'mist' in description.lower():
            output_label.configure(bg='#CDD8D9')  # Gray for mist
        else:
            output_label.configure(bg='#f0f0f0')  # Default color


    else:
        result_text = "Failed to fetch weather data."
        output_label.configure(bg='#f0f0f0')  # Default color

    output_label.config(text=result_text)

# Create the main Tkinter window
root = Tk()
root.title("Climate Detector")

# Add some padding to the window
root.geometry("400x300")
root.configure(bg='#F8E559')

# Create Entry widget to get location input
entry_location = Entry(root, width=30, font=("Helvetica", 30))
entry_location.pack(pady=20)

# Create a Label widget to display the output
output_label = Label(root, text="", font=("Helvetica", 30), bg='#f0f0f0')
output_label.pack(pady=20)

# Create a button to trigger the output
show_output_button = Button(root, text="Show Weather", command=show_output, font=("Helvetica", 30), bg='#4CAF50', fg='white', relief=GROOVE)
show_output_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
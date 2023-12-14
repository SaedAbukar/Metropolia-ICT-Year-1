import requests


def get_weather(city, api_key):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    response = requests.get(api_url)
    data = response.json()

    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temperature_kelvin = data['main']['temp']
        temperature_celsius = temperature_kelvin - 273.15
        return weather_description, temperature_celsius
    else:
        error_message = data['message']
        return None, f"Error: {error_message}"


def main():
    city = input("Enter the city name: ")
    api_key = "6ce33329d9eb56fcde8cc14e07aa160e"

    weather_description, temperature = get_weather(city, api_key)

    if weather_description is not None and temperature is not None:
        print(f"Weather in {city}: {weather_description}")
        print(f"Temperature: {temperature:.2f} °C")
    else:
        print("Failed to fetch weather information.")


if __name__ == "__main__":
    main()


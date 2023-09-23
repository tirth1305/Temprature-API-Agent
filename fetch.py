import requests
from twilio.rest import Client
from fake_useragent import UserAgent  # Import UserAgent from fake-useragent

# Twilio credentials (replace with your own)
account_sid = 'AC4043c050f46311992a89bee778cb4b7f'
auth_token = 'ff0bcf46dc6d56a8ce06ecc36053680b'
twilio_phone_number = '+12512205010'
recipient_phone_number = '+917802036041'

# OpenWeatherMap API key (replace with your own)
api_key = 'f8db1590bd766078927840d37a6c10ae'

# Generate a random User-Agent string using fake-useragent
user_agent = UserAgent()
user_agent_string = user_agent.random  # Generate the random User-Agent string

# Set the User-Agent header in the HTTP request
headers = {'User-Agent': user_agent_string}

def get_temperature(city):
    try:
        # Send an HTTP GET request to the OpenWeatherMap API
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            weather_data = response.json()
            temperature = weather_data['main']['temp']
            return temperature
        else:
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def send_temperature_sms(temperature, city):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"The temperature in {city} is: {temperature}°C",
        from_=twilio_phone_number,
        to=recipient_phone_number
    )
    print(f"Temperature sent via SMS: {temperature}°C")

def main():
    city = input("Enter City: ")
    temperature = get_temperature(city)

    if temperature is not None:
        send_temperature_sms(temperature, city)
    else:
        print("Failed to fetch temperature data.")

if __name__ == "__main__":
    main()

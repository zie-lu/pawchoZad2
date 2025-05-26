from flask import Flask, request, render_template_string
import datetime
import requests

app = Flask(__name__)
PORT = 5000

def log_start_details():
    log_message = (
        f"Application started on {datetime.datetime.now()}\n"
        f"Author: Piotr Zieliński\n"
        f"Listening on TCP port {PORT}\n"
    )
    with open("app.log", "a") as log_file:
        log_file.write(log_message)
    print(log_message)

COUNTRIES_AND_CITIES = {
    "Poland": ["Warsaw", "Krakow", "Gdansk"],
    "Germany": ["Berlin", "Munich", "Hamburg"],
    "USA": ["New York", "Los Angeles", "Chicago"]
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Weather Application</title>
    <script>
        function updateCities() {
            const country = document.getElementById("country").value;
            const citySelect = document.getElementById("city");
            
            // Clear current city options
            citySelect.innerHTML = "";

            // Update city options based on selected country
            const citiesByCountry = {
                "Poland": ["Warsaw", "Krakow", "Gdansk"],
                "Germany": ["Berlin", "Munich", "Hamburg"],
                "USA": ["New York", "Los Angeles", "Chicago"]
            };

            if (citiesByCountry[country]) {
                citiesByCountry[country].forEach(city => {
                    const option = document.createElement("option");
                    option.value = city;
                    option.textContent = city;
                    citySelect.appendChild(option);
                });
            }
        }
    </script>
</head>
<body>
    <h1>Weather Application</h1>
    <form action="/" method="post">
        <label for="country">Country:</label>
        <select name="country" id="country" onchange="updateCities()">
            {% for country in countries %}
            <option value="{{ country }}">{{ country }}</option>
            {% endfor %}
        </select><br>
        <label for="city">City:</label>
        <select name="city" id="city">
            {% for city in cities %}
            <option value="{{ city }}">{{ city }}</option>
            {% endfor %}
        </select><br>
        <button type="submit">Get Weather</button>
    </form>

    {% if weather %}
    <h2>Weather in {{ weather.city }}, {{ weather.country }}</h2>
    <p>Temperature: {{ weather.temperature }}°C</p>
    <p>Wind Speed: {{ weather.wind_speed }} km/h</p>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def weather_app():
    selected_country = "Poland"
    selected_city = "Warsaw"
    weather_data = None

    if request.method == 'POST':
        selected_country = request.form.get('country', "Poland")
        selected_city = request.form.get('city', "Warsaw")

        cities = {
            "Warsaw": {"lat": 52.2297, "lon": 21.0122},
            "Krakow": {"lat": 50.0647, "lon": 19.9450},
            "Gdansk": {"lat": 54.3520, "lon": 18.6466},
            "Berlin": {"lat": 52.5200, "lon": 13.4050},
            "Munich": {"lat": 48.1351, "lon": 11.5820},
            "Hamburg": {"lat": 53.5511, "lon": 9.9937},
            "New York": {"lat": 40.7128, "lon": -74.0060},
            "Los Angeles": {"lat": 34.0522, "lon": -118.2437},
            "Chicago": {"lat": 41.8781, "lon": -87.6298}
        }

        if selected_city in cities:
            lat = cities[selected_city]["lat"]
            lon = cities[selected_city]["lon"]

            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            response = requests.get(weather_url)
            if response.status_code == 200:
                weather = response.json().get("current_weather", {})
                weather_data = {
                    "country": selected_country,
                    "city": selected_city,
                    "temperature": weather.get("temperature"),
                    "wind_speed": weather.get("windspeed")
                }

    return render_template_string(
        HTML_TEMPLATE,
        countries=COUNTRIES_AND_CITIES.keys(),
        cities=COUNTRIES_AND_CITIES[selected_country],
        weather=weather_data
    )

if __name__ == "__main__":
    log_start_details()
    app.run(host="0.0.0.0", port=PORT)
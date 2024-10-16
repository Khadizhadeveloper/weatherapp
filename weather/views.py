import requests
from django.shortcuts import render
from django.conf import settings

def weather_view(request):
    city = request.GET.get('city')
    api_key = settings.WEATHER_API_KEY  # Получаем ключ API из настроек
    weather_data = None
    forecast_data = None
    error_message = None

    if city:
        try:
            # URL для получения текущей погоды
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            weather_response = requests.get(weather_url)

            if weather_response.status_code == 200:
                weather_data = weather_response.json()

                # Проверяем, есть ли координаты в ответе
                if 'coord' in weather_data:
                    lat = weather_data['coord']['lat']
                    lon = weather_data['coord']['lon']

                    # URL для получения прогноза
                    forecast_url = f"http://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={api_key}&units=metric"
                    forecast_response = requests.get(forecast_url)

                    if forecast_response.status_code == 200:
                        forecast_data = forecast_response.json()
                        forecast_data['daily'] = forecast_data['daily'][:7]
                    else:
                        error_message = f"Error fetching forecast data: {forecast_response.status_code}"
                else:
                    error_message = "Coordinates not found in weather data."
            else:
                error_message = f"Error fetching weather data: {weather_response.status_code}"

        except requests.exceptions.RequestException as e:
            error_message = f"Error making API request: {e}"

    return render(request, 'weather.html', {
        'weather_data': weather_data,
        'forecast_data': forecast_data,
        'city': city,
        'error_message': error_message,
    })

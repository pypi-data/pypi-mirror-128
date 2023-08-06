# Ree-connector

A lightweight Python package to consume data from REE (Red Eléctrica de España)

## Intro

The development of this package is motivated by the change in the regulated tariff PVPC (Voluntary Price for Small Consumers) of the Spanish electricity market. This allowed small consumers to choose the tariff that best suited their consumption according to their schedules or needs.

Following this change, the three sections into which it was previously divided (general, night, electric vehicle) disappeared. From this moment on, each hourly time slot has a different price, and can be very different from the price of its neighbours. This eliminates the possibility of adjusting your consumption to certain hours, where you know for sure that the price of electricity is cheaper.

Therefore, this package is designed to obtain information about the market and contains a series of methods that will help you to know the best hours to make your heavy consumption, among other things, and of course, integrate it with your Python application to manage home automation systems based on this data.

------------------------------------------------------------------------------

El desarrollo de este paquete está motivado por el cambio producido en la tarifa regulada PVPC (Precio Voluntario para el Pequeño Consumidor) del mercado eléctrico español. Esto permitía a los pequeños consumidores escoger la tarifa que mas se adaptaba a su consumo en función de sus horarios o necesidades.

Tras este cambio, desaparecieron los tres tramos en los que se dividía anteriormente (general, noche, vehículo eléctrico). A partir de este momento, cada tramo de una hora tiene un precio distinto, y puede ser muy diferente al precio de sus vecinos. Esto elimina la posibilidad de ajustar tu consumo a unos horarios determinados, donde sabes seguro que el precio de la luz es mas barato.

Por ello, este paquete está pensado para obtener la información sobre el mercado y contiene una serie de métodos que te ayudarán a conocer las mejores horas para realizar tu consumo pesado, entre otras cosas, y como no, integrarlo con tu aplicación Python para poder gestionar sistemas domoticos en base a estos datos.

------------------------------------------------------------------------------
## First Steps / Primeros Pasos

#### Access Token Request / Solicitud Token Acceso

To use this package you need an access token.
To request it you must send an email to consultasios@ree.es to ask REE (Red Eléctrica de España) for your access token. They usually reply in less than 24h, in the subject you can put "API access token request".

-----------------------------------------------------------------------------

Para utilizar este paquete necesitas un token de acceso.
Para solicitarlo debes enviar un email a consultasios@ree.es para solicitar a REE (Red Eléctrica de España) tu token de acceso. Normalmente suelen responder en menos de 24h, en el asunto puedes poner "Solicitud token acceso API".

-----------------------------------------------------------------------------

#### Quick Start / Inicio Rápido

```` 
```
from datetime import datetime
from ree_connector import markets

# We generate a date as a string with format 'dd-mm-yyyy
date = datetime.now().strftime("%d-%m-%Y")


# We generate a date as a string with format 'dd-mm-yyyy'
# You can do some tests without api key, for production environments
# must request your API token.

market = markets.PvpcMarket(date,"XXXXXXXXXXXXXXXXXXXXXXXXXXXX","PEN")

# Returns all prices for market session
market.get_session_prices()

# Returns min price for market session
market.get_session_min_price()

# Returns max price for market session
market.get_session_max_price()

# Returns avg price for market session
market.get_session_avg_price()

# Returns if price is under session average price or not
market.get_session_prices()[10].is_under_avg()

# Setter method to under_avg attribute
market.get_session_prices()[10].set_under_avg(True)

# Returns the n cheapest prices for market session
market.get_n_cheapest_hours(3)

# Returns if price is cheap or not
market.get_session_prices()[10].is_cheap()

# Setter method to cheap attribute
market.get_session_prices()[10].set_cheap(True)

# Returns the price for Iberian Peninsula and Balearic Islands.
market.get_session_prices()[10].get_pen_price()

# Returns the price for Canary Island and Melilla
market.get_session_prices()[10].get_can_price()

# Returns the session interval
market.get_session_prices()[10].get_raw_hour()

# Atribute with left-hand side datetime
market.get_session_prices()[10].left_hour

# Atribute with right-hand side datetime
market.get_session_prices()[10].right_hour
```
```` 

## Docs

[Documentation](https://jorgemarin.gitlab.io/ree-connector/)


## License / Licencia


MIT License

Copyright (c) 2021 Jorge Marín

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Contributors:
    Jorge Marín - initial Package version 


import time
import datetime
import alphasign
import pyowm

def main():
        sign = alphasign.Serial()
        sign.connect()
        sign.clear_memory()

        # Set the time

        timeString = alphasign.String(size=100, label="1")
        tempString = alphasign.String(size=100, label="2")
        humiString = alphasign.String(size=100, label="3")

        helloText = alphasign.Text("%s%s %s%sF %s%s%%" %(alphasign.colors.DIM_RED, timeString.call(), 
                alphasign.colors.YELLOW, tempString.call(), 
                alphasign.colors.ORANGE, humiString.call()), label="A", mode=alphasign.modes.HOLD)
        sign.allocate((timeString,tempString,humiString,helloText))
        sign.set_run_sequence((helloText,))
        sign.write(timeString)
        sign.write(tempString)
        sign.write(humiString)
        sign.write(helloText)

        while True:

                owm = pyowm.OWM('163f58185b28688d805dae724b718025')
                observation = owm.weather_at_place('Rockville,MD')
                w = observation.get_weather()
                currTemp = int(w.get_temperature('fahrenheit').get('temp'))
                humidity = w.get_humidity()

                currentTime = datetime.datetime.strftime(datetime.datetime.now(), "%H:%M")
                stringData = currentTime

                timeString.data = currentTime
                tempString.data = currTemp
                humiString.data = humidity

                sign.write(timeString)
                sign.write(tempString)
                sign.write(humiString)

                time.sleep(10)

if __name__ == "__main__":
        main()

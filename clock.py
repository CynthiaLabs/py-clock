import os
import time
import ctypes
import shutil
import asyncio
import pyfiglet
import requests
import subprocess
import python_weather
from datetime import datetime
from colorama import init, Fore
from ping3 import ping, verbose_ping
from forex_python.converter import CurrencyRates
from webob import day
init()
time.sleep(1)
os.system("cls")
os.system("mode con: cols=101 lines=16")
os.system("title Cli-Clock")

stupid_line = "\u2501"
client = python_weather.Client()
city = input("Please enter the name of your City: ")

def clock():
    async def getdata(city):
        try:
            weather = await client.find(city)
            temperature = weather.current.temperature
            humidity = weather.current.humidity
            sky_text = weather.current.sky_text
        except:
            temperature = "Error"
            humidity = "Error"
            sky_text = "Error"
            
        def getcrypto(currency):
            try:
                r = requests.get(f'https://production.api.coindesk.com/v1/currency/ticker?currencies={currency}').json()
                price = r['data']['currency'][f'{currency.upper()}']['quotes']['USD']['price']
                return round(price, 2)
            except:
                return "Error"
            
        def getcurrency(currency):
            try:
                c = CurrencyRates()
                return round(float(c.get_rate('EUR', f'{currency}')), 2)
            except:
                return "Error"

        total, used, free = shutil.disk_usage("/")

        subprocess_result = subprocess.Popen("""for /f "tokens=2*delims=: " %i in ('netsh wlan show networks^|find "SSID"')do @echo\%j""",shell=True,stdout=subprocess.PIPE)
        subprocess_output = subprocess_result.communicate()[0],subprocess_result.returncode
        network_name = subprocess_output[0].decode('utf-8').replace("\n", "").split(" ")[0]

        lib = ctypes.windll.kernel32
        t = lib.GetTickCount64()
        t = int(str(t)[:-3])
        mins, sec = divmod(t, 60)
        hour, mins = divmod(mins, 60)
        days, hour = divmod(hour, 24)

        print(f"""{Fore.WHITE}
       Weather Data for {Fore.LIGHTCYAN_EX}{city}{Fore.WHITE}{" " * (32 - (17 + int(len(city))))} EUR -> BTC: {Fore.LIGHTYELLOW_EX}{getcrypto("btc")}{Fore.WHITE}{" " * (24 - (11 + int(len(str(getcrypto("btc"))))))} Disk Space: {Fore.LIGHTGREEN_EX}{free // (2**30)}{Fore.WHITE} of {Fore.LIGHTGREEN_EX}{total // (2**30)} GB{Fore.WHITE} free
       Current Temperature: {Fore.LIGHTCYAN_EX}{temperature}{Fore.WHITE}C{" " * (32 - (22 + int(len(str(temperature)))))} EUR -> XMR: {Fore.LIGHTYELLOW_EX}{getcrypto("xmr")}{Fore.WHITE}{" " * (24 - (11 + int(len(str(getcrypto("xmr"))))))} Used Network: {Fore.LIGHTGREEN_EX}{network_name}{Fore.WHITE}
       Humidity: {Fore.LIGHTCYAN_EX}{humidity}{Fore.WHITE}%{" " * (32 - (11 + int(len(str(humidity)))))} EUR -> USD: {Fore.LIGHTYELLOW_EX}{getcurrency("USD")}{Fore.WHITE}{" " * 9} Uptime: {Fore.LIGHTGREEN_EX}{days}d {hour:02}h {mins:02}m{Fore.WHITE}
       Sky: {Fore.LIGHTCYAN_EX}{sky_text}{Fore.WHITE}{" " * (32 - (5 + int(len(sky_text))))} EUR -> GBP: {Fore.LIGHTYELLOW_EX}{getcurrency("GBP")}{Fore.WHITE}{" " * 9} Ping: {Fore.LIGHTGREEN_EX}{round(float(ping("cynthialabs.net")), 2)}{Fore.WHITE} ms""")

    loop = asyncio.get_event_loop()

    while True:
        rn = datetime.now().astimezone() # Time for me
        op_string = rn.strftime(f"%I : %M %p") # Time in sexy
        os.system("cls")

        hours = rn.strftime(f"%H")
        minutes = rn.strftime(f"%M")
        daynumber = rn.strftime(f"%d")
        if str(daynumber).endswith("1"):
            thingy = "st"
        elif str(daynumber).endswith("2"):
            thingy = "nd"
        elif str(daynumber).endswith("3"):
            thingy = "rd"
        else:
            thingy = "th"
        date = rn.strftime(f"%A, %B %d{thingy} %Y")
        percentage = (int(hours) / 24 + int(minutes) / (60 * 24)) * 100
        print(Fore.LIGHTMAGENTA_EX)
        print(*[x.center((shutil.get_terminal_size().columns) -1) for x in pyfiglet.figlet_format(op_string).split("\n") if not x == "" ],sep=" \n")
        print(Fore.WHITE)
        print((date).center((shutil.get_terminal_size().columns) - 1))
        print(Fore.LIGHTGREEN_EX)
        print(f"{stupid_line}" * round(percentage) + f"{Fore.WHITE}{stupid_line}" * (100 - round(percentage)))
        loop.run_until_complete(getdata(city))
        time.sleep(60)

clock()
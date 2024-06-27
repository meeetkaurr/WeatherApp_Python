from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

root = Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)

def getWeather():
    city = textfield.get()
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city, exactly_one=True, timeout=10)
        
        if not location:
            raise ValueError("Invalid city name")
        
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
        
        if not result:
            raise ValueError("Could not determine the timezone")

        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        name.config(text="CURRENT WEATHER")

        # Fetch weather
        api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=ae0c444adf94d41e7052579cc6f53006"
        json_data = requests.get(api).json()
        
        if json_data.get("cod") != 200:
            raise ValueError("Invalid city name for weather data")

        condition = json_data['weather'][0]['main']
        description = json_data['weather'][0]['description']
        temp = int(json_data['main']['temp'] - 273.15)
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']

        t.config(text=(temp, "°C"))
        c.config(text=(condition, "|", "FEELS", "LIKE", temp, "°C"))
        w.config(text=wind)
        h.config(text=humidity)
        d.config(text=description)
        p.config(text=pressure)

    except Exception as e:
        messagebox.showerror("Weather App", f"Invalid Entry!!\n{e}")
        textfield.delete(0, END)

# Search box
search_image = PhotoImage(file="search.png")
myimage = Label(image=search_image)
myimage.place(x=20, y=20)

textfield = Entry(root, justify=CENTER, font=("poppins", 25, "bold"), width=17, bg="#404040", border=0, fg="white")
textfield.place(x=50, y=40)
textfield.focus()

Search_icon = PhotoImage(file="search_icon.png")
myimage_icon = Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getWeather)
myimage_icon.place(x=400, y=34)

# Logo
logo_image = PhotoImage(file="logo.png")
logo = Label(image=logo_image)
logo.place(x=150, y=100)

# Bottom box
Frame_image = PhotoImage(file="box.png")
frame_myimage = Label(image=Frame_image)
frame_myimage.pack(padx=5, pady=5, side=BOTTOM)

# Time
name = Label(root, text="Time", font=("arial", 15, "bold"))
name.place(x=30, y=100)
clock = Label(root, font=("Helvetica", 20))
clock.place(x=30, y=130)

# Labels
label1 = Label(root, text="WIND", font=("Helvetica", 15, "bold"), bg="#1ab5ef", fg="white")
label1.place(x=120, y=400)

label2 = Label(root, text="HUMIDITY", font=("Helvetica", 15, "bold"), bg="#1ab5ef", fg="white")
label2.place(x=250, y=400)

label3 = Label(root, text="DESCRIPTION", font=("Helvetica", 15, "bold"), bg="#1ab5ef", fg="white")
label3.place(x=430, y=400)

label4 = Label(root, text="PRESSURE", font=("Helvetica", 15, "bold"), bg="#1ab5ef", fg="white")
label4.place(x=650, y=400)

t = Label(font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)
c = Label(font=("arial", 15, "bold"))
c.place(x=400, y=250)

w = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
w.place(x=120, y=430)
h = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
h.place(x=280, y=430)
d = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
d.place(x=450, y=430)
p = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
p.place(x=670, y=430)

root.mainloop()

# Bibliotheken laden
import network
from ota import OTAUpdater
from time import sleep
from machine import Pin,ADC
import neopixel
import machine
import owntime
from WIFI_CONFIG import SSID,PASSWORD

firmware_url="https://raw.githubusercontent.com/Sabine127/PicoOTA/"

ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "Fibonacci/main.py")
ota_updater.download_and_install_update_if_available()

lightPin=26
LightPin=ADC(lightPin)
lightVal=0
lightFaktor=0.4

modePin=27
ModePin=ADC(modePin)
modeVal=0
Modus=0

# Zeitzone
TZ_OFFSET = +1

# GPIO-Pin für WS2812
pin_np = 15

# Anzahl der LEDs
leds = 40

brightness=0.05 #Wert zwischen 0 und 1

# Farbwerte
hour_redVal = 255
hour_greenVal = 0
hour_blueVal = 0
hour_color = (int(hour_redVal*brightness), int(hour_greenVal*brightness), int(hour_blueVal*brightness))
print('hour_color: ',hour_color)

min_redVal = 100
min_greenVal = 255
min_blueVal = 0
min_color = (int(min_redVal*brightness), int(min_greenVal*brightness), int(min_blueVal*brightness))
print('min_color: ',min_color)

both_redVal = 0
both_greenVal = 0
both_blueVal = 255
both_color = (int(both_redVal*brightness), int(both_greenVal*brightness), int(both_blueVal*brightness))
print('both_color: ',both_color)

none_redVal = 100
none_greenVal = 255
none_blueVal = 255
none_color = (int(none_redVal*brightness), int(none_greenVal*brightness), int(none_blueVal*brightness))
print('none_color: ',none_color)

show_color_eins_a=(0,0,0)
show_color_eins_b=(0,0,0)
show_color_zwei=(0,0,0)
show_color_drei=(0,0,0)
show_color_fuenf=(0,0,0)

# Für FibonacciRechnung
h_eins_a=False
h_eins_b=False
h_zwei=False
h_drei=False
h_fuenf=False
m_eins_a=False
m_eins_b=False
m_zwei=False
m_drei=False
m_fuenf=False

# Initialisierung WS2812/NeoPixel
np = neopixel.NeoPixel(Pin(pin_np, Pin.OUT), leds)

# Ländereinstellung
network.country('DE')

# Client-Betrieb
wlan = network.WLAN(network.STA_IF)

# WLAN-Interface aktivieren
wlan.active(True)

# WLAN-Verbindung herstellen
wlan.connect(SSID, PASSWORD)

# WLAN-Verbindungsstatus prüfen
import time
print('Warten auf WLAN-Verbindung')
while not wlan.isconnected() and wlan.status() >= 0:
    time.sleep(1)
print('WLAN-Verbindung hergestellt / Status:', wlan.status())

if wlan.isconnected():
    # Zeit setzen
    owntime.setTime()
    print('Zeit wurde aus dem Wlan geholt')


while True:
    modeVal=ModePin.read_u16()
    Modus=int(modeVal/6555)
    print('Modus: ',Modus)
    
    lightVal=LightPin.read_u16()
    brightness=lightFaktor*lightVal/65550
    print(lightFaktor,lightVal,brightness)
    hour_color = (int(hour_redVal*brightness), int(hour_greenVal*brightness), int(hour_blueVal*brightness))
    min_color = (int(min_redVal*brightness), int(min_greenVal*brightness), int(min_blueVal*brightness))
    both_color = (int(both_redVal*brightness), int(both_greenVal*brightness), int(both_blueVal*brightness))
    none_color = (int(none_redVal*brightness), int(none_greenVal*brightness), int(none_blueVal*brightness))
#    print(hour_color,min_color,both_color,none_color)
    # Datum und Uhrzeit lesen
    # Uhrzeit ändern
    datetime = owntime.localTime(TZ_OFFSET)

#	deaktiviert, da es häufig zu Programm-Abstürzen führt
#    if (datetime[5]+1)%5==0 and datetime[6]==0:
#        # NTP-Zeit holen
#        tm = owntime.getTimeNTP()
#        print(tm)
#        # Zeit einstellen
#        machine.RTC().datetime((tm[0], tm[1], tm[2], tm[3], tm[4], tm[5], tm[6],tm[7]))
#        print('Uhrzeit eingestellt: %02d:%02d:%2d' % (tm[4], tm[5],tm[6]))
#        print(tm[0],tm[1],tm[2],tm[3],tm[4],tm[5],tm[6])
#        print()


    if datetime[4]>=13:
        hours=datetime[4]-12
    else:
        hours=datetime[4]
        
    minutes=datetime[5]
    seconds=datetime[6]
    minutes_show=int(minutes/5)
    minutes_rest=minutes%5
#    print('hours: ', hours)
#    print('minutes: ', minutes)
#    print('minutes_show: ', minutes_show)
#    print('minutes_rest: ',minutes_rest)
    

    if (seconds)%15==0:
        print('   Minute:', minutes)
        print('  Sekunde:', seconds)
        print('   Stunde:', hours)
        print('minutes_show:', minutes_show)
        print('hours: ',h_eins_a, h_eins_b, h_zwei, h_drei, h_fuenf)
        print('minutes: ',m_eins_a, m_eins_b, m_zwei, m_drei, m_fuenf)
        
    show_color_eins_a=(0,0,0)
    show_color_eins_b=(0,0,0)
    show_color_zwei=(0,0,0)
    show_color_drei=(0,0,0)
    show_color_fuenf=(0,0,0)
    h_eins_a=False
    h_eins_b=False
    h_zwei=False
    h_drei=False
    h_fuenf=False
    m_eins_a=False
    m_eins_b=False
    m_zwei=False
    m_drei=False
    m_fuenf=False

#_________________________________________________________________________________________
    # Abfrage welche Zahlen angezeigt werden sollen
    # hours
    if hours >= 8:
        h_fuenf=True
        if hours-5==7:
            h_eins_a=True
            h_eins_b=True
            h_zwei=True
            h_drei=True
        if hours-5==6:
            h_eins_a=True
            h_zwei=True
            h_drei=True
        if hours-5==5:
            h_zwei=True
            h_drei=True
        if hours-5==4:
            h_eins_a=True
            h_drei=True
        if hours-5==3:
            h_drei=True
        if hours-5==2:
            h_zwei=True
        if hours-5==1:
            h_eins_a=True
        
    if hours==7:
        h_zwei=True
        h_fuenf=True
    if hours==6:
        h_eins_a=True
        h_fuenf=True
    if hours==5:
        h_fuenf=True
    if hours==4:
        h_eins_a=True
        h_drei=True
    if hours==3:
        h_drei=True
    if hours==2:
        h_zwei=True
    if hours==1:
        h_eins_a=True
        
    #________________________________________________________________________
    # minutes    
    if minutes_show >= 8:
        m_fuenf=True
        if minutes_show-5==7:
            m_eins_a=True
            m_eins_b=True
            m_zwei=True
            m_drei=True
        if minutes_show-5==6:
            m_eins_b=True
            m_zwei=True
            m_drei=True
        if minutes_show-5==5:
            if h_zwei:
                m_eins_a=True
                m_einb_b=True
            else:
                m_zwei=True
            m_drei=True            
        if minutes_show-5==4:
            m_eins_b=True
            if h_drei:
                m_zwei=True
                m_eins_a=True
            else:
                m_drei=True
        if minutes_show-5==3:
            if h_drei:
                m_zwei=True
                m_eins_b=True
            else:
                m_drei=True
        if minutes_show-5==2:
            if h_zwei:
                m_eins_a=True
                m_eins_b=True
            else:
                m_zwei=True
        if minutes_show-5==1:
            m_eins_b=True
        
    if minutes_show==7:
        if h_zwei:
            m_eins_a=True
            m_eins_b=True
        else:
            m_zwei=True
        m_fuenf=True
    if minutes_show==6:
        m_eins_b=True
        if h_fuenf:
            m_zwei=True
            m_drei=True
        else:
            m_fuenf=True
    if minutes_show==5:
        if h_fuenf:
            m_eins_a=True
            m_eins_b=True
            m_drei=True
        else:
            m_fuenf=True
    if minutes_show==4:
        m_eins_b=True
        if h_drei:
            m_zwei=True
            m_eins_a=True
        else:
            m_drei=True
    if minutes_show==3:
        if h_drei:
            m_zwei=True
            m_eins_b=True
        else:
            m_drei=True
    if minutes_show==2:
        if h_zwei:
            m_eins_a=True
            m_eins_b=True
        else:
            m_zwei=True
    if minutes_show==1:
        m_eins_b=True


    # Bestimmung der Anzeigenfarbe
    # eins_a
    if h_eins_a and m_eins_a:
        show_color_eins_a = both_color
    elif h_eins_a:
        show_color_eins_a = hour_color
    elif m_eins_a:
        show_color_eins_a = min_color
    else:
        show_color_eins_a = none_color

    # eins_b
    if h_eins_b and m_eins_b:
        show_color_eins_b = both_color
    elif h_eins_b:
        show_color_eins_b = hour_color
    elif m_eins_b:
        show_color_eins_b = min_color
    else:
        show_color_eins_b = none_color

    # zwei
    if h_zwei and m_zwei:
        show_color_zwei = both_color
    elif h_zwei:
        show_color_zwei = hour_color
    elif m_zwei:
        show_color_zwei = min_color
    else:
        show_color_zwei = none_color

    # drei
    if h_drei and m_drei:
        show_color_drei = both_color
    elif h_drei:
        show_color_drei = hour_color
    elif m_drei:
        show_color_drei = min_color
    else:
        show_color_drei = none_color


    # fuenf
    if h_fuenf and m_fuenf:
        show_color_fuenf = both_color
    elif h_fuenf:
        show_color_fuenf = hour_color
    elif m_fuenf:
        show_color_fuenf = min_color
    else:
        show_color_fuenf = none_color

#_________________________________________________________________________________________
# LED-Bereiche für Zahlen
    # eins_a
    for i in range (2,3):
        np[i] = show_color_eins_a
    # eins_b
    for i in range (13,14):
        np[i] = show_color_eins_b
    # zwei
    for i in range (0,2):
        np[i] = show_color_zwei
    for i in range (14,16):
        np[i] = show_color_zwei
    # drei
    for i in range (16,19):
        np[i] = show_color_drei
    for i in range (29,32):
        np[i] = show_color_drei
    for i in range (32,35):
        np[i] = show_color_drei
    # fuenf
    for i in range (3,8):
        np[i] = show_color_fuenf
    for i in range (8,13):
        np[i] = show_color_fuenf
    for i in range (19,24):
        np[i] = show_color_fuenf
    for i in range (24,29):
        np[i] = show_color_fuenf
    for i in range (35,40):
        np[i] = show_color_fuenf
       
    np.write()
    
    sleep(1)





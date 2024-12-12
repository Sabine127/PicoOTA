from ota import OTAUpdater
from WIFI_CONFIG import SSID, PASSWORD

firmware_url = "https://github.com/Sabine127/PicoOTA.git"

ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "test.py")
ota_updater.download_and_install_update_if_available()


print('version erneuert')

from ota import OTAUpdater
from WIFI_CONFIG import SSID, PASSWORD

firmware_url = "https://drive.google.com/drive/folders/1sw3sqLbzB5_f0jwnQ1XUyzXsikQrHChz"

ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "test.py")
ota_updater.download_and_install_update_if_available()


print('version erneuert')
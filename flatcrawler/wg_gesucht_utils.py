
wg_gesucht_msg_base_url = "https://www.wg-gesucht.de/nachricht-senden.html?message_ad_id="

def write_wg_gesucht_message(advert_id: str, renter_name: str, city: str, language: str):
    msg_url = wg_gesucht_msg_base_url + advert_nr


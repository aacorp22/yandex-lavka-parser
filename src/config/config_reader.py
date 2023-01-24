import configparser
import logging


log = logging.getLogger("config")

keys = {
    "locations": {
        "location1",
        "location2",
        "location3",
        "location4"
    },
    "urls": {
        "snacks_url",
        "energetics_url"
    },
    "good_classes": {
        "good_class",
        "good_name",
        "good_price",
        "good_comment",
        "good_weight",
        "good_discount",
        "good_image",
        "snack_excel_save_name",
        "energetic_excel_save_name"
    },
    "html_classes": {
        "location_button",
        "clear_input",
        "input_field",
        "ok_button"
    }
}

def get_config() -> dict:
    log.info("Starting config parser")
    _conf = configparser.ConfigParser()
    _conf.read("config.ini", encoding="utf-8")
    config = {section: dict(_conf.items(section)) for section in _conf.sections()}
    
    for section in keys:
        for k in keys[section]:
            if k not in config[section].keys():
                log.error(f"Missing value in config. Key: {k}")
                raise RuntimeError

    log.info("Config downloaded successfully")
    
    return config

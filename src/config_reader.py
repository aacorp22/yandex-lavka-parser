import configparser
import logging


log = logging.getLogger("config")

_conf = configparser.ConfigParser()
_conf.read("config.ini", encoding="utf-8")
config = {section: dict(_conf.items(section)) for section in _conf.sections()}

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
    "snacks": {
        "snack_class",
        "snack_name",
        "snack_price",
        "snack_comment",
        "snack_weight",
        "snack_discount",
        "snack_image",
        "snack_excel_save_name"
    },
    "energetics": {
        "energetic_class",
        "energetic_name",
        "energetic_price",
        "energetic_comment",
        "energetic_weight",
        "energetic_discount",
        "energetic_image",
        "energetic_excel_save_name"
    },
    "html_classes": {
        "location_button",
        "clear_input",
        "input_field",
        "ok_button"
    }
}

for section in keys:
    for k in keys[section]:
        if k not in config[section].keys():
            log.error(f"Missing value in config. Key: {k}")
            raise RuntimeError

from pathlib import Path
import json
import sys


def get_config(config_path, options):
    if Path(config_path).exists() and config_path.endswith(".json"):
        loadedConfig = json.load(open(config_path, "r"))
        if "input" in loadedConfig:
            options["input"] = [loadedConfig["input"]]
        if "stylesheets" in loadedConfig:
            options["stylesheets"] = [loadedConfig["stylesheets"]]
        if "lang" in loadedConfig:
            options["lang"] = loadedConfig["lang"]
        if "output" in loadedConfig:
            options["output"] = loadedConfig["output"]
        return options

    print("ERROR: Could not find config file")
    sys.exit(1)


def get_sidebar_config(config_path, options):
    if Path(config_path).exists() and config_path.endswith(".json"):
        loadedConfig = json.load(open(config_path, "r"))
        options["sidebar"] = loadedConfig["sidebar"]
        options["sidebar"]["items"] = (
            [options["sidebar"]["items"]]
            if isinstance(options["sidebar"]["items"], str)
            else options["sidebar"]["items"]
        )

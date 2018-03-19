import json

from core.addon import TrollAddon
from core.patch import TrollPatch


def get_troll_patch(json_raw):
    """
    Parses the TrollGame Patch from a raw json.

    :param json_raw: The raw json string to be parsed.
    :return: The TrollPatch object read from the json or
    None if the raw json is None / invalid.
    """
    if json_raw is None:
        return None

    json_obj = json.loads(json_raw)

    json_patch = json_obj['patch']
    if json_patch is None:
        return None

    url = json_patch['url']
    if url is None:
        return None

    version = json_patch['version']
    if version is None:
        return None

    trollpatch = TrollPatch(url, version)
    return trollpatch


def get_troll_addons(json_raw):
    """
        Parses the TrollGame Addons list from a raw json.

        :param json_raw: The raw json string to be parsed.
        :return: A list of TrollAddon objects read from the json or
        None if the raw json is None / invalid.
        """
    if json_raw is None:
        return None

    json_obj = json.loads(json_raw)

    json_addons = json_obj['addons']
    if json_addons is None:
        return None

    addons = []
    for json_addon in json_addons:
        addon_obj = json_addons[json_addon]
        if addon_obj is None:
            continue

        parsed_name = addon_obj['name']
        if parsed_name is None:
            continue

        parsed_url = addon_obj['url']
        if parsed_url is None:
            continue

        parsed_version = addon_obj['version']
        if parsed_version is None:
            continue

        new_addon = TrollAddon(name=parsed_name, url=parsed_url, version=parsed_version)
        addons.append(new_addon)
    return addons

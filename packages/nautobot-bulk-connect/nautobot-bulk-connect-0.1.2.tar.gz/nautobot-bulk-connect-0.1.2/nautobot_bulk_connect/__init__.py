from nautobot.extras.plugins import PluginConfig


class ChangeConfig(PluginConfig):
    name = 'nautobot_bulk_connect'
    verbose_name = 'Bulk Connect'
    description = 'A plugin for bulk connect'
    version = '0.1.0'
    author = "Gesellschaft für wissenschaftliche Datenverarbeitung mbH Göttingen"
    author_email = "netzadmin@gwdg.de"
    base_url = 'nautobot-bulk-connect'
    required_settings = [
        'device_role'
    ]
    default_settings = {}
    middleware = []


config = ChangeConfig

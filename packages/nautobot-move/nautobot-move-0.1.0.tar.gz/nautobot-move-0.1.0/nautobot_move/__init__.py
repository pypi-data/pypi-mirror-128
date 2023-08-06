from nautobot.extras.plugins import PluginConfig


class MoveConfig(PluginConfig):
    name = "nautobot_move"
    verbose_name = "Move"
    description = "A plugin for moving devices"
    version = "0.1.0"
    author = "Gesellschaft für wissenschaftliche Datenverarbeitung mbH Göttingen"
    author_email = "netzadmin@gwdg.de"
    base_url = "nautobot-move"
    required_settings = []
    default_settings = {}
    middleware = []


config = MoveConfig

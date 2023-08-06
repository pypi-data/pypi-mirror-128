from nautobot.extras.plugins import PluginConfig


class ReapplyConfig(PluginConfig):
    name = 'nautobot_type_reapply'
    verbose_name = 'Type Re-Apply'
    description = 'A plugin for re-applying device types'
    version = "0.1.0"
    author = "Gesellschaft für wissenschaftliche Datenverarbeitung mbH Göttingen"
    author_email = "netzadmin@gwdg.de"
    base_url = 'nautobot-type-reapply'
    required_settings = [
    ]
    default_settings = {
    }
    middleware = [
    ]


config = ReapplyConfig

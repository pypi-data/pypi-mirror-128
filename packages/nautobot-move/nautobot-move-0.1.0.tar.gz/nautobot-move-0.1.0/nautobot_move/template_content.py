from nautobot.extras.plugins import PluginTemplateExtension


class MoveTemplate(PluginTemplateExtension):
    model = "dcim.device"

    def buttons(self):
        device = self.context["object"]

        return self.render(
            "nautobot_move/inc/buttons.html",
            {
                "device": device,
            },
        )


template_extensions = [MoveTemplate]

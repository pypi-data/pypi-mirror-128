from nautobot.extras.plugins import PluginTemplateExtension


class DeviceReapplyTemplate(PluginTemplateExtension):
    model = 'dcim.device'

    def buttons(self):
        device = self.context['object']

        if not device.device_type:
            return ""

        return self.render('nautobot_type_reapply/inc/buttons.html', {
            'device': device,
        })


template_extensions = [DeviceReapplyTemplate]

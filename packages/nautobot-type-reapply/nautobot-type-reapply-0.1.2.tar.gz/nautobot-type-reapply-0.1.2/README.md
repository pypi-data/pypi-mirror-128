# Nautobot Type Re-Apply

This plugin inserts a button to re-apply device types on a device on demand.

Please note that this plugin uses internal Nautobot components, which is
explicitly discouraged by the documentation. We promise to keep the plugin up
to date, but the latest version might break on unsupported Nautobot version.
Your mileage may vary.

## Installation

The plugin can be found on [pypi](https://pypi.org/project/nautobot-type-reapply).
You should therefore be able to install it using `pip`:

```
pip install nautobot-type-reapply
```

Make sure to use the same version of `pip` that manages Nautobot, so if you’ve
set up a virtual environment, you will have to use `<venv>/bin/pip` instead.

After that, you should be able to install the plugin as described in [the
Nautobot documentation](https://nautobot.readthedocs.io/en/stable/plugins/). No
change to `PLUGINS_CONFIG` is necessary.

## Usage

Once this plugin is installed, a button will appear on devices that allows you
to reapply the device type, which will add and delete device components
according to the definition of the type.

<img alt="The button" src="./docs/button.png" width="150">

You will be asked for confirmation and all changes that will be applied will be
listed before the actual operation.

![The confirmation form](./docs/form.png)

<hr/>

Have fun!

"""Support for IAQ-Pro monitor."""
import logging
import requests

from homeassistant.const import (CONF_NAME, CONF_HOST,)
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Perform the setup for IAQ-Pro monitor."""

    host = config.get(CONF_HOST)
    name = config.get(CONF_NAME)

    _LOGGER.info("Initializing IAQ-Pro with host {}.".format(host))

    devices = []
    iaq = IAQProDevice(name, host)
    devices.append(iaq)
    add_devices(devices)

class IAQProDevice(Entity):
    """Representation of an IAQ-Pro."""

    def __init__(self, name, host):
        """Initialize the IAQ-Pro."""
        self._state = None
        self._name = name
        self._host = host
        self._data_json = {}
        self.update_data()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return 'mdi:cloud'

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return 'IAQ'

    @property
    def device_state_attributes(self):
        """Return the state attributes of the last update."""
        attrs = {}
        try:
            attr_list = self._data_json["tag"]
            for tag in attr_list:
                if tag.startswith('Sensor-'):
                    continue
                attrs[tag] = '{val} {unit}'.format(
                    val = self._data_json["content"][tag]["value"],
                    unit = self._data_json["content"][tag]["unit"]
                )
        except:
            attrs = {}
        return attrs

    def update_data(self, timeout=0.2):
        try:
            r = requests.get('http://{}/temp/appData.json'.format(self._host))
            self._data_json = r.json()
            self._state = self._data_json["AQI"]
        except:
            self._data_json = {}
            self._state = None
            _LOGGER.exception('Fail to get data from IAQ-Pro')

    def update(self):
        """Get the latest data and updates the states."""
        self.update_data()

# Homeassistant-MTI-IAQ-Pro
Using MTI IAQ-Pro as custom sensor component for Home Assistant

<img src="https://github.com/robmarkcole/Homeassistant-MTI-IAQ-Pro/master/images/screenshot.jpg">

## Installation
1. **cp iaq_pro.py <config_dir>/custom_components/sensor/**
2. Get the **IP** from checking **IAQ-Pro**.

## Configuration
```<your_config_file>.yaml
sensor:
  - platform: iaq_pro
    host: <ip_of_iaq_pro>
    name: <custom_device_name>
    scan_interval: (int)<default:30>
```
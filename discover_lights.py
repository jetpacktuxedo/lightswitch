import json
import lifxlan

lifx = lifxlan.LifxLAN()
rawlights = lifx.get_lights()

lights = {}
for light in rawlights:
    lights[light.get_label()] = {
            'mac': light.get_mac_addr(),
            'ip': light.get_ip_addr()
            }

with open('lights.json', 'w') as lightsout:
    json.dump(lights, lightsout, indent=2, sort_keys=True)

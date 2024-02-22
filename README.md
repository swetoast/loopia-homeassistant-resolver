# Dynamic DNS Update for Home Assistant

This project is a Flask application that updates the dynamic DNS records for a list of hostnames with Loopia as the DNS provider. It also includes a Home Assistant sensor and automation.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/dyndns-update.git
    ```
2. Navigate to the project directory:
    ```bash
    cd dyndns-update
    ```
3. Install the required Python packages:
    ```bash
    pip install Flask requests configparser
    ```

## Configuration

1. Open `dns_endpoint.conf` in a text editor.
2. Under the `[Credentials]` section, set `username` and `password` to your Loopia DNS credentials.
3. Under the `[Hostnames]` section, set `hostnames` to a comma-separated list of hostnames to update.
4. Under the `[DEFAULT]` section, set `HOST`, `PORT`, `USE_HTTPS`, `CERTIFICATE_PATH`, and `KEY_PATH` as needed.

## Running the Application

1. Start the application:
    ```bash
    python app.py
    ```
2. The application will now update your dynamic DNS records whenever you access `http://IP_ADDRESS:PORT/update_dyndns`.

## Home Assistant Sensor

To add a sensor in Home Assistant that triggers the dynamic DNS update:

1. Add the following to your `configuration.yaml`:
    ```yaml
    sensor:
      - platform: rest
        resource: http://IP_ADDRESS:PORT/update_dyndns
        name: DNS Resolver
        value_template: '{{ value_json[0].status }}'
        json_attributes:
          - 'hostname'
          - 'ip_address'
        scan_interval:
          hours: 4
    ```
2. Restart Home Assistant to apply the changes.

## Home Assistant Automation

To add an automation in Home Assistant that triggers the dynamic DNS update when the IP address does not match:

1. Add the following to your `automations.yaml`:
    ```yaml
    alias: "Auto-Update: Update DNS Resolver on IP Mismatch"
    description: >-
      This automation updates the DNS Resolver sensor when its IP address does not
      match with the external IP sensor.
    trigger:
      - platform: template
        value_template: >-
          {{ states('sensor.external_ip') != state_attr('sensor.dns_resolver',
          'ip_address') }}
    action:
      - service: homeassistant.update_entity
        target:
          entity_id: sensor.dns_resolver
        data: {}
    mode: restart
    ```
2. Restart Home Assistant to apply the changes.

## License

This project is unlicensed.

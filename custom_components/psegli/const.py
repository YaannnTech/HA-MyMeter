"""Constants for the PSEG Long Island integration."""

DOMAIN = "psegli"

# Defaults
DEFAULT_NAME = "PSEG Long Island"
DEFAULT_SCAN_INTERVAL = 300  # 5 minutes

# Configuration
CONF_COOKIE = "cookie"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_MFA_METHOD = "mfa_method"  # "email" or "sms"
CONF_SITE = "site"

# MyMeter sites, keyed like the addon's SITES.
# service_type: MyMeter's /Dashboard/SetServiceType value for electric (1), for sites whose
# accounts can also have gas (4); the chart otherwise shows whatever was last viewed.
SITES = {
    "pseg_li": {"name": "PSEG Long Island", "mymeter_host": "mysmartenergy.psegliny.com"},
    "pseg_nj": {"name": "PSE&G New Jersey", "mymeter_host": "mysmartenergy.nj.pseg.com", "service_type": 1},
}
DEFAULT_SITE = "pseg_li"

# Addon configuration
CONF_ADDON_URL = "addon_url"
DEFAULT_ADDON_URL = "http://localhost:8000"

# Sensor names
SENSOR_TOTAL_ENERGY = "total_energy"
SENSOR_DAILY_USAGE = "daily_usage"
SENSOR_WEEKLY_USAGE = "weekly_usage"
SENSOR_CURRENT_USAGE = "current_usage"
SENSOR_OFF_PEAK_USAGE = "off_peak_usage"
SENSOR_ON_PEAK_USAGE = "on_peak_usage"
SENSOR_TEMPERATURE = "temperature"

# Sensor attributes
ATTR_LAST_UPDATE = "last_update"
ATTR_COMPARISON = "comparison"
ATTR_DESCRIPTION = "description" 
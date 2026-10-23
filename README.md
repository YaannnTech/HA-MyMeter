# PSEG Long Island Home Assistant Integration

> **About this fork:** HA-MyMeter is a fork of [daswass/ha-psegli](https://github.com/daswass/ha-psegli) that adds support for other utilities on the MyMeter usage portal. It currently supports **PSEG Long Island** and **PSE&G New Jersey**; more MyMeter sites are the goal. Changes are offered back upstream ([#11](https://github.com/daswass/ha-psegli/issues/11)).
>
> To use this fork, add `https://github.com/YaannnTech/HA-MyMeter` wherever the instructions below say `https://github.com/daswass/ha-psegli`.
>
> Not affiliated with or endorsed by PSEG, VertexOne, or Accelerated Innovations (MyMeter).

A Home Assistant integration for PSEG Long Island that provides automated energy usage data collection and statistics updates using a dedicated automation addon.

## 🚀 **Architecture Overview**

This integration uses a **two-component approach**:

1. **PSEG Long Island Automation Addon**: Handles automated login, reCAPTCHA bypass, and cookie management
2. **PSEG Long Island Integration**: Lightweight component that fetches energy data using the addon's authentication

### **How It Works:**

1. **User Configuration**: Enter PSEG credentials in the integration setup
2. **Automated Login**: Addon uses Playwright to handle reCAPTCHA and login
3. **Cookie Management**: Addon provides fresh authentication cookies to the integration
4. **Data Retrieval**: Integration fetches energy usage data from PSEG API
5. **Automatic Refresh**: Cookies are automatically refreshed when they expire

## 🌐 **Supported Utilities**

| Utility | Site | Login |
|---|---|---|
| PSEG Long Island (default) | `mysmartenergy.psegliny.com` | PSEG Long Island My Account |
| PSE&G New Jersey | `mysmartenergy.nj.pseg.com` | PSE&G My Account (Okta), with email or SMS verification code |

Choose the utility when adding the integration. Both use the same MyMeter usage portal. Time-of-use accounts get `psegli:on_peak_usage` and `psegli:off_peak_usage` statistics; flat-rate accounts (such as PSE&G NJ Residential Service) get a single `psegli:total_usage` statistic. Add it under **Settings → Dashboards → Energy → Electricity grid**.

## 📋 **Prerequisites**

- Home Assistant OS, Core, or Supervised installation
- PSEG Long Island account credentials (username/email and password)
- Internet access for PSEG API calls

## 🔧 **Installation**

### **Step 1: Install the Automation Addon**

1. **Add the custom repository:**

   - Go to **Settings** → **Add-ons** → **Add-on Store**
   - Click the three dots menu (⋮) → **Repositories**
   - Add: `https://github.com/daswass/ha-psegli`
   - Click **Add**

2. **Install the addon:**

   - Find **PSEG Long Island Automation** in the store
   - Click **Install**
   - Wait for installation to complete
   - Click **Start**

3. **Verify the addon is running:**
   - Check that the addon shows "Running" status
   - The addon provides a web interface at port 8000

### **Step 2: Install the Integration**

1. **Copy the integration files:**

   ```bash
   # From your HA system
   cp -r custom_components/psegli /config/custom_components/
   ```

2. **Restart Home Assistant**

3. **Add the integration:**
   - Go to **Settings** → **Devices & Services**
   - Click **Add Integration**
   - Search for **PSEG Long Island**
   - Enter your PSEG username/email and password
   - Click **Submit**

## ⚙️ **Configuration**

### **Integration Setup**

The integration configuration is simple - just enter your PSEG credentials:

- **Username/Email**: Your PSEG account email address
- **Password**: Your PSEG account password
- **Cookie**: A working Cookie from a manual login to https://mysmartenergy.psegliny.com/Dashboard

### **Automatic Operation**

Once configured, the integration will:

- Fetch energy usage data every 5 minutes
- Update Home Assistant Energy Dashboard statistics

With optional AddOn:

- Automatically log in to PSEG using the addon
- Handle reCAPTCHA challenges transparently
- Maintain authentication cookies automatically

## 🎯 **Features**

- **🔐 Automated Authentication**: No manual cookie management needed
- **🤖 reCAPTCHA Bypass**: Uses Playwright for automated login
- **📊 Energy Statistics**: Updates Home Assistant Energy Dashboard
- **🔄 Automatic Refresh**: Handles cookie expiration seamlessly
- **⏱️ Real-time Data**: Hourly interval data from PSEG

## 🔍 **How It Works**

1. **Initial Setup**: User enters PSEG credentials in integration setup
2. **Addon Communication**: Integration calls addon API to get fresh cookies
3. **Automated Login**: Addon uses Playwright to handle reCAPTCHA and login
4. **Cookie Provision**: Addon returns valid authentication cookies
5. **Data Fetching**: Integration uses cookies to call PSEG API
6. **Automatic Refresh**: Process repeats when cookies expire

## 🐛 **Troubleshooting**

### **Addon Not Available**

- Check if addon is running in **Settings** → **Add-ons**
- Verify addon logs for errors
- Ensure port 8000 is available
- Check addon health at `/api/health`

### **Integration Setup Issues**

- Verify addon is running before adding integration
- Check Home Assistant logs for configuration errors
- Ensure PSEG credentials are correct
- Verify internet connectivity

### **Authentication Issues**

- Check addon logs for login failures
- Verify PSEG account is active and not locked
- Ensure reCAPTCHA is accessible from your network
- Check if PSEG has changed their login process

### **MFA / "Enter MFA Code" action not showing**

If the `psegli.enter_mfa_code` action doesn't appear in Developer Tools > Actions:

1. **Reload the integration** – Go to Settings > Integrations > PSEG Long Island > ⋮ > Reload

2. **Use Options flow** – You can still complete MFA via Settings > Integrations > PSEG Long Island > ⋮ > Options (leave cookie empty, Submit, then enter the code)

### **Data Not Updating**

- Check integration logs for API errors
- Verify addon is providing valid cookies
- Check PSEG website accessibility
- Verify integration is enabled and running

## 📊 **Data Structure**

The integration provides:

- **Hourly Energy Usage**: kWh consumption per hour
- **Daily Totals**: Aggregated daily consumption
- **Statistics**: Long-term energy tracking
- **Energy Dashboard**: Integration with HA Energy features

## 🆘 **Support**

- **Addon Issues**: Check addon logs in Home Assistant
- **Integration Issues**: Check Home Assistant logs
- **PSEG Issues**: Verify account status on PSEG website
- **GitHub Issues**: Report bugs at [ha-psegli repository](https://github.com/daswass/ha-psegli)

## 🚀 **Advanced Usage**

### **Manual Refresh**

```yaml
service: psegli.update_statistics
```

### **Addon API Endpoints**

The addon provides these endpoints:

- `GET /health` - Health check
- `POST /login` - Login with username/password
- `POST /login-form` - Login with form data

## 📝 **Changelog**

### **v2.5.6**

- Check for hourly readings only on series that are imported (no more warning about the Temperature series)

### **v2.5.5**

- PSE&G NJ: select the electric meter (`/Dashboard/SetServiceType?ServiceType=1`) before fetching usage, so the data no longer depends on the meter last viewed on the MyMeter website

### **v2.5.4**

- Skip chart series that are not hourly: MyMeter returns the chart last viewed on its website, and a monthly view (e.g. PSE&G NJ gas) was imported as hourly kWh
- New action `psegli.clear_statistics` to delete imported statistics, e.g. to re-import them with `update_statistics` after wrong data was imported
- Specify `mean_type` and `unit_class` for imported statistics (required from Home Assistant 2026.11)
- Debug log no longer includes the `__RequestVerificationToken` value

### **v2.5.3**

- Send the keep-alive every 4 minutes instead of 10: MyMeter sessions appear to last about 10 minutes and are only renewed by a request in the second half of that time
- Debug log: names of the cookies MyMeter sets on each session check (never their values)

### **v2.5.2**

- Accept the session cookie MyMeter renews in its responses and save it to the config entry; the client previously kept sending the cookie as first entered, so sessions expired shortly after sign-in no matter how often they were used

### **v2.5.1**

- Keep the MyMeter session alive with a lightweight dashboard request every 10 minutes; MyMeter ends idle sessions sooner than the 30-minute schedule
- Show a notification when the session expires and no addon is available to log in again, with steps to paste a new cookie
- Add a 60-second timeout to MyMeter requests (a stalled request could block checks for over 15 minutes); a network error no longer counts as an expired cookie
- Run the scheduled refresh as a background task so it does not delay Home Assistant shutdown

### **v2.5.0**

- Add PSE&G New Jersey support: choose the utility during integration setup (existing setups stay on PSEG Long Island)
- Addon: new `site` field on `POST /login` (`pseg_li` default, `pseg_nj`); NJ logs in through MyMeter's SAML sign-in and PSE&G's Okta page, including email/SMS MFA
- Switch addon base image to Debian 12 (bookworm); Debian 11 packages are no longer available
- Import usage for flat-rate accounts as `psegli:total_usage` (previously only On-Peak/Off-Peak series were imported)
- Fix hourly readings shifting by an hour outside daylight saving time (and by 4 hours on hosts not set to Eastern time): read MyMeter's timestamps as local wall-clock time instead of adding a fixed 4 hours
- Fix a cookie entered via Configure not being used until the integration was reloaded
- Fix expired sessions being reported as valid: MyMeter answers an expired session with an AJAX redirect instead of a login page, so the scheduled cookie refresh never ran

### **v2.4.7**

- Fix addon communication on Home Assistant OS: discover addon via Supervisor instead of `localhost:8000`
- Increase login/MFA timeout to 300s for long Playwright flows

### **v2.4.6**

- Fix Options flow for Home Assistant 2025.12+ (`config_entry` is now read-only on OptionsFlow)

### **v2.4.5**

- Allow integration setup to complete when MFA required (call enter_mfa_code with code)
- Add INFO logging for statistics update start/completion

### **v2.4.4**

- Skip scheduled cookie refresh when cookie still valid (avoid MFA every 30 min)
- Auto-update statistics after enter_mfa_code and on scheduled runs
- Trigger update_statistics after refresh_cookie succeeds

### **v2.4.3**

- Fix MFA code submission flow (wait_for_selector, iframe support, get_by_placeholder fallback)
- Add HEADED=1 env var for local MFA debugging

### **v2.4.2**

- Fix enter_mfa_code action: register identically to refresh_cookie and update_statistics (no configuration.yaml needed)

### **v2.4.1**

- Bump version to force integration reload (fixes enter_mfa_code action visibility)
- MFA support: enter_mfa_code service for completing verification from Developer Tools

### **v2.3.1**

- Cleanup logging

### **v2.3.0**

- Improved auto-update scheduling

### **v2.2.0**

- Refactored Add-On
- Improved statistics calculation

### **v2.1.3**

- Add-On retry improvements

### **v2.1.2**

- Update Stealth version

### **v2.1.1**

- Add-On logic updates

### **v2.1.0**

- Fully functional integration with optional Add-On

### **v2.0.0**

- **Major Architecture Change**: Now uses Home Assistant addon for automation
- **Simplified Setup**: No more manual cookie management
- **Automated reCAPTCHA**: Playwright handles all browser automation
- **Repository Installation**: Addon installs from custom repository
- **User-Friendly Configuration**: Simple username/password form
- **Automatic Cookie Refresh**: Seamless authentication management

### **v1.0.0**

- Initial release with manual cookie management
- Basic PSEG API integration
- Energy Dashboard integration

## 🤝 **Contributing**

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Note**: This integration requires the PSEG Long Island Automation Addon to function. The addon handles all browser automation and reCAPTCHA challenges automatically, making the integration much more user-friendly than previous versions.

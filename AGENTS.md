# HA-MyMeter

Fork of [daswass/ha-psegli](https://github.com/daswass/ha-psegli) that adds support for other utilities on the MyMeter usage portal (currently PSEG Long Island and PSE&G New Jersey). Changes are meant to go back upstream, so they must stay additive.

## Layout

- `custom_components/psegli/`: the Home Assistant integration. Fetches hourly usage from MyMeter with a session cookie and imports it as external statistics.
- `addons/psegli-automation/`: the Home Assistant add-on. A FastAPI service on port 8000 that logs in with Playwright and returns MyMeter cookies (`POST /login`, then `POST /login/mfa` when a verification code is needed).
- `repository.yaml` makes the repo a Supervisor add-on repository; `hacs.json` makes it a HACS custom integration repository.

## Upstream rules

- Keep the integration domain `psegli`, its services and config entry keys unchanged. PSEG Long Island stays the default everywhere, so existing setups behave exactly as before.
- One concern per upstream PR, on its own branch cut from `upstream/main` (e.g. `fix/...`, `feat/...`).
- Fork-only changes never go into PR branches: the "About this fork" README note, `repository.yaml` URL/maintainer, `AGENTS.md`.
- Upstream has ignored issues so far (none answered since 2025-08). Don't block fork work on upstream review.

## Sites

The supported sites are defined twice and must stay in sync: `SITES` in `addons/psegli-automation/auto_login.py` (adds `okta_signin_url` for sites that log in through MyMeter's SAML entry point) and `SITES` in `custom_components/psegli/const.py`. The config entry stores the key as `site`; entries without it are `pseg_li`.

## MyMeter behavior worth knowing

- Data endpoints: `/Dashboard` (HTML with a `__RequestVerificationToken` form field), `POST /Dashboard/Chart` (sets the chart context), `GET /Dashboard/ChartData` (JSON series).
- Session cookies: `MM_SID` and `__RequestVerificationToken`. The add-on returns them as `MM_SID=...; __RequestVerificationToken=...`, which is also the format of the manual cookie field.
- `MM_SID` is an ASP.NET Core cookie (`CfDJ8...`). The client keeps cookies in the `requests` cookie jar (never a fixed `Cookie` header) and stores any renewed cookie back in the config entry, in case MyMeter ever sends one.
- An expired session does not produce a login URL. Because the client sends `X-Requested-With: XMLHttpRequest`, MyMeter answers `/Dashboard` with HTTP 200 and `{"AjaxResults":[{"Action":"Redirect","Value":"/"}]}`. Without that header it redirects to `/`. See `PSEGLIClient._is_logged_out`.
- Chart timestamps are the utility's local wall-clock time encoded as if UTC. Read them with `datetime.fromtimestamp(ts, tz=timezone.utc).replace(tzinfo=None)`; never add a fixed offset.
- Data lags about two days behind real time.
- Time-of-use accounts (LI) return On-Peak/Off-Peak series (`psegli:on_peak_usage`, `psegli:off_peak_usage`). Flat-rate accounts (NJ Residential Service) return one meter series, imported as `psegli:total_usage`. Temperature is always skipped.
- PSE&G NJ gas is monthly only and is intentionally not imported.
- `POST /Dashboard/Chart` does not name a meter. The service is chosen with `GET /Dashboard/SetServiceType?ServiceType=N` (302 back to `/Dashboard`; PSE&G NJ: 1 = electric, 4 = gas), stored in the session. Sites with a `service_type` in `SITES` select it before each fetch; as a second guard, `_process_chart_data` skips series that are not hourly.
- MyMeter does not renew `MM_SID` via Set-Cookie on `/Dashboard`; sessions end after a server-side idle timeout between 4 and 10 minutes. The integration sends a keep-alive every 4 minutes.

## PSE&G NJ login

- Entry point `https://mysmartenergy.nj.pseg.com/Saml/okta-prod/SignIn` redirects to PSE&G's Okta (`id.myaccount.pseg.com`), standard Okta Sign-In Widget (identifier first, then password, then an email/SMS authenticator), then back through MyMeter's `/acs` to `/Dashboard`.
- Okta can show a reCAPTCHA image challenge after the username. Do not try to solve or bypass it (no solver services, no audio-challenge tricks). The add-on detects it, saves `okta_fail_debug.html` and `.png`, and fails. A human-in-the-loop login is the acceptable alternative.
- Direct MyMeter login (email/password form on the MyMeter page) is retired for NJ.

## Versions and changelog

- Integration version: `custom_components/psegli/manifest.json`. Add-on version: `addons/psegli-automation/config.yaml` and `build.yaml`, always bumped together; the Supervisor only rebuilds when it changes.
- Changelog lives in `README.md` under "Changelog", newest first.
- `hacs.json` requires Home Assistant 2024.12.0 because the options flow relies on `OptionsFlow.config_entry`.

## Testing

There is no test suite. What works:

- `python3 -m py_compile` on changed files.
- Add-on image: `docker build -t hamymeter-test:nj addons/psegli-automation`, then e.g. `docker run --rm hamymeter-test:nj python auto_login.py --site pseg_nj --email ... --password ...`.
- Data client outside Home Assistant: copy `psegli.py`, `const.py`, `exceptions.py` into a temporary `psegli/` package next to a stub `homeassistant/exceptions.py` (`class HomeAssistantError(Exception): pass`), in a venv with `requests` and `beautifulsoup4`.
- An expired-cookie check against the live sites needs no account: any fake `MM_SID` must be rejected by `_test_connection_sync`.
- Anything needing a real session or login runs on the user's side. Scripts must prompt with `getpass` and print only summaries. Never ask for passwords or cookie values in chat, and never print or commit them.
- Avoid repeated failed logins against PSE&G's Okta; they can make its bot checks stricter.

## Style

Match the surrounding upstream code: emoji-prefixed log messages in the add-on, `_LOGGER` with %-formatting in the integration, 4-space indentation, blank lines inside methods carry trailing indentation in older upstream code.

# SkopeoGate

Webapplicatie om OCI-archieven (`.tar`) via een uploadformulier naar een skopeo-bestemming te kopiëren.

## Configuratie

De applicatie wordt geconfigureerd via omgevingsvariabelen:

| Variabele | Verplicht | Standaard | Beschrijving |
|---|---|---|---|
| `SKOPEO_DESTINATION` | Ja | - | Skopeo-bestemmingsadres, bijv. `docker://mijn.registry.com:5000/myrepo` |
| `SKOPEO_USERNAME` | Nee | - | Gebruikersnaam voor authenticatie bij de bestemming (`--dest-username`) |
| `SKOPEO_PASSWORD_FILE` | Nee | - | Pad naar een bestand met het wachtwoord voor de bestemming (`--dest-password`) |
| `MAX_MB` | Nee | `400` | Maximale uploadgrootte in MB |

Voorbeeld:

```
SKOPEO_DESTINATION=docker://mijn.registry.com:5000/myrepo
SKOPEO_USERNAME=gebruiker
SKOPEO_PASSWORD_FILE=/run/secrets/skopeo-password
MAX_MB=400
```

Er is ook een [`.env-example`](.env-example)-bestand beschikbaar als startpunt. Kopieer dit naar `.env` en pas de waarden aan:

```
cp .env-example .env
```

---

## Lokaal starten via `uv run`

Naast de container-images kan de applicatie ook rechtstreeks lokaal worden gestart met [uv](https://docs.astral.sh/uv/).

> [!IMPORTANT]
> Zorg dat de vereiste omgevingsvariabelen (zie [Configuratie](#configuratie)) zijn ingesteld voordat je de applicatie start, bijvoorbeeld via een `.env`-bestand of door ze te exporteren in de shell.

- `uv sync` — installeert de dependencies uit `pyproject.toml`/`uv.lock` in een virtuele omgeving
- `uv run fastapi run main.py` — start de applicatie in productiemodus
- `uv run fastapi dev main.py` — start de applicatie in ontwikkelmodus (met auto-reload)

---

# Offline methode

Alle bestanden zijn beschikbaar tijdens de image build.

> [!IMPORTANT]
> Zorg dat de mappen `./packages` en `./wheels` zijn aangemaakt!

## Binnenhalen van benodigde dependencies (via internet)

- `podman run --rm -v "${PWD}/packages:/packages" --user root registry.access.redhat.com/ubi10/ubi:latest bash -c "dnf download --resolve --destdir /packages skopeo"`
- `podman run --rm -v "${PWD}/wheels:/wheels" --user root registry.access.redhat.com/ubi10/python-312-minimal:latest pip download "fastapi[standard]" -d /wheels`

## Image bouwen

- `podman build --no-cache --build-arg BUILD_MODE=offline -t skopeogate:offline .`

---

# Online methode

Alle bestanden worden via het internet binnengehaald.

## Image bouwen

- `podman build --no-cache --build-arg BUILD_MODE=online -t skopeogate:online .`

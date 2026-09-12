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
MAX_MB=200
SKOPEO_USERNAME=gebruiker
SKOPEO_PASSWORD_FILE=/run/secrets/skopeo-password
```

---

# Offline methode

Alle bestanden zijn beschikbaar tijdens de image build.

> [!IMPORTANT]
> Zorg dat de mappen `./packages` en `./wheels` zijn aangemaakt!

## Binnenhalen van benodigde dependencies (via internet)

- `podman run --rm -v "${PWD}/packages:/packages" --user root registry.access.redhat.com/ubi9/ubi:latest bash -c "dnf download --resolve --destdir /packages skopeo"`
- `podman run --rm -v "${PWD}/wheels:/wheels" --user root registry.access.redhat.com/ubi9/python-312-minimal:latest pip download "fastapi[standard]>=0.136.1" pydantic-settings -d /wheels`

## Image bouwen

- `podman build --no-cache --build-arg BUILD_MODE=offline -t skopeogate:offline .`

---

# Online methode

Alle bestanden worden via het internet binnengehaald.

## Image bouwen

- `podman build --no-cache --build-arg BUILD_MODE=online -t skopeogate:online .`

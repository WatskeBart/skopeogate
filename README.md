# SkopeoGate

Webapplicatie om OCI-archieven (`.tar`) via een uploadformulier naar een skopeo-bestemming te kopiëren.

## Configuratie

De applicatie wordt geconfigureerd via omgevingsvariabelen:

| Variabele | Standaard | Beschrijving |
|---|---|---|
| `DESTINATION` | `dir:/tmp/artifact_output` | Skopeo-bestemmingsadres, bijv. `docker://mijn.registry.com:5000/myrepo` |
| `MAX_SIZE_MB` | `100` | Maximale uploadgrootte in MB |
| `SKOPEO_ARGS` | `--dest-tls-verify=false` | Extra argumenten die aan `skopeo copy` worden meegegeven |

Voorbeeld:

```
DESTINATION=docker://mijn.registry.com:5000/myrepo
MAX_SIZE_MB=200
SKOPEO_ARGS=--dest-tls-verify=false --src-creds=gebruiker:wachtwoord
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

# Offline methode

Alle bestanden zijn beschikbaar tijdens de image build.

> [!important] Zorg dat de mappen `./packages` en `./wheels` zijn aangemaakt!

## Binnenhalen van benodigde dependencies (via internet)

- `podman run --rm -v "${PWD}/packages:/packages" --user root registry.access.redhat.com/ubi9/ubi:latest bash -c "dnf download --resolve --destdir /packages skopeo`
- `podman run --rm -v "${PWD}/wheels:/wheels" --user root registry.access.redhat.com/ubi9/python-312-minimal:latest pip download "fastapi[standard]>=0.136.1" -d /wheels`

## Image bouwen

- `podman build --no-cache --build-arg BUILD_MODE=offline -t upload-2-skopeo:offline .`

# Online methode

Alle bestanden worden via het internet binnen gehaald.

## Image bouwen

- `podman build --no-cache --build-arg BUILD_MODE=online -t upload-2-skopeo:online .`
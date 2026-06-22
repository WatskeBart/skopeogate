#!/bin/sh
set -eu

MODE=${BUILD_MODE:-offline}

if [ "$MODE" = "offline" ]; then
    if [ ! -d ./packages ] || [ ! -d ./wheels ]; then
        echo "Fout: mappen ./packages en ./wheels zijn vereist voor een offline build." >&2
        exit 1
    elif [ -z "$(ls ./packages/*.rpm 2>/dev/null)" ] || [ -z "$(ls ./wheels/*.whl 2>/dev/null)" ]; then
        echo "Fout: ./packages moet *.rpm bestanden bevatten en ./wheels moet *.whl bestanden bevatten." >&2
        exit 1
    fi
    rpm -Uvh --nodeps ./packages/*.rpm
    pip install --no-cache-dir --no-index --find-links ./wheels/ "fastapi[standard]"
    rm -rf ./{packages,wheels}
elif [ "$MODE" = "online" ]; then
    microdnf install -y skopeo
    microdnf clean all
    pip install --no-cache-dir "fastapi[standard]>=0.136.1"
    rm -rf /var/cache/yum
    rm -rf ./{packages,wheels}
else
    echo "Onbekende BUILD_MODE: '$MODE'. Gebruik 'offline' of 'online'." >&2
    exit 1
fi

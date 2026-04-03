# Référence — factory.py

Ce module gère le chargement dynamique des providers via `importlib`.
Les classes sont mises en cache avec `lru_cache` pour éviter les imports répétitifs.

## Enum `PaymentProviderPath`

Dot-paths vers les classes clients de chaque provider.

::: paygate_africa.factory.PaymentProviderPath

---

## Enum `ProviderSettingsPath`

Dot-paths vers les classes settings de chaque provider.

::: paygate_africa.factory.ProviderSettingsPath

---

## Fonctions

::: paygate_africa.factory.validate_payment_provider

::: paygate_africa.factory.load_provider_class

::: paygate_africa.factory.select_provider

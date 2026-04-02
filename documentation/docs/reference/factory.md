# Référence — factory.py

Ce module gère le chargement dynamique des providers via `importlib`.
Les classes sont mises en cache avec `lru_cache` pour éviter les imports répétitifs.

## Enum `PaymentProviderPath`

Dot-paths vers les classes clients de chaque provider.

::: paygate.factory.PaymentProviderPath

---

## Enum `ProviderSettingsPath`

Dot-paths vers les classes settings de chaque provider.

::: paygate.factory.ProviderSettingsPath

---

## Fonctions

::: paygate.factory.validate_payment_provider

::: paygate.factory.load_provider_class

::: paygate.factory.select_provider

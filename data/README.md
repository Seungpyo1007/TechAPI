# data/ — curated dataset

These JSON files are the **curated, validated** records the API serves. Layout is
singular folder names, organised by brand:

```
brand/<slug>.json
soc/<manufacturer>/<slug>.json
smartphone/<brand>/<slug>.json
gpu/<manufacturer>/<slug>.json
cpu/<manufacturer>/<year>/<slug>.json   # CPUs are additionally split by release year
```

> ⚠️ **This is a curated subset — NOT an exhaustive list of every device/chip.**
> It is hand-verified and intentionally partial. Breadth is expanded out-of-band
> through an internal pipeline that publishes curated records here after review;
> each record carries `source_urls`. Don't assume a device is missing-by-error —
> it may simply not be curated yet.

Validate after edits: `python -m scripts.validate`. Add only real, sourced models.

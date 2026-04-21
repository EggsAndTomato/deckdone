# Icon Library

Tabler Icons for DeckDone SVG slide generation.

## Setup

Icons are not included in the git repo. Download them with:

```bash
# Clone tabler-icons (MIT license) and copy
git clone --depth 1 https://github.com/tabler/tabler-icons.git /tmp/tabler-icons
cp -r /tmp/tabler-icons/icons/filled/ skills/deckdone-build/templates/icons/tabler-filled/
cp -r /tmp/tabler-icons/icons/outline/ skills/deckdone-build/templates/icons/tabler-outline/
rm -rf /tmp/tabler-icons
```

| Library | Style | Count | viewBox |
|---------|-------|-------|---------|
| `tabler-filled` | Fill, bezier-curve contours | 1,000+ | `0 0 24 24` |
| `tabler-outline` | Stroke / line | 5,000+ | `0 0 24 24` |

## Usage in SVG

```xml
<use data-icon="tabler-outline/home" x="100" y="200" width="48" height="48" fill="#0076A8"/>
<use data-icon="tabler-filled/chart-bar" x="300" y="200" width="48" height="48" fill="#DE3545"/>
```

One library per presentation — never mix.

## License

MIT License, Copyright (c) 2020 Paweł Kuna. See `THIRD_PARTY_LICENSES` for full text.

# jakubtatarkiewicz.github.io

Strona osobista Jakuba Tatarkiewicza wraz z projektami z zakresu analizy danych.

Dostępna pod [jakubtatarkiewicz.com](https://jakubtatarkiewicz.com) (VPS) oraz
przez GitHub Pages.

## Struktura

- `index.html` + `assets/` — wizytówka (strona główna)
- `Analiza-sygnalow-rynkowych/` — analiza sygnałów rynkowych (raport Quarto)
- `Porownanie-metod-iteracyjnych/` — porównanie metod iteracyjnych
- `Work/` — dokumenty (CV, resume)

## Deployment

Push na gałąź `main` automatycznie publikuje stronę na VPS
(GitHub Actions → rsync przez SSH, patrz `.github/workflows/deploy.yml`).

- Na serwer trafiają **wyłącznie pliki będące stroną** (whitelista rozszerzeń:
  html/css/js/obrazy/wideo/fonty/pdf). Źródła (`.qmd`, `.R`, `.m`, `.csv`,
  `.py`, `.md`) pozostają tylko w repozytorium.
- Deploy działa w trybie **mirror** (`--delete`): pliki usunięte z repo są
  usuwane również z serwera.

# Styl "Cinematic Editorial Dark" — przewodnik

Styl wypracowany na wizytówce jakubtatarkiewicz.com (wariant index3).
Charakter: ciemne, filmowe tło + szampańskie złoto + typografia zamiast ramek.

## 1. Paleta kolorów

### Kolory bazowe

| Rola | Wartość | Użycie |
|---|---|---|
| Tło bazowe | `#0b1220` | tło strony pod wideo / fallback; głęboki granatowo-czarny |
| Tekst główny | `#eef4f8` | nagłówki, treść — chłodna złamana biel, nigdy czysta `#fff` |
| Tekst drugorzędny | `rgba(238, 244, 248, 0.72)` | leady, opisy, metadane — ta sama biel z opacity 72% |

### Akcent (szampańskie złoto)

| Rola | Wartość | Użycie |
|---|---|---|
| Akcent | `#e2b25f` | eyebrow, daty, separatory, główna akcja, aktywne stany |
| Akcent jasny (hover) | `#f0c87e` | rozjaśnienie akcentu przy interakcji |
| Tekst na akcencie | `#241a06` | gdy złoto jest tłem (np. aktywny segment przełącznika) |
| Poświata akcentu | `rgba(226, 178, 95, 0.35)` | box-shadow pod złotymi wypełnieniami |

### Powierzchnie i linie

| Rola | Wartość | Użycie |
|---|---|---|
| Szkło ciemne | `rgba(10, 18, 28, 0.55)` + `backdrop-filter: blur(12px)` | tylko drobne pływające elementy (przełącznik języka, tooltipy) |
| Linia włoskowa | `rgba(238, 244, 248, 0.16)` | separatory, obwódki — zawsze 1px, nigdy pełne ramki |
| Przyciemnienie tła | gradienty `rgba(11, 18, 32, 0.2-0.7)` | radial + linear nakładka na wideo/zdjęcie |
| Cień tekstu | `0 2px 14-18px rgba(0, 0, 0, 0.6)` | czytelność tekstu leżącego wprost na tle |

## 2. Tło

- Pełnoekranowe wideo (lub zdjęcie) przypięte `position: fixed` pod całością (`z-index: 0`).
- Obróbka: `filter: blur(10px) saturate(1.15) brightness(0.6)` + `transform: scale(1.08)`
  (scale ukrywa rozmyte krawędzie).
- Wideo: spowolnione (`playbackRate ≈ 0.67`), zapętlone bez cięcia (plik ping-pong:
  przód + tył sklejone ffmpeg-iem), `muted autoplay loop playsinline`.
- Na wierzchu nakładka: `radial-gradient` (jaśniej w 1/3 od góry-lewej) + `linear-gradient`
  (ciemniej dołem) — wartości w sekcji paleta.
- Zawsze fallback dla `prefers-reduced-motion`: statyczny gradient zamiast wideo.

## 3. Typografia

| Rola | Font | Rozmiar | Waga | Detale |
|---|---|---|---|---|
| Display (hero) | Playfair Display (serif) | `clamp(46px, 9.5vw, 104px)` | 500 | line-height 1.06, letter-spacing 0.01em |
| Nagłówki sekcji | Inter | `clamp(28px, 5vw, 38px)` | 700-800 | line-height 1.05 |
| Eyebrow (nadtytuł) | Inter | 12px | 800 | UPPERCASE, letter-spacing 0.14em, kolor akcentu |
| Body / lead | Inter | 16-17px | 400 | line-height 1.6, kolor drugorzędny |
| Tagi / metadane | Inter | 13-14px | 700-750 | UPPERCASE, letter-spacing 0.08em |
| Linki-akcje | Inter | 16px | 750 | bez uppercase |

Zasada: serif tylko dla jednego wielkiego napisu display; całe UI groteskiem (Inter).
Kontrast serif/grotesk robi charakter, nadużyty — teatralność.

## 4. Komponenty bez ramek (klucz stylu)

Nic nie siedzi w pudełku. Wyróżnianie przez typografię, nie przez tła:

- **Lista tagów**: wersaliki z rozstrzelonym światłem w jednej linii, rozdzielone
  złotą kropką `·` (font-weight 900, kolor akcentu, odstęp 14px z obu stron).
- **Akcja główna**: złoty link tekstowy ze stałym podkreśleniem 2px (`currentColor`)
  i strzałką `→`, która przy hoverze przesuwa się o 4-6px w prawo (200ms ease).
- **Akcje drugorzędne**: białe linki, podkreślenie animowane `transform: scaleX(0→1)`
  od lewej (220ms ease), strzałka `↗` dla linków zewnętrznych; hover = kolor akcentu jasnego.
- **Separatory sekcji**: pusta przestrzeń (rytm 96px) + linia włoskowa tam, gdzie konieczna.
- **Oś czasu**: okrągłe białe znaczniki 52px (logo, `border: 2px` linia włoskowa),
  pionowa linia włoskowa 2px między nimi, data w złocie nad tytułem.
- **Tooltip / toast / przełącznik**: jedyne dopuszczalne "szkło" — ciemna pigułka
  `rgba(10,18,28,0.55)` + `backdrop-filter: blur(12px)`, border włoskowy, radius 999px.

## 5. Ruch

- Przejścia mikro: 160-220ms `ease` (kolor, transform, opacity). Nic dłuższego w UI.
- Hover na linkach: podkreślenie rośnie od lewej + strzałka odjeżdża.
- Wskaźnik scrolla: strzałka z animacją "bob" (translateY 0→7px, 1.8s ease-in-out infinite).
- Przewijanie kotwic: `scroll-behavior: smooth`.
- Szanuj `prefers-reduced-motion: reduce` — wyłącz wideo i animacje dekoracyjne.

## 6. Layout

- Jedna kolumna treści `max-width: 680px`, wyśrodkowana; szeroki margines powietrza.
- Ekran otwarcia: 100vh, tylko display-nazwa + eyebrow, wyśrodkowane; cała reszta niżej.
- Rytm pionowy sekcji: 96px odstępu, padding boczny 20px na mobile.
- Zaokrąglenia: 999px (pigułki), 6-10px (tooltips); brak kart, więc mało radiusów.

## 7. Duch stylu (jak decydować w nowych sytuacjach)

1. Zanim dodasz tło/ramkę — spróbuj typografii: wagi, wersalików, światła, złotej kropki.
2. Złoto jest rzadkie: akcent, nie wypełniacz. Jeden złoty element na widok wystarczy.
3. Biel zawsze złamana (`#eef4f8`), czernie zawsze granatowe (`#0b1220`, `rgba(10,18,28,…)`).
4. Tekst na obrazie = zawsze cień tekstu + przyciemnienie tła; czytelność przed efektem.
5. Interakcje sygnalizuj ruchem (podkreślenie, strzałka), nie zmianą tła.

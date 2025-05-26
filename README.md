## README – Automatyzacja budowania i publikacji wieloarchitekturalnego obrazu Docker z testem bezpieczeństwa (GitHub Actions)

### Opis projektu

Repozytorium zawiera aplikację webową (Flask), która jest budowana i publikowana jako obraz Docker na publicznym rejestrze GitHub Container Registry (GHCR). Proces CI/CD jest zrealizowany w GitHub Actions i obejmuje:

- Budowę obrazu na podstawie Dockerfile oraz kodu źródłowego,
- Obsługę dwóch architektur: `linux/amd64` oraz `linux/arm64`,
- Wykorzystanie cache warstw Docker (eksporter: registry, backend: DockerHub, tryb max),
- Automatyczne skanowanie obrazu pod kątem podatności CVE (Trivy),
- Publikację wyłącznie obrazów wolnych od krytycznych i wysokich zagrożeń,
- Przesyłanie obrazu do publicznego repozytorium autora na GHCR.

---

## Sposób działania pipeline

1. **Checkout kodu**
Pobranie kodu źródłowego z repozytorium.
2. **Konfiguracja środowiska multiarchitekturalnego**
    - Ustawienie QEMU do emulacji architektur,
    - Ustawienie Buildx do budowy obrazów na różne platformy.
3. **Logowanie do rejestrów**
    - DockerHub (dla cache warstw),
    - GHCR (dla publikacji obrazu).
4. **Budowa i publikacja obrazu Docker**
    - Budowa z Dockerfile,
    - Obsługa platform: `linux/amd64`, `linux/arm64`,
    - Wykorzystanie cache warstw (eksporter/odbiorca: registry, dedykowane repozytorium na DockerHub, tryb max),
    - Tagowanie obrazu (szczegóły poniżej),
    - Wysyłka obrazu do GHCR.
5. **Skanowanie bezpieczeństwa (CVE)**
    - Skanowanie obrazu narzędziem Trivy,
    - Pipeline przerywa publikację, jeśli wykryte zostaną podatności o poziomie CRITICAL lub HIGH.
6. **Publikacja raportu bezpieczeństwa**
    - Wyniki skanowania są przesyłane do zakładki Security w repozytorium GitHub.

---

## Sposób tagowania obrazów i cache

**Obrazy Docker:**

- `ghcr.io/zie-lu/pawchozad2:latest` – zawsze najnowszy obraz z głównej gałęzi,
- `ghcr.io/zie-lu/pawchozad2:<commit_SHA>` – unikalny tag dla każdego commita (umożliwia identyfikację wersji i łatwe rollbacki).

**Cache warstw Docker:**

- Cache warstw jest przechowywany w dedykowanym, publicznym repozytorium DockerHub, np.
`docker.io/pzielinski123/cache-pawchozad2:buildcache`
- Używany jest tryb `max`, co zapewnia maksymalne wykorzystanie cache i skraca czas budowy kolejnych obrazów.
- Taki sposób tagowania cache (np. `buildcache`) pozwala na łatwe zarządzanie i czyszczenie cache w razie potrzeby oraz unika konfliktów między różnymi projektami lub gałęziami.

**Uzasadnienie wyboru:**

- Tagowanie obrazów przez `latest` i hash commita jest praktyką rekomendowaną przez społeczność Docker/GitHub Actions – zapewnia jednoznaczną identyfikację wersji oraz wsparcie dla automatycznych deploymentów i rollbacków.
- Cache warstw w dedykowanym repozytorium i trybie `max` minimalizuje czas budowy, a jednocześnie nie zanieczyszcza głównego repozytorium obrazów produkcyjnych.

---

## Skanowanie bezpieczeństwa – wybór narzędzia

Wybrano **Trivy** jako narzędzie do automatycznego skanowania obrazów pod kątem podatności CVE, ponieważ:

- Jest szybki, prosty w integracji z GitHub Actions i szeroko stosowany w środowisku open source,
- Pozwala na blokowanie pipeline w przypadku wykrycia podatności CRITICAL/HIGH,
- Wyniki mogą być automatycznie przesyłane do zakładki Security w repozytorium.

---

## Wymagane sekrety repozytorium

- `DOCKERHUB_USERNAME` – login do DockerHub (dla cache)
- `DOCKERHUB_TOKEN` – token/pat do DockerHub
- `GHCR_TOKEN` – token do GHCR (można użyć `${{ secrets.GITHUB_TOKEN }}` jeśli repozytorium jest Twoje)

---

## Uruchamianie:
- docker pull ghcr.io/zie-lu/pawchozad2:latest
- docker run -p 5000:5000 ghcr.io/zie-lu/pawchozad2:latest
- docker run --platform linux/amd64 -p 5000:5000 ghcr.io/zie-lu/pawchozad2:latest
- docker run --platform linux/arm64 -p 5000:5000 ghcr.io/zie-lu/pawchozad2:latest

## Podsumowanie

Pipeline spełnia wszystkie wymagania zadania:

- Buduje i publikuje multiarchitekturalny obraz Docker,
- Efektywnie wykorzystuje cache warstw w dedykowanym repozytorium,
- Automatycznie skanuje obraz i blokuje publikację w razie wykrycia krytycznych/zagrażających podatności,
- Stosuje rekomendowane praktyki tagowania obrazów i cache.

---


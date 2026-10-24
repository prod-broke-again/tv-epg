# EPG publisher

Раз в 6 часов GitHub Actions скачивает https://iptvx.one/epg/epg.xml.gz, собирает компактный `epg.json` для каналов из `channels.json` и публикует его в ветку `data`.

## Настройка (один раз)
1. Создай публичный репозиторий на GitHub (например `tv-epg`) и залей в него содержимое этой папки.
2. Settings → Actions → General → Workflow permissions: Read and write.
3. Actions → Update EPG → Run workflow (первый запуск вручную).
4. В `.env` лаунчера: `EPG_URL=https://raw.githubusercontent.com/<логин>/tv-epg/data/epg.json` и пересобрать приложение.

Если iptvx.one не отдаёт файл с серверов GitHub, в логе будет ошибка скачивания; тогда напиши, подберём другое зеркало.

## Если поменялся список каналов
Скопируй новый `app/src/main/assets/channels.json` в корень этого репозитория.

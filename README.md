# RimWorld-Ukrainian
Repository of Ukrainian localization for RimWorld.

## Як долучитися?

1. Основним джерелом перекладів є
  [проект](https://crowdin.com/project/rimworld-ukr) на платформі CrowdIn.
  Усі нові переклади варто робити спершу там, задля уникнення розбіжностей
  між перекладами у цьому репозиторі та на CrowdIn. Завантажити переклади з
  CrowdIn у цей репозиторій можна за допомогою скрипта:
  `./Notes/scripts/download-translated-files.py --access-token abcde12345`.
  Токен для скрипта можна створити в [налаштуваннях](https://crowdin.com/settings#api-key)
  профілю користувача на CrowdIn. Детальніше про параметри скрипта:

  ```console
  $ ./Notes/scripts/download-translated-files.py -h
usage: download-translatef-files.py [-h] [--project-identifier PROJECT_IDENTIFIER] [--access-token ACCESS_TOKEN]

Replace local files with latest version from CrowdIn.

options:
  -h, --help            show this help message and exit
  --project-identifier PROJECT_IDENTIFIER
                        Crowdin project identifier
  --access-token ACCESS_TOKEN
                        Crowdin API v2 access token
  ```

  Для запуску скрипта потрібен Python 3.6+.

2. Переклади також можна додавати напряму сюди. Це робити не бажано, бо такі
  переклади може бути втрачено під час синхронізації перекладу з CrowdIn.
 
В будь-якому випадку, насамперед вам варто ознайомитися із [вікі](https://github.com/Ludeon/RimWorld-Ukrainian/wiki).
Також у нагоді стане посилання, розміщене нижче.

## See this page for important license info:
http://ludeon.com/forums/index.php?topic=2933.0

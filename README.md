# RimWorld-Ukrainian
Repository of Ukrainian localization for RimWorld.

## Як долучитися?

1. Основним джерелом перекладів є
  [проект](https://crowdin.com/project/rimworld-ukr) на платформі CrowdIn.
  Усі нові переклади варто робити спершу там, задля уникнення розбіжностей
  між перекладами у цьому репозиторі та на CrowdIn. Завантажити переклади з
  CrowdIn у цей репозиторій можна за допомогою скрипта:
  `./scripts/import-from-crowdin.py -p rimworld-urk -k abcde12345`. Ключ для
  скрипта можна знайти у вкладці API налаштувань проекту на CrowdIn (доступна
  для менеджерів проекту). Детальніше про параметри скрипта:

  ```console
  $ ./scripts/import-from-crowdin.py -h
  usage: import-from-crowdin.py [-h] [-p PROJECT_IDENTIFIER] [-k PROJECT_KEY]

  Replace local translations with latest version from CrowdIn.

  optional arguments:
    -h, --help            show this help message and exit
    -p PROJECT_IDENTIFIER, --project-identifier PROJECT_IDENTIFIER
                          Crowdin project identifier
    -k PROJECT_KEY, --project-key PROJECT_KEY
                          Crowdin API project key
  ```

  Для запуску скрипта потрібен Python 3.6+.

2. Переклади також можна додавати напряму сюди. Це робити не бажано, бо такі
  переклади може бути втрачено під час синхронізації перекладу з CrowdIn.
 
В будь-якому випадку, насамперед вам варто ознайомитися із [вікі](https://github.com/Ludeon/RimWorld-Ukrainian/wiki).
Також у нагоді стане посилання, розміщене нижче.

## See this page for important license info:
http://ludeon.com/forums/index.php?topic=2933.0

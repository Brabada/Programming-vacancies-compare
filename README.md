# Programming vacancies compare

Project that present average salaries for TOP-15 programming languages from hh.ru and superjob.ru in console.

List of languages: JavaScript, Java, Python, Ruby, PHP, C++, C#, C, Go, Objective-C, Scala, Swift, TypeScript.

Criteria of search:
- Salary must be in rubles;
- Only Moscow;
- Fetching vacancies for last 30 days.


### How to install
For start you need `Python3` and `pip`.

For installing required packages:
```shell
$ cd "path_where_is_script"
$ pip install -r "requirements.txt"
```

After you should get ID of Moscow from https://api.hh.ru/areas and add to .env file.
For 05.10.22 ID of Moscow is **1**.

```shell
$ cd "path_where_is_script"
$ HH_MOSCOW_CITY_ID=1 > .env
```

Then get secret key for application SuperJob: https://api.superjob.ru/register.
It's look like that: `v3.r.137031281.8054edeea860dbc1bbc9ac7ab85e21606306f085.20e67ea8db18ff01e22169dcd914984a3ade7a56`

And add this key to existing .env as:
`SUPERJOB=API_KEY=v3.r.137031281.8054edeea860dbc1bbc9ac7ab85e21606306f085.20e67ea8db18ff01e22169dcd914984a3ade7a56`

Take Moscow city id from there https://api.superjob.ru/2.0/towns/.
For 05.10.22 ID of Moscow is 4.

Add this id as to .env as:
`SJ_MOSCOW_CITY_ID=4`


## How to launch

```shell
$ cd "path_where_is_script"
$ python get_average_salary.py
```

It can take about 2 minutes.

Output must be:
```shell
+HeadHunter Moscow------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| JavaScript            | 7717             | 914                 | 149413           |
| Java                  | 4412             | 366                 | 186280           |
| Python                | 5110             | 542                 | 168862           |
| Ruby                  | 369              | 84                  | 192589           |
| PHP                   | 3442             | 1049                | 139785           |
| C++                   | 3030             | 668                 | 142401           |
| C#                    | 2912             | 638                 | 141647           |
| C                     | 7173             | 1020                | 152928           |
| Go                    | 1283             | 261                 | 222480           |
| Objective-C           | 254              | 54                  | 189433           |
| Scala                 | 319              | 23                  | 243152           |
| Swift                 | 748              | 153                 | 201493           |
| TypeScript            | 2367             | 518                 | 179609           |
+-----------------------+------------------+---------------------+------------------+
+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| JavaScript            | 41               | 31                  | 95677            |
| Java                  | 15               | 5                   | 173000           |
| Python                | 32               | 22                  | 108363           |
| Ruby                  | 3                | 1                   | 325000           |
| PHP                   | 15               | 12                  | 139743           |
| C++                   | 11               | 2                   | 159000           |
| C#                    | 6                | 5                   | 151200           |
| C                     | 10               | 3                   | 133333           |
| Go                    | 4                | 1                   | 300000           |
| Objective-C           | 2                | 0                   | 0                |
| Scala                 | 1                | 1                   | 240000           |
| Swift                 | 2                | 0                   | 0                |
| TypeScript            | 8                | 2                   | 78000            |
+-----------------------+------------------+---------------------+------------------+
```



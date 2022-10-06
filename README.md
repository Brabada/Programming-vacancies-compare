# Programming vacancies compare

Project that present average salaries for TOP-15 programming languages from [hh.ru](https://hh.ru/) and [superjob.ru](https://www.superjob.ru/) in console.

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

It can take about ~30 seconds.

Output must be:
```shell
+HeadHunter Moscow------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| JavaScript            | 2577             | 684                 | 176753           |
| Java                  | 2048             | 272                 | 223771           |
| Python                | 2218             | 397                 | 198859           |
| Ruby                  | 148              | 39                  | 219705           |
| PHP                   | 1157             | 523                 | 170768           |
| C++                   | 1159             | 327                 | 176378           |
| C#                    | 1032             | 254                 | 182334           |
| C                     | 2640             | 735                 | 174132           |
| Go                    | 675              | 145                 | 241220           |
| Objective-C           | 88               | 17                  | 263647           |
| Scala                 | 184              | 17                  | 251352           |
| Swift                 | 280              | 58                  | 248103           |
| TypeScript            | 931              | 223                 | 201793           |
+-----------------------+------------------+---------------------+------------------+
+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| JavaScript            | 43               | 33                  | 97515            |
| Java                  | 15               | 5                   | 173000           |
| Python                | 33               | 22                  | 108363           |
| Ruby                  | 3                | 1                   | 325000           |
| PHP                   | 17               | 13                  | 140070           |
| C++                   | 10               | 2                   | 159000           |
| C#                    | 5                | 5                   | 159000           |
| C                     | 11               | 4                   | 130000           |
| Go                    | 4                | 1                   | 300000           |
| Objective-C           | 2                | 0                   | 0                |
| Scala                 | 1                | 1                   | 240000           |
| Swift                 | 2                | 0                   | 0                |
| TypeScript            | 8                | 2                   | 78000            |
+-----------------------+------------------+---------------------+------------------+
```



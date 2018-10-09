# Databse code for the news DB

import psycopg2

DBNAME = "news"


TOP_3_ARTICLES = """
    select
        articles.title, count(log.id) as hits
    from
        articles join log on log.path like '%' || articles.slug
    group by
        articles.title
    order by
        hits desc
    limit
        3
        """

TOP_AUTHORS = """
    select
        authors.name, count(log.id) as hits
    from
        authors
        join articles on authors.id = articles.author
        join log on log.path like '%' || articles.slug

    group by
        authors.name
    order by
        hits desc
"""

HIGHEST_ERROR_DATE = QUERY_DAYS_WITH_HIGH_ERRORS = """
        select
            to_char(errors_by_day.date,'Month DD, YYYY'),
            to_char(((errors_by_day.count::decimal /
            requests_by_day.count::decimal) * 100),'0.0') || '%' as error_percent
        from
            (select date(time) as date, count(*) as count
            from log group by date(time)) as requests_by_day
        join
            (select date(time), count(*) from log where status != '200 OK'
             group by date(time)) as errors_by_day
        on
            requests_by_day.date = errors_by_day.date
        order by
            error_percent desc
        limit
            1;
        """


def report(query):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    posts = c.fetchall()
    db.close()
    return posts


def proper_print(table):
    for entry in table:
        print(str(entry[0]) + " - " + str(entry[1]))


print('--- TEST 1 ---')
proper_print(report(TOP_3_ARTICLES))

print('--- TEST 2 ---')
proper_print(report(TOP_AUTHORS))

print('--- TEST 3 ---')
proper_print(report(HIGHEST_ERROR_DATE))

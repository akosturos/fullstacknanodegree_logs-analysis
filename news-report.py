import psycopg2
import sys
import datetime

#DBNAME = "news"
#Goals and queries
##Goal #1
goalOneTitle = "Return top three most popular posts, by views:"
goalOneQuery = ("select articles.title, count(*) as views from articles"
                " join log on log.path"
                " like '%' || articles.slug || '%'"
                " where log.status like '%200%'"
                " group by articles.title, log.path"
                " order by views desc")
goalOneReturnAmount = 3

##Goal #2
goalTwoTitle = "Return most popular authors, by views:"
goalTwoQuery = ("select authors.name, count(*) as views"
                " from articles"
                " join authors on articles.author = authors.id"
                " join log on log.path like '%' || articles.slug || '%'"
                " where log.status like '%200%'"
                " group by authors.name"
                " order by views desc")
goalTwoReturnAmount = -1

##Goal #3
goalThreeTitle = "Return days where error rate was higher than %1, show error %:"
goalThreeQuery =("select day, error_rate from"
                 " (select day, sum(url_requests) / (select count(*)"
                        " from log where substring(cast(log.time as text), 0, 11) = day)"
                        " as error_rate from (select substring(cast(log.time as text), 0, 11)"
                        " as day, count(*) as url_requests from log"
                        " where status like '%404%' group by day)"
                        " as log_percentage group by day order by error_rate)"
                " as alias where error_rate >= .01000")
goalThreeReturnAmount = -1

def runQuery(query, queryTitle, returnAmount):
    """Return the top three most popular posts"""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute(query)
    posts = c.fetchall()
    db.close()
    #check to see if there will be an out of range error
    if(len(posts) < returnAmount or returnAmount <= 0):
        returnAmount = len(posts)

    # print and report
    print("\n" + queryTitle)
    for post in range(returnAmount):
        print(posts[post],)
    #print(posts[0])

def main():
    runQuery(goalOneQuery, goalOneTitle, goalOneReturnAmount)
    runQuery(goalTwoQuery, goalTwoTitle, goalTwoReturnAmount)
    runQuery(goalThreeQuery, goalThreeTitle, goalThreeReturnAmount)

if __name__ == '__main__':
    main()

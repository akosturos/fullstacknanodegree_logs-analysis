# LOGS ANALYSIS
To run: `pyhthon3 news-data.py` in your terminal

## Goal
### The goal of this analysis was to find the following:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?


## Description
### Objective 1 - Popular articles
In order to find the most popular articles, you need to create a view that has the article
name and also the count of the article. This is a pretty straightforward approach, but as you
dive deeper into the psql tables you start to see that there are some articles that have the url misspelled, and wrong article names. So the like feature of the search won't work perfectly,
you also have to make a constraint where the log status was 200, meaning the url was correct. In
my query I do not limit the total table, in order to verify that there are only values that
are correct urls, relating to correct articles.

####Query:
`select articles.title, count(*) as views from articles
 join log on log.path
 like '%' || articles.slug || '%'
 where log.status like '%200%'
 group by articles.title, log.path
 order by views desc;`


#### Result:
     title                              | views  
    ------------------------------------+--------
    Candidate is jerk, alleges rival    | 338647
    Bears love berries, alleges bear    | 253801
    Bad things gone, say good people    | 170098
    Goats eat Google's lawn             |  84906
    Trouble for troubled troublemakers  |  84810
    Balloon goons doomed                |  84557
    There are a lot of bears            |  84504
    Media obsessed with bears           |  84383
    (8 rows)




### Objective 2 - Popular authors
To get the most popular authors, we need to get all the successful, ie (200 status)
url visits for each article, then tie that back into the author that wrote it. We
can do this by grouping the count by the author name.

`select authors.name, count(*) as views
 from articles
 join authors on articles.author = authors.id
 join log on log.path like '%' || articles.slug || '%'
 where log.status like '%200%'
 group by authors.name
 order by views desc;`


#### Result:
    name          | views  
    ------------------------+--------
    Ursula La Multa        | 507594
    Rudolf von Treppenwitz | 423457
    Anonymous Contributor  | 170098
    Markoff Chaney         |  84557
    (4 rows)

### Objective 3 - Popular authors

To get the days where the error rate is more than 1%, we will have to look at the log
table, and sum up all the requests per day as the divisor, and sum up all the requests where
there was an error status 404 as the numerator.

`select day, error_rate from
 (select day, sum(url_requests) / (select count(*)
                from log where substring(cast(log.time as text), 0, 11) = day)
                as error_rate from (select substring(cast(log.time as text), 0, 11) as day,
                            count(*) as url_requests from log
                            where status like '%404%' group by day)
                as log_percentage group by day order by error_rate)
  as alias where error_rate >= .01000;`

#### Result:
    day     |       error_rate       
    ------------+------------------------
    2016-07-17 | 0.02262686246802725956
    (1 row)



  

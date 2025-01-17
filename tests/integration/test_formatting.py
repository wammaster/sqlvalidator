from sqlvalidator import format_sql


def test_format_select_star():
    sql = "select * from table;"
    expected = """
SELECT *
FROM table;
"""
    assert format_sql(sql) == expected.strip()


def test_upper_function_name():
    sql = "select sum(column) FROM table;"
    expected = """
SELECT SUM(column)
FROM table;
"""
    assert format_sql(sql) == expected.strip()


def test_nested_function_name():
    sql = "select ifnull(sum(col), 'NOTHING') from table_stmt;"
    expected = """
SELECT IFNULL(SUM(col), 'NOTHING')
FROM table_stmt;
"""
    assert format_sql(sql) == expected.strip()


def test_extract_function():
    sql = "select extract(day from date) from table_stmt;"
    expected = """
SELECT EXTRACT(DAY FROM date)
FROM table_stmt;
"""
    assert format_sql(sql) == expected.strip()


def test_no_from_statement():
    sql = "select 1;"
    expected = "SELECT 1;"
    assert format_sql(sql) == expected.strip()


def test_simple_column():
    sql = "select col from table_stmt;"
    expected = """
SELECT col
FROM table_stmt;
"""
    assert format_sql(sql) == expected.strip()


def test_conditional_column():
    sql = "select col = 1 from table_stmt;"
    expected = """
SELECT col = 1
FROM table_stmt;
"""
    assert format_sql(sql) == expected.strip()


def test_conditional_parenthesis_columns():
    sql = "select (col + 1) = 4 as out from table_stmt;"
    expected = """
SELECT (col + 1) = 4 AS out
FROM table_stmt;
"""
    assert format_sql(sql) == expected.strip()


def test_simple_aliased_column():
    sql = "select col alias from table_stmt;"
    expected = """
SELECT col alias
FROM table_stmt;
"""
    assert format_sql(sql) == expected.strip()


def test_simple_aliased_as_column():
    sql = "select col as alias from table_stmt;"
    expected = """
SELECT col AS alias
FROM table_stmt;
"""
    assert format_sql(sql) == expected.strip()


def test_select_except_one_line():
    sql = "select * except(field) from table_stmt;"
    expected = """
SELECT * EXCEPT (field)
FROM table_stmt;
"""
    assert format_sql(sql) == expected.strip()


def test_select_except_multi_line():
    sql = "select * except(field, col, f2) from table_stmt;"
    expected = """
SELECT * EXCEPT (
 field,
 col,
 f2
)
FROM table_stmt;
"""
    assert format_sql(sql) == expected.strip()


def test_multiple_columns():
    sql = "select col, col2 from table_stmt;"
    expected = """
SELECT
 col,
 col2
FROM table_stmt;
"""
    assert format_sql(sql) == expected.strip()


def test_parenthesis():
    sql = "select (email,id), id from auth_user;"
    expected = """
SELECT
 (email, id),
 id
FROM auth_user;
"""
    assert format_sql(sql) == expected.strip()


def test_basic_arithmetic():
    sql = "select (1+1) add, 2*3, 9/3;"
    expected = """
SELECT
 (1 + 1) add,
 2 * 3,
 9 / 3;
"""
    assert format_sql(sql) == expected.strip()


def test_chained_arithmetic():
    sql = "select 1+1+1, 2*3-5"
    expected = """
SELECT
 1 + 1 + 1,
 2 * 3 - 5
"""
    assert format_sql(sql) == expected.strip()


def test_nested_queries():
    sql = "select field from (select field from table_stmt);"
    expected = """
SELECT field
FROM (
 SELECT field
 FROM table_stmt
);
"""
    assert format_sql(sql) == expected.strip()


def test_nested_queries_multiple_columns():
    sql = "select field, f2 from (select field, f2 from table_stmt);"
    expected = """
SELECT
 field,
 f2
FROM (
 SELECT
  field,
  f2
 FROM table_stmt
);
"""
    assert format_sql(sql) == expected.strip()


def test_two_nested_queries():
    sql = "select field from (select field, f2 from (select * from t));"
    expected = """
SELECT field
FROM (
 SELECT
  field,
  f2
 FROM (
  SELECT *
  FROM t
 )
);
"""
    assert format_sql(sql) == expected.strip()


def test_assert_no_semi_colon():
    sql = "select * from t"
    expected = """
SELECT *
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_quoted_from():
    sql = "select * from `table`;"
    expected = """
SELECT *
FROM `table`;
"""
    assert format_sql(sql) == expected.strip()


def test_where_clause_boolean_column():
    sql = "select * from t where col"
    expected = """
SELECT *
FROM t
WHERE col
"""
    assert format_sql(sql) == expected.strip()


def test_where_clause_boolean_equal():
    sql = "select * from t where col = true"
    expected = """
SELECT *
FROM t
WHERE col = TRUE
"""
    assert format_sql(sql) == expected.strip()


def test_where_clause_boolean_is():
    sql = "select * from t where col is true"
    expected = """
SELECT *
FROM t
WHERE col IS TRUE
"""
    assert format_sql(sql) == expected.strip()


def test_where_clause_str():
    sql = "select * from t where col = 'test'"
    expected = """
SELECT *
FROM t
WHERE col = 'test'
"""
    assert format_sql(sql) == expected.strip()


def test_where_clause_columns():
    sql = "select * from t where col = col2"
    expected = """
SELECT *
FROM t
WHERE col = col2
"""
    assert format_sql(sql) == expected.strip()


def test_where_clause_parenthesis_expression():
    sql = "select * from t where (col + 1) = col2"
    expected = """
SELECT *
FROM t
WHERE (col + 1) = col2
"""
    assert format_sql(sql) == expected.strip()


def test_where_clause_boolean():
    sql = "select * from t where col = 1 and col2=4"
    expected = """
SELECT *
FROM t
WHERE col = 1 AND col2 = 4
"""
    assert format_sql(sql) == expected.strip()


def test_where_clause_parenthesis_boolean():
    sql = "select * from t where (col = 1 and (col2=4))"
    expected = """
SELECT *
FROM t
WHERE (col = 1 AND (col2 = 4))
"""
    assert format_sql(sql) == expected.strip()


def test_where_clause_multiple_parenthesis_booleans():
    sql = (
        "select * from t where (col = 1 and col2=4) or (col = 2 and (col =6 or col=9))"
    )
    expected = """
SELECT *
FROM t
WHERE (col = 1 AND col2 = 4) OR (col = 2 AND (col = 6 OR col = 9))
"""
    assert format_sql(sql) == expected.strip()


def test_where_clause_multiple_booleans():
    sql = "select * from t where col = 1 and col2=4 And col = 2 and col =6 or (col=9)"
    expected = """
SELECT *
FROM t
WHERE col = 1 AND col2 = 4 AND col = 2 AND col = 6 OR (col = 9)
"""
    assert format_sql(sql) == expected.strip()


def test_boolean_conditions_select_where():
    sql = "select (col+1) = 3 AND col2=4 from t where (col+1) = 3 AND col2=4"
    expected = """
SELECT (col + 1) = 3 AND col2 = 4
FROM t
WHERE (col + 1) = 3 AND col2 = 4
"""
    assert format_sql(sql) == expected.strip()


def test_parenthesis_boolean_conditions_select_where():
    sql = "select ((col+1) = 3 AND col2=4) from t where ((col+1) = 3 AND col2=4)"
    expected = """
SELECT ((col + 1) = 3 AND col2 = 4)
FROM t
WHERE ((col + 1) = 3 AND col2 = 4)
"""
    assert format_sql(sql) == expected.strip()


def test_distinct_on_one_field():
    sql = "SELECT DISTINCT ON (location) location, time, report FROM weather_reports;"
    expected = """
SELECT DISTINCT ON (location)
 location,
 time,
 report
FROM weather_reports;
"""
    assert format_sql(sql) == expected.strip()


def test_distinct_on_multiple_fields():
    sql = (
        "SELECT DISTINCT ON (location, time) location, time, report "
        "FROM weather_reports;"
    )
    expected = """
SELECT DISTINCT ON (location, time)
 location,
 time,
 report
FROM weather_reports;
"""
    assert format_sql(sql) == expected.strip()


def test_empty_group_by():
    sql = "SELECT * from t group by ()"
    expected = """
SELECT *
FROM t
GROUP BY ()
"""
    assert format_sql(sql) == expected.strip()


def test_group_by():
    sql = "SELECT * from t GROUP BY col"
    expected = """
SELECT *
FROM t
GROUP BY col
"""
    assert format_sql(sql) == expected.strip()


def test_group_by_parenthesis():
    sql = "SELECT * from t GROUP BY (col)"
    expected = """
SELECT *
FROM t
GROUP BY (col)
"""
    assert format_sql(sql) == expected.strip()


def test_group_by_multiple_elements():
    sql = "SELECT * from t GROUP BY col1, col2, col3"
    expected = """
SELECT *
FROM t
GROUP BY
 col1,
 col2,
 col3
"""
    assert format_sql(sql) == expected.strip()


def test_group_by_multiple_elements_parenthesis():
    sql = "SELECT * from t GROUP BY (col1, col2, col3)"
    expected = """
SELECT *
FROM t
GROUP BY (col1, col2, col3)
"""
    assert format_sql(sql) == expected.strip()


def test_where_and_group_by():
    sql = "SELECT count(*) from t where x =3 GROUP BY col1;"
    expected = """
SELECT COUNT(*)
FROM t
WHERE x = 3
GROUP BY col1;
"""
    assert format_sql(sql) == expected.strip()


def test_group_by_parenthesis_rollup():
    sql = "SELECT * from t GROUP BY ROLLUP (col)"
    expected = """
SELECT *
FROM t
GROUP BY ROLLUP (col)
"""
    assert format_sql(sql) == expected.strip()


def test_group_by_multiple_elements_parenthesis_rollup():
    sql = "SELECT * from t GROUP BY ROLLUP (col1, col2, col3);"
    expected = """
SELECT *
FROM t
GROUP BY ROLLUP (col1, col2, col3);
"""
    assert format_sql(sql) == expected.strip()


def test_where_and_having():
    sql = "SELECT count(*) from t where x =3 having (sum(x) > 50);"
    expected = """
SELECT COUNT(*)
FROM t
WHERE x = 3
HAVING (SUM(x) > 50);
"""
    assert format_sql(sql) == expected.strip()


def test_order_by():
    sql = "SELECT * from t order by col"
    expected = """
SELECT *
FROM t
ORDER BY col
"""
    assert format_sql(sql) == expected.strip()


def test_order_by_mutliple_fields():
    sql = "SELECT * from t order by col, 2"
    expected = """
SELECT *
FROM t
ORDER BY
 col,
 2
"""
    assert format_sql(sql) == expected.strip()


def test_order_by_mutliple_fields_order():
    sql = "SELECT * from t order by col DESC, 2 ASC"
    expected = """
SELECT *
FROM t
ORDER BY
 col DESC,
 2 ASC
"""
    assert format_sql(sql) == expected.strip()


def test_limit():
    sql = "SELECT * from t limit 5"
    expected = """
SELECT *
FROM t
LIMIT 5
"""
    assert format_sql(sql) == expected.strip()


def test_limit_all():
    sql = "SELECT * from t limit all"
    expected = """
SELECT *
FROM t
LIMIT ALL
"""
    assert format_sql(sql) == expected.strip()


def test_offset():
    sql = "SELECT * from t offset 5"
    expected = """
SELECT *
FROM t
OFFSET 5
"""
    assert format_sql(sql) == expected.strip()


def test_subquery_where():
    sql = """
    SELECT any_value(url) f_0
    FROM (SELECT * FROM `toto`
    WHERE http_code <> 0 AND (STARTS_WITH(url, 'https') OR url = 'http://example.com'))
    GROUP BY url_hash
        """
    expected = """
SELECT ANY_VALUE(url) f_0
FROM (
 SELECT *
 FROM `toto`
 WHERE http_code <> 0 AND (STARTS_WITH(url, 'https') OR url = 'http://example.com')
)
GROUP BY url_hash
"""
    assert format_sql(sql) == expected.strip()


def test_aliased_subquery():
    sql = """
    SELECT subquery.field
    FROM (SELECT * FROM `table`
    WHERE value <> 0) subquery
    GROUP BY subquery.col
"""
    expected = """
SELECT subquery.field
FROM (
 SELECT *
 FROM `table`
 WHERE value <> 0
) subquery
GROUP BY subquery.col
"""
    assert format_sql(sql) == expected.strip()


def test_aliased_as_subquery():
    sql = """
    SELECT AGG(subquery.field)
    FROM (SELECT * FROM `table`
    WHERE value <> 0) as subquery
    GROUP BY subquery.col
"""
    expected = """
SELECT AGG(subquery.field)
FROM (
 SELECT *
 FROM `table`
 WHERE value <> 0
) AS subquery
GROUP BY subquery.col
"""
    assert format_sql(sql) == expected.strip()


def test_is_not_null_condition():
    sql = """
SELECT a.field field
FROM (SELECT field,
field_id
FROM test_1.table_2
WHERE col <> 0 AND long__name__col IS NOT NULL) a
ORDER BY a.field_id
"""
    expected = """
SELECT a.field field
FROM (
 SELECT
  field,
  field_id
 FROM test_1.table_2
 WHERE col <> 0 AND long__name__col IS NOT NULL
) a
ORDER BY a.field_id
"""
    assert format_sql(sql) == expected.strip()


def test_filter_not_predicate():
    sql = """
SELECT field
FROM tt where not bool_field
"""
    expected = """
SELECT field
FROM tt
WHERE NOT bool_field
"""
    assert format_sql(sql) == expected.strip()


def test_boolean_filter_not_predicate():
    sql = """
SELECT field
FROM tt where not bool_field and not (x = Y)
"""
    expected = """
SELECT field
FROM tt
WHERE NOT bool_field AND NOT(x = Y)
"""
    assert format_sql(sql) == expected.strip()


def test_boolean_filter_first_not_predicate():
    sql = """
SELECT field
FROM tt where not (bool_field) and (x = Y)
"""
    expected = """
SELECT field
FROM tt
WHERE NOT(bool_field) AND (x = Y)
"""
    assert format_sql(sql) == expected.strip()


def test_basic_join():
    sql = """
SELECT field
FROM table JOIN other_table USING (field)
"""
    expected = """
SELECT field
FROM table
JOIN other_table
USING (field)
"""
    assert format_sql(sql) == expected.strip()


def test_parenthesis_join():
    sql = """
SELECT field
FROM table JOIN (other_table) USING (field)
"""
    expected = """
SELECT field
FROM table
JOIN (
 other_table
)
USING (field)
"""
    assert format_sql(sql) == expected.strip()


def test_join_on_clause():
    sql = """
SELECT field
FROM table JOIN (other_table) ON f1 = f2
"""
    expected = """
SELECT field
FROM table
JOIN (
 other_table
)
ON f1 = f2
"""
    assert format_sql(sql) == expected.strip()


def test_join_long_on_clause():
    sql = """
SELECT field
FROM table JOIN (other_table) ON the__first__very__long__field__name__to__join = the__second__very__long__field__name__to__join and f1 = f2
"""  # noqa
    expected = """
SELECT field
FROM table
JOIN (
 other_table
)
ON
 the__first__very__long__field__name__to__join = the__second__very__long__field__name__to__join
 AND f1 = f2
"""  # noqa
    assert format_sql(sql) == expected.strip()


def test_join_long_on_clause_with_parenthesis():
    sql = """
SELECT field
FROM table JOIN (other_table) ON (the__first__very__long__field__name__to__join = the__second__very__long__field__name__to__join and (f1 = f2))
"""  # noqa
    expected = """
SELECT field
FROM table
JOIN (
 other_table
)
ON (
 the__first__very__long__field__name__to__join = the__second__very__long__field__name__to__join
 AND (f1 = f2)
)
"""  # noqa
    assert format_sql(sql) == expected.strip()


def test_join_on_clause_boolean():
    sql = """
SELECT field
FROM table JOIN (other_table) ON f1 = f2 and f3=f4
"""
    expected = """
SELECT field
FROM table
JOIN (
 other_table
)
ON f1 = f2 AND f3 = f4
"""
    assert format_sql(sql) == expected.strip()


def test_two_parenthesis_joins_with_group_by():
    sql = """
SELECT avg(col), count(*)
FROM table JOIN (other_table) USING (field) FULL OUTER JOIN ( SELECT * FROM last_table WHERE x = 1 ) USING (f2)
GROUP BY field
"""  # noqa
    expected = """
SELECT
 AVG(col),
 COUNT(*)
FROM table
JOIN (
 other_table
)
USING (field)
FULL OUTER JOIN (
 SELECT *
 FROM last_table
 WHERE x = 1
)
USING (f2)
GROUP BY field
"""
    assert format_sql(sql) == expected.strip()


def test_nested_joins():
    sql = """
SELECT COALESCE(sq_1.col, sq_2.col) f0_

FROM (SELECT ANY_VALUE(col) col,
LAST_VALUE(ANY_VALUE(col2)) OVER (PARTITION BY ANY_VALUE(col) ORDER BY SUM(clicks) ASC, SUM(metric) ASC RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) last,
hash
FROM (SELECT *
FROM `events`
WHERE _TABLE_SUFFIX BETWEEN '20200410' AND '20200510')
JOIN
(SELECT * EXCEPT (hash)
FROM (SELECT *,
ROW_NUMBER() OVER (PARTITION BY hash) AS rn
FROM `test-table`
WHERE _TABLE_SUFFIX BETWEEN '20200401' AND '20200501')
WHERE rn = 1)
USING (hash)
GROUP BY hash) sq_1

FULL OUTER JOIN

(SELECT ANY_VALUE(col) col,
hash
FROM (SELECT *
FROM `events`
WHERE _TABLE_SUFFIX BETWEEN '20200310' AND '20200410')
JOIN
(SELECT * EXCEPT (hash),
FROM (SELECT *,
ROW_NUMBER() OVER (PARTITION BY hash) AS rn
FROM `test-table`
WHERE _TABLE_SUFFIX BETWEEN '20200301' AND '20200401')
WHERE rn = 1)
USING (hash)
GROUP BY hash) sq_2

ON sq_1.hash = sq_2.hash
WHERE sq_1.last = 1
GROUP BY f0_
"""  # noqa
    expected = """
SELECT COALESCE(sq_1.col, sq_2.col) f0_
FROM (
 SELECT
  ANY_VALUE(col) col,
  LAST_VALUE(ANY_VALUE(col2)) OVER (
   PARTITION BY ANY_VALUE(col)
   ORDER BY
    SUM(clicks) ASC,
    SUM(metric) ASC
   RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) last,
  hash
 FROM (
  SELECT *
  FROM `events`
  WHERE _TABLE_SUFFIX BETWEEN '20200410' AND '20200510'
 )
 JOIN (
  SELECT * EXCEPT (hash)
  FROM (
   SELECT
    *,
    ROW_NUMBER() OVER (
     PARTITION BY hash
    ) AS rn
   FROM `test-table`
   WHERE _TABLE_SUFFIX BETWEEN '20200401' AND '20200501'
  )
  WHERE rn = 1
 )
 USING (hash)
 GROUP BY hash
) sq_1
FULL OUTER JOIN (
 SELECT
  ANY_VALUE(col) col,
  hash
 FROM (
  SELECT *
  FROM `events`
  WHERE _TABLE_SUFFIX BETWEEN '20200310' AND '20200410'
 )
 JOIN (
  SELECT * EXCEPT (hash)
  FROM (
   SELECT
    *,
    ROW_NUMBER() OVER (
     PARTITION BY hash
    ) AS rn
   FROM `test-table`
   WHERE _TABLE_SUFFIX BETWEEN '20200301' AND '20200401'
  )
  WHERE rn = 1
 )
 USING (hash)
 GROUP BY hash
) sq_2
ON sq_1.hash = sq_2.hash
WHERE sq_1.last = 1
GROUP BY f0_
"""
    assert format_sql(sql) == expected.strip()


def test_parenthesis_join_subquery():
    sql = """
SELECT field
FROM table JOIN (SELECT * from other_table WHERE date > "2020-01-01") USING (field)
"""
    expected = """
SELECT field
FROM table
JOIN (
 SELECT *
 FROM other_table
 WHERE date > "2020-01-01"
)
USING (field)
"""
    assert format_sql(sql) == expected.strip()


def test_partitioning_function():
    sql = "SELECT *, row_number() over (partition by x) from t;"
    expected = """
SELECT
 *,
 ROW_NUMBER() OVER (
  PARTITION BY x
 )
FROM t;
    """
    assert format_sql(sql) == expected.strip()


def test_partitioning_function_multiple_params():
    sql = "SELECT row_number() over (partition by x,z, x+z) from t;"
    expected = """
SELECT ROW_NUMBER() OVER (
 PARTITION BY
  x,
  z,
  x + z
)
FROM t;
    """
    assert format_sql(sql) == expected.strip()


def test_partitioning_function_multiple_params_with_frame():
    sql = "SELECT row_number() over (partition by x,z, x+z rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) from t;"  # noqa
    expected = """
SELECT ROW_NUMBER() OVER (
 PARTITION BY
  x,
  z,
  x + z
 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
FROM t;
    """
    assert format_sql(sql) == expected.strip()


def test_partitioning_function_order_by():
    sql = "SELECT *, row_number() over (partition by x order BY x) from t;"
    expected = """
SELECT
 *,
 ROW_NUMBER() OVER (
  PARTITION BY x
  ORDER BY x
 )
FROM t;
    """
    assert format_sql(sql) == expected.strip()


def test_partitioning_function_order_by_frame():
    sql = "SELECT *, row_number() over (partition by x order BY x rows BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) from t;"  # noqa
    expected = """
SELECT
 *,
 ROW_NUMBER() OVER (
  PARTITION BY x
  ORDER BY x
  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
 )
FROM t;
    """
    assert format_sql(sql) == expected.strip()


def test_partitioning_function_order_by_multiple():
    sql = "SELECT row_number() over (partition by x,z, x+z order by x desc, z ASC)  from t;"  # NOQA
    expected = """
SELECT ROW_NUMBER() OVER (
 PARTITION BY
  x,
  z,
  x + z
 ORDER BY
  x DESC,
  z ASC
)
FROM t;
    """
    assert format_sql(sql) == expected.strip()


def test_partitioning_function_order_by_no_partition():
    sql = "SELECT row_number() over (order by x desc, z ASC)  from t;"
    expected = """
SELECT ROW_NUMBER() OVER (
 ORDER BY
  x DESC,
  z ASC
)
FROM t;
    """
    assert format_sql(sql) == expected.strip()


def test_partitioning_function_order_by_no_partition_with_frame():
    sql = "SELECT row_number() over (order by x desc, z ASC RANGE between UNBOUNDED preceding AND unbounded FOLLOWING)  from t;"  # noqa
    expected = """
SELECT ROW_NUMBER() OVER (
 ORDER BY
  x DESC,
  z ASC
 RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
FROM t;
    """
    assert format_sql(sql) == expected.strip()


def test_partitioning_function_no_order_with_frame():
    sql = "SELECT row_number() over (RANGE between UNBOUNDED preceding AND unbounded FOLLOWING)  from t;"  # noqa
    expected = """
SELECT ROW_NUMBER() OVER (RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
FROM t;
    """
    assert format_sql(sql) == expected.strip()


def test_partitioning_function_equals_with_alias():
    sql = "SELECT row_number() over (RANGE between UNBOUNDED preceding AND unbounded FOLLOWING) = 1 test from t;"  # noqa
    expected = """
SELECT ROW_NUMBER() OVER (RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) = 1 test
FROM t;
    """  # noqa
    assert format_sql(sql) == expected.strip()


def test_partitioning_function_empty():
    sql = "SELECT row_number() over () from t;"
    expected = """
SELECT ROW_NUMBER() OVER ()
FROM t;
    """
    assert format_sql(sql) == expected.strip()


def test_long_function():
    sql = "select (IFNULL(SUM(f1), 0) + (APPROX_COUNT_DISTINCT(IF(f2 >= DATE('2018-04-10'), f3, NULL)) - IFNULL(SUM(f4), 0)) + 50) f_1 from t;"  # NOQA
    expected = """
SELECT (IFNULL(SUM(f1), 0) + (APPROX_COUNT_DISTINCT(IF(f2 >= DATE('2018-04-10'), f3, NULL)) - IFNULL(SUM(f4), 0)) + 50) f_1
FROM t;
"""  # NOQA
    assert format_sql(sql) == expected.strip()


def test_date_functions_field():
    sql = "select DATE(TIMESTAMP_TRUNC(CAST(sq_2.date AS TIMESTAMP), MONTH)) from table as sq_2"  # NOQA
    expected = """
SELECT DATE(TIMESTAMP_TRUNC(CAST(sq_2.date AS TIMESTAMP), MONTH))
FROM table AS sq_2
"""  # NOQA
    assert format_sql(sql) == expected.strip()


def test_case_expr():
    sql = (
        "select case c when 1 THEN 'test' when 1+3 then 'other' else 'none' end from t;"
    )
    expected = """
SELECT CASE c
 WHEN 1 THEN 'test'
 WHEN 1 + 3 THEN 'other'
 ELSE 'none'
END
FROM t;
"""  # NOQA
    assert format_sql(sql) == expected.strip()


def test_case_expr_multiple_fields():
    sql = "select col, col2, case c when 1 THEN 'test' when 1+3 then 'other' else 'none' end from t;"  # noqa
    expected = """
SELECT
 col,
 col2,
 CASE c
  WHEN 1 THEN 'test'
  WHEN 1 + 3 THEN 'other'
  ELSE 'none'
 END
FROM t;
"""  # NOQA
    assert format_sql(sql) == expected.strip()


def test_case():
    sql = "select case when c = 1 THEN 'test' when c <= 1+3 then 'other' else 'none' end from t;"  # noqa
    expected = """
SELECT CASE
 WHEN c = 1 THEN 'test'
 WHEN c <= 1 + 3 THEN 'other'
 ELSE 'none'
END
FROM t;
"""  # NOQA
    assert format_sql(sql) == expected.strip()


def test_case_multiple_fields():
    sql = "select col, case when c = 1 THEN 'test' when c <= 1+3 then 'other' else 'none' end from t;"  # noqa
    expected = """
SELECT
 col,
 CASE
  WHEN c = 1 THEN 'test'
  WHEN c <= 1 + 3 THEN 'other'
  ELSE 'none'
 END
FROM t;
"""  # NOQA
    assert format_sql(sql) == expected.strip()


def test_case_no_else():
    sql = "select case when c = 1 THEN 'test' when c <= 1+3 then 'other' end from t;"
    expected = """
SELECT CASE
 WHEN c = 1 THEN 'test'
 WHEN c <= 1 + 3 THEN 'other'
END
FROM t;
"""  # NOQA
    assert format_sql(sql) == expected.strip()


def test_index_access():
    sql = "select col[0] f0, col[safe_index(-1)] f1 from table;"
    expected = """
SELECT
 col[0] f0,
 col[SAFE_INDEX(-1)] f1
FROM table;
"""  # NOQA
    assert format_sql(sql) == expected.strip()


def test_array_with_subquery():
    sql = "select ARRAY(SELECT struct(dimension, IFNULL(sum(metric),0) ) FROM unnest(f_2) group BY dimension ORDER by dimension) from table"  # noqa
    expected = """
SELECT ARRAY(
 SELECT STRUCT(dimension, IFNULL(SUM(metric), 0))
 FROM UNNEST(f_2)
 GROUP BY dimension
 ORDER BY dimension
)
FROM table
"""  # NOQA
    assert format_sql(sql) == expected.strip()


def test_array_with_subquery_multiple_args():
    sql = "select ARRAY(SELECT struct(dimension, IFNULL(sum(metric),0) ) FROM unnest(f_2) group BY dimension ORDER by dimension), col from table"  # noqa
    expected = """
SELECT
 ARRAY(
  SELECT STRUCT(dimension, IFNULL(SUM(metric), 0))
  FROM UNNEST(f_2)
  GROUP BY dimension
  ORDER BY dimension
 ),
 col
FROM table
"""  # NOQA
    assert format_sql(sql) == expected.strip()


def test_unnest_with_offset():
    sql = "SELECT ARRAY( SELECT col from UNNEST(f_2) with offset ) FROM table;"
    expected = """
SELECT ARRAY(
 SELECT col
 FROM UNNEST(f_2) WITH OFFSET
)
FROM table;
"""
    assert format_sql(sql) == expected.strip()


def test_unnest_with_offset_alias():
    sql = "SELECT ARRAY( SELECT a.col from UNNEST(f_2) as a with offset ) FROM table;"
    expected = """
SELECT ARRAY(
 SELECT a.col
 FROM UNNEST(f_2) AS a WITH OFFSET
)
FROM table;
"""
    assert format_sql(sql) == expected.strip()


def test_unnest_with_offset_both_aliased():
    sql = """
SELECT some_field f0,
(SELECT SUM(IF(hh = structure.cq[SAFE_OFFSET(o)], 1, 0))
FROM UNNEST(other_struct.cq) hh WITH offset o) * 100
/ LEAST(other_struct.len, structure.len) f1 from table;"""
    expected = """
SELECT
 some_field f0,
 (
  SELECT SUM(IF(hh = structure.cq[SAFE_OFFSET(o)], 1, 0))
  FROM UNNEST(other_struct.cq) hh WITH OFFSET o
 ) * 100 / LEAST(other_struct.len, structure.len) f1
FROM table;
"""
    assert format_sql(sql) == expected.strip()


def test_function_calls():
    sql = "select SAFE_DIVIDE(SUM(SUM(met)) OVER (PARTITION BY ANY_VALUE(hash) ORDER BY SUM(met) DESC, ANY_VALUE(hash2) ASC) ,SUM(SUM(met)) OVER (PARTITION BY ANY_VALUE(hash))) from t group by hash3"  # noqa
    expected = """
SELECT SAFE_DIVIDE(
 SUM(SUM(met)) OVER (
  PARTITION BY ANY_VALUE(hash)
  ORDER BY
   SUM(met) DESC,
   ANY_VALUE(hash2) ASC
 ),
 SUM(SUM(met)) OVER (
  PARTITION BY ANY_VALUE(hash)
 )
)
FROM t
GROUP BY hash3
"""  # NOQA
    assert format_sql(sql) == expected.strip()


def test_regex():
    sql = "select regexp_replace(field, r'[^a-zA-Z0-9]', '') from t;"
    expected = """
SELECT REGEXP_REPLACE(field, r'[^a-zA-Z0-9]', '')
FROM t;
"""
    assert format_sql(sql) == expected.strip()


def test_multiple_regexes():
    sql = r"select REGEXP_REPLACE(regexp_replace(NORMALIZE_AND_CASEFOLD ( arr [SAFE_OFFSET(0)],NFD), r'\p{{Mn}}', ''), r'[^a-zA-Z0-9]', ' ') from t;"  # noqa
    expected = r"""
SELECT REGEXP_REPLACE(
 REGEXP_REPLACE(NORMALIZE_AND_CASEFOLD(arr[SAFE_OFFSET(0)], NFD), r'\p{{Mn}}', ''),
 r'[^a-zA-Z0-9]',
 ' '
)
FROM t;
"""  # NOQA
    assert format_sql(sql) == expected.strip()


def test_parentheses_nested_select():
    sql = """select (SELECT SUM(IF(hh = b.some_field.cq[SAFE_OFFSET(o)],1,0))
FROM UNNEST(a.other_field.cq) hh OFFSET o) * 100 / LEAST(a.other_field.len, b.some_field.len) result_field
from t1 a
join t2 b USING (f1)
"""  # NOQA
    expected = """
SELECT (
 SELECT SUM(IF(hh = b.some_field.cq[SAFE_OFFSET(o)], 1, 0))
 FROM UNNEST(a.other_field.cq) hh
 OFFSET o
) * 100 / LEAST(a.other_field.len, b.some_field.len) result_field
FROM t1 a
JOIN t2 b
USING (f1)
"""
    assert format_sql(sql) == expected.strip()


def test_union():
    sql = "select f1 from t1 union t2;"
    expected = """
SELECT f1
FROM t1
UNION t2;
"""
    assert format_sql(sql) == expected.strip()


def test_intersect():
    sql = "select f1 from t1 intersect   t2;"
    expected = """
SELECT f1
FROM t1
INTERSECT t2;
"""
    assert format_sql(sql) == expected.strip()


def test_except():
    sql = "select f1 from t1 except select * from `t2`;"
    expected = """
SELECT f1
FROM t1
EXCEPT
SELECT *
FROM `t2`;
"""
    assert format_sql(sql) == expected.strip()


def test_query_combinations():
    sql = """SELECT A FROM TA
INTERSECT SELECT B FROM TB EXCEPT (SELECT C FROM TB)
UNION SELECT D FROM TD"""
    expected = """
SELECT A
FROM TA
INTERSECT
SELECT B
FROM TB
EXCEPT
(
 SELECT C
 FROM TB
)
UNION
SELECT D
FROM TD
"""
    assert format_sql(sql) == expected.strip()


def test_long_function_calls():
    sql = """select STRUCT(LENGTH(a_very_very_very_long_field_name_that_takes_quite_some_space) AS len, TO_CODE_POINTS(some_other_very_very_long_field_name) AS cq) a_very_very_long_result_field
from t;
"""  # NOQA
    expected = """
SELECT STRUCT(
 LENGTH(a_very_very_very_long_field_name_that_takes_quite_some_space) AS len,
 TO_CODE_POINTS(some_other_very_very_long_field_name) AS cq
) a_very_very_long_result_field
FROM t;
"""
    assert format_sql(sql) == expected.strip()


def test_long_function_calls_multiple_fields():
    sql = """select f1, STRUCT(LENGTH(a_very_very_very_long_field_name_that_takes_quite_some_space) AS len, TO_CODE_POINTS(some_other_very_very_long_field_name) AS cq) a_very_very_long_result_field
from t;
"""  # NOQA
    expected = """
SELECT
 f1,
 STRUCT(
  LENGTH(a_very_very_very_long_field_name_that_takes_quite_some_space) AS len,
  TO_CODE_POINTS(some_other_very_very_long_field_name) AS cq
 ) a_very_very_long_result_field
FROM t;
"""
    assert format_sql(sql) == expected.strip()


def test_capitalized_column_name():
    sql = "select COL_name from t;"
    expected = """
SELECT COL_name
FROM t;
"""
    assert format_sql(sql) == expected.strip()


def test_capitalized_alias():
    sql = "select col an_ALIAS from t;"
    expected = """
SELECT col an_ALIAS
FROM t;
"""
    assert format_sql(sql) == expected.strip()


def test_break_long_where():
    sql = "select * from t where this > 0 AND that < 0 AND foo = 4 AND veryveryverylonglonglongname = 'test' OR other_long_long_long_name < 10"  # noqa
    expected = """
SELECT *
FROM t
WHERE
 this > 0
 AND that < 0
 AND foo = 4
 AND veryveryverylonglonglongname = 'test'
 OR other_long_long_long_name < 10
"""
    assert format_sql(sql) == expected.strip()


def test_break_long_where_nested_operations():
    sql = "select * from t where this > 0 AND that < 0 AND foo = 4 AND (veryveryveryveryveryveryverylonglonglongname = 'test' OR other_long_long_long_long_name < 10)"  # noqa
    expected = """
SELECT *
FROM t
WHERE
 this > 0
 AND that < 0
 AND foo = 4
 AND (
  veryveryveryveryveryveryverylonglonglongname = 'test'
  OR other_long_long_long_long_name < 10
 )
"""
    assert format_sql(sql) == expected.strip()


def test_break_long_parenthesis_where_nested_operations():
    sql = "select * from t where (this > 0 AND that < 0 AND foo = 4 AND (veryveryveryveryveryveryverylonglonglongname = 'test' OR other_long_long_long_long_name < 10) OR x < 0)"  # noqa
    expected = """
SELECT *
FROM t
WHERE (
 this > 0
 AND that < 0
 AND foo = 4
 AND (
  veryveryveryveryveryveryverylonglonglongname = 'test'
  OR other_long_long_long_long_name < 10
 )
 OR x < 0
)
"""
    assert format_sql(sql) == expected.strip()


def test_cast_type():
    sql = "select cast(date as date) from t;"
    expected = """
SELECT CAST(date AS DATE)
FROM t;
"""
    assert format_sql(sql) == expected.strip()


def test_cast_in_condition():
    sql = (
        "select * from t where CAST(Date AS DaTe) between '2020-01-01' AND '2020-02-01'"
    )
    expected = """
SELECT *
FROM t
WHERE CAST(Date AS DATE) BETWEEN '2020-01-01' AND '2020-02-01'
"""
    assert format_sql(sql) == expected.strip()


def test_date_function():
    sql = "select date(date) from t"
    expected = """
SELECT DATE(date)
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_select_boolean_condition_expression():
    sql = "select field is not null and col > 0, x from t;"
    expected = """
SELECT
 field IS NOT NULL AND col > 0,
 x
FROM t;
"""
    assert format_sql(sql) == expected.strip()


def test_bitwise_operation():
    sql = "select field & 64 as col from t;"
    expected = """
SELECT field & 64 AS col
FROM t;
"""
    assert format_sql(sql) == expected.strip()


def test_cross_join():
    sql = "select f1, f2 from t1 cross join t2;"
    expected = """
SELECT
 f1,
 f2
FROM t1
CROSS JOIN t2;
"""
    assert format_sql(sql) == expected.strip()


def test_implicit_cross_join():
    sql = "select f1,f2 from t1, t2;"
    expected = """
SELECT
 f1,
 f2
FROM t1, t2;
"""
    assert format_sql(sql) == expected.strip()


def test_implicit_cross_join_unnest():
    sql = "select field from t1, unnest(t2);"
    expected = """
SELECT field
FROM t1, UNNEST(t2);
"""
    assert format_sql(sql) == expected.strip()


def test_multiple_joins_unnest():
    sql = "select field from t1 a, unnest(t2) as b, unnest(t3) as c;"
    expected = """
SELECT field
FROM t1 a, UNNEST(t2) AS b, UNNEST(t3) AS c;
"""
    assert format_sql(sql) == expected.strip()


def test_nested_multiple_joins_unnest():
    sql = (
        "select field from (select x from (select * from t1) a, unnest(t2) as b,"
        "unnest(t3) as c);"
    )
    expected = """
SELECT field
FROM (
 SELECT x
 FROM (
  SELECT *
  FROM t1
 ) a, UNNEST(t2) AS b, UNNEST(t3) AS c
);
"""
    assert format_sql(sql) == expected.strip()


def test_having_boolean_clause():
    sql = (
        "select dim from t group by dim having sum(field) is not null and avg(col) > 0"
    )
    expected = """
SELECT dim
FROM t
GROUP BY dim
HAVING SUM(field) IS NOT NULL AND AVG(col) > 0
"""
    assert format_sql(sql) == expected.strip()


def test_if_with_date_column_name():
    sql = "select if(date(date) = '2020-01-01', 1, 0) from t"
    expected = """
SELECT IF(DATE(date) = '2020-01-01', 1, 0)
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_long_nested_where():
    sql = """
select * from (
select f from table
  WHERE EXISTS( SELECT 1 FROM UNNEST(long__field__name__multiple__array) AS a WHERE a LIKE '%Travel%' )
   AND STARTS_WITH(the_second_keyword, 'travel')
   AND ( ENDS_WITH(the_first_keyword, 'paris') OR EXISTS( SELECT 1 FROM UNNEST(long__field__name__multiple__array) AS a WHERE a LIKE '%Travel in Paris%' ) )
)
"""  # noqa
    expected = """
SELECT *
FROM (
 SELECT f
 FROM table
 WHERE
  EXISTS(
   SELECT 1
   FROM UNNEST(long__field__name__multiple__array) AS a
   WHERE a LIKE '%Travel%'
  )
  AND STARTS_WITH(the_second_keyword, 'travel')
  AND (
   ENDS_WITH(the_first_keyword, 'paris')
   OR EXISTS(
    SELECT 1
    FROM UNNEST(long__field__name__multiple__array) AS a
    WHERE a LIKE '%Travel in Paris%'
   )
  )
)
"""
    assert format_sql(sql) == expected.strip()


def test_long_case_when_conditions_line_breaks():
    sql = """
select case when(the__very__long__integer__variable_that__is__tested >= 0 AND the__very__long__integer__variable_that__is__tested < 1000) THEN '0000_from_0_to_1000'
   WHEN the__very__long__integer__variable_that__is__tested >= 1000 AND the__very__long__integer__variable_that__is__tested < 10000 THEN '0001_from_1000_to_10000'
   WHEN the__very__long__integer__variable_that__is__tested >= 10000
THEN '0002_from_10000_to_' end
from t;
"""  # noqa
    expected = """
SELECT CASE
 WHEN (
  the__very__long__integer__variable_that__is__tested >= 0
  AND the__very__long__integer__variable_that__is__tested < 1000
 )
 THEN '0000_from_0_to_1000'
 WHEN
  the__very__long__integer__variable_that__is__tested >= 1000
  AND the__very__long__integer__variable_that__is__tested < 10000
 THEN '0001_from_1000_to_10000'
 WHEN the__very__long__integer__variable_that__is__tested >= 10000 THEN '0002_from_10000_to_'
END
FROM t;
"""  # noqa
    assert format_sql(sql) == expected.strip()


def test_long_case_when_conditions_line_breaks_multi_column():
    sql = """
select x, case when(the__very__long__integer__variable_that__is__tested >= 0 AND the__very__long__integer__variable_that__is__tested < 1000) THEN '0000_from_0_to_1000'
   WHEN the__very__long__integer__variable_that__is__tested >= 1000 AND the__very__long__integer__variable_that__is__tested < 10000 THEN '0001_from_1000_to_10000'
   WHEN the__very__long__integer__variable_that__is__tested >= 10000
THEN '0002_from_10000_to_' end
from t;
"""  # noqa
    expected = """
SELECT
 x,
 CASE
  WHEN (
   the__very__long__integer__variable_that__is__tested >= 0
   AND the__very__long__integer__variable_that__is__tested < 1000
  )
  THEN '0000_from_0_to_1000'
  WHEN
   the__very__long__integer__variable_that__is__tested >= 1000
   AND the__very__long__integer__variable_that__is__tested < 10000
  THEN '0001_from_1000_to_10000'
  WHEN the__very__long__integer__variable_that__is__tested >= 10000 THEN '0002_from_10000_to_'
 END
FROM t;
"""  # noqa
    assert format_sql(sql) == expected.strip()


def test_where_in_subquery():
    sql = "select * from t where id in (select id from other_t where field <> 0);"
    expected = """
SELECT *
FROM t
WHERE
 id IN (
  SELECT id
  FROM other_t
  WHERE field <> 0
 );
"""
    assert format_sql(sql) == expected.strip()


def test_table_in_square_brackets():
    sql = "select * from [complex.table.name];"
    expected = """
SELECT *
FROM [complex.table.name];
"""
    assert format_sql(sql) == expected.strip()


def test_union_all_nested_query():
    sql = """select * from (
select hash, max(date)
from (
(select * from t1)
UNION ALL (select * from t2)
) group by hash
)"""
    expected = """
SELECT *
FROM (
 SELECT
  hash,
  MAX(date)
 FROM (
  (
   SELECT *
   FROM t1
  )
  UNION ALL
  (
   SELECT *
   FROM t2
  )
 )
 GROUP BY hash
)
"""
    assert format_sql(sql) == expected.strip()


def test_array():
    sql = "select [f1, 'x', f2] from t"
    expected = """
SELECT [f1, 'x', f2]
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_chained_field():
    sql = "select namespace.complex_array[offset(3)].SomeStuff[offset(3)] from t"
    expected = """
SELECT namespace.complex_array[OFFSET(3)].SomeStuff[OFFSET(3)]
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_multiple_table_name_with_cross_join():
    sql = "select * from x.y.z, a.b.c"
    expected = """
SELECT *
FROM x.y.z, a.b.c
"""
    assert format_sql(sql) == expected.strip()


def test_multiple_table_name_with_multiple_joins():
    sql = "select * from x.y.z, a.b.c join i.j using (k) left join t on p=l;"
    expected = """
SELECT *
FROM x.y.z, a.b.c
JOIN i.j
USING (k)
LEFT JOIN t
ON p = l;
"""
    assert format_sql(sql) == expected.strip()


def test_where_with_offset_column():
    sql = "select sum(x) from UNNEST(c) AS x WITH OFFSET where offset between 1 and 2 offset 5;"  # noqa
    expected = """
SELECT SUM(x)
FROM UNNEST(c) AS x WITH OFFSET
WHERE offset BETWEEN 1 AND 2
OFFSET 5;
"""
    assert format_sql(sql) == expected.strip()


def test_struct():
    sql = "select struct(f1, f2 as x) from t"
    expected = """
SELECT STRUCT(f1, f2 AS x)
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_array_agg():
    sql = "SELECT ARRAY_AGG(a) agg from t"
    expected = """
SELECT ARRAY_AGG(a) agg
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_array_agg_order_by():
    sql = "SELECT ARRAY_AGG(a ORDER BY o) agg from t"
    expected = """
SELECT ARRAY_AGG(a ORDER BY o) agg
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_distinct_array_agg_order_by():
    sql = "SELECT ARRAY_AGG(distinct a ignore nulls order by o ASC, b desc limit 4) agg from t"  # noqa
    expected = """
SELECT ARRAY_AGG(DISTINCT a IGNORE NULLS ORDER BY o ASC, b DESC LIMIT 4) agg
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_where_boolean_followed_by_group():
    sql = """
SELECT *
FROM t
WHERE col1 = col0 and col2 = col0 and col3 = col0
GROUP BY field, col0
"""
    expected = """
SELECT *
FROM t
WHERE col1 = col0 AND col2 = col0 AND col3 = col0
GROUP BY
 field,
 col0
"""
    assert format_sql(sql) == expected.strip()


def test_date_column_in_function_call():
    sql = "select if(date >= date('2018-04-10'), col, null) from t"
    expected = """
SELECT IF(date >= DATE('2018-04-10'), col, NULL)
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_floating_point_number():
    sql = "select f * 0.0009 from t"
    expected = """
SELECT f * 0.0009
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_negative_floating_point_number():
    sql = "select f-0.0009, -8.9 from t"
    expected = """
SELECT
 f - 0.0009,
 -8.9
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_where_not_in_subquery():
    sql = """select field
FROM t WHERE id NOT IN (SELECT id
FROM other_table
WHERE col <> 0)"""
    expected = """
SELECT field
FROM t
WHERE
 id NOT IN (
  SELECT id
  FROM other_table
  WHERE col <> 0
 )
"""
    assert format_sql(sql) == expected.strip()


def test_contains_predicate():
    sql = "select field from t where x contains 'foo';"
    expected = """
SELECT field
FROM t
WHERE x CONTAINS 'foo';
"""
    assert format_sql(sql) == expected.strip()


def test_bitwise_shifting():
    sql = "select c1<<32 from t"
    expected = """
SELECT c1 << 32
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_quoted_table_name():
    sql = 'SELECT col FROM "schema"."table"'
    expected = """
SELECT col
FROM "schema"."table"
"""
    assert format_sql(sql) == expected.strip()


def test_long_quoted_table_name():
    sql = 'SELECT col FROM "project"."dataset"."table"'
    expected = """
SELECT col
FROM "project"."dataset"."table"
"""
    assert format_sql(sql) == expected.strip()


def test_extract_date():
    sql = "select extract(date from some_date)"
    expected = """
SELECT EXTRACT(DATE FROM some_date)
"""
    assert format_sql(sql) == expected.strip()


def test_count_distinct():
    sql = "SELECT count(distinct id) agg from t"
    expected = """
SELECT COUNT(DISTINCT id) agg
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_count_distinct_with_function():
    sql = "SELECT count(distinct IF(code = 200, url, NULL)) agg from t"
    expected = """
SELECT COUNT(DISTINCT IF(code = 200, url, NULL)) agg
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_count_equal_countif():
    sql = "select count(1) = countif(date >= date('1994-04-11')) num_recent from t"
    expected = """
SELECT COUNT(1) = COUNTIF(date >= DATE('1994-04-11')) num_recent
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_invalid_join_missing_using_or_on():
    sql = "SELECT field FROM table JOIN other_table"
    expected = """
SELECT field
FROM table
JOIN other_table
"""
    assert format_sql(sql) == expected.strip()


def test_string_alias():
    sql = "select x `alias`, y \"alias\", z 'alias', 'col' AS 'alias' from t"
    expected = """
SELECT
 x `alias`,
 y "alias",
 z 'alias',
 'col' AS 'alias'
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_index_chained_column():
    sql = """select field.`col`[SAFE_OFFSET(2)] from t where
    field.`col`[SAFE_OFFSET(2)] IS NOT NULL;
    """
    expected = """
SELECT field.`col`[SAFE_OFFSET(2)]
FROM t
WHERE field.`col`[SAFE_OFFSET(2)] IS NOT NULL;
"""
    assert format_sql(sql) == expected.strip()


def test_group_each_by():
    sql = "select f, sum(s) from t group each by f;"
    expected = """
SELECT
 f,
 SUM(s)
FROM t
GROUP EACH BY f;
"""
    assert format_sql(sql) == expected.strip()


def test_plain_join_each():
    sql = """
SELECT field
FROM table JOIN EACH (select * from other_table) USING (field)
"""
    expected = """
SELECT field
FROM table
JOIN EACH (
 SELECT *
 FROM other_table
)
USING (field)
"""
    assert format_sql(sql) == expected.strip()


def test_escaped_char():
    sql = """
select id from users WHERE name = 'O\\'Connor'
"""
    expected = """
SELECT id
FROM users
WHERE name = 'O\\'Connor'
"""
    assert format_sql(sql) == expected.strip()


def test_filter_where():
    sql = "select count(1) filter (where active = true) from users"
    expected = """
SELECT COUNT(1) FILTER (WHERE active = TRUE)
FROM users
"""
    assert format_sql(sql) == expected.strip()


def test_filter_where_alias():
    sql = "select id, count(1) filter (where active = true) c from users group by id"
    expected = """
SELECT
 id,
 COUNT(1) FILTER (WHERE active = TRUE) c
FROM users
GROUP BY id
"""
    assert format_sql(sql) == expected.strip()


def test_filter_where_alias_as():
    sql = (
        "select id c0, count(1) filter (where active = true and ok) as c1,"
        "count(1) filter (WHERE 1 =1 or 2=1) as c2, name from users group by id, name"
    )
    expected = """
SELECT
 id c0,
 COUNT(1) FILTER (WHERE active = TRUE AND ok) AS c1,
 COUNT(1) FILTER (WHERE 1 = 1 OR 2 = 1) AS c2,
 name
FROM users
GROUP BY
 id,
 name
"""
    assert format_sql(sql) == expected.strip()


def test_with_statement():
    sql = """
with tmp_t as (select id, sum(n) from t group by id)
select id, count(*) from myt
join tmp_t using (id)
group by id"""
    expected = """
WITH tmp_t AS (
 SELECT
  id,
  SUM(n)
 FROM t
 GROUP BY id
)
SELECT
 id,
 COUNT(*)
FROM myt
JOIN tmp_t
USING (id)
GROUP BY id
"""
    assert format_sql(sql) == expected.strip()


def test_multiple_with_statements():
    sql = """
    WITH regional_sales AS (
        SELECT region, SUM(amount) AS total_sales
        FROM orders GROUP BY region
     ), top_regions AS (
        SELECT region FROM regional_sales
        WHERE total_sales > (SELECT SUM(total_sales)/10 FROM regional_sales)
     )
SELECT region, product,
       SUM(quantity) AS product_units,
       SUM(amount) AS product_sales
FROM orders WHERE region IN (SELECT region FROM top_regions)
GROUP BY region, product;"""
    expected = """
WITH regional_sales AS (
 SELECT
  region,
  SUM(amount) AS total_sales
 FROM orders
 GROUP BY region
),
top_regions AS (
 SELECT region
 FROM regional_sales
 WHERE
  total_sales > (
   SELECT SUM(total_sales) / 10
   FROM regional_sales
  )
)
SELECT
 region,
 product,
 SUM(quantity) AS product_units,
 SUM(amount) AS product_sales
FROM orders
WHERE
 region IN (
  SELECT region
  FROM top_regions
 )
GROUP BY
 region,
 product;
"""
    assert format_sql(sql) == expected.strip()


def test_nested_with_statement():
    sql = """
select * from
( with t as ( select 1 foo ) select * from t )
"""
    expected = """
SELECT *
FROM (
 WITH t AS (
  SELECT 1 foo
 )
 SELECT *
 FROM t
)
"""
    assert format_sql(sql) == expected.strip()


def test_function_with_index_access():
    sql = "select split(col, ':')[safe_offset(0)] from t"
    expected = """
SELECT SPLIT(col, ':')[SAFE_OFFSET(0)]
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_multiple_index_accesses():
    sql = "select array_concat_agg(col)[0][0] from t"
    expected = """
SELECT ARRAY_CONCAT_AGG(col)[0][0]
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_string_containing_quote():
    sql = 'select col = "Test\'" from t'
    expected = """
SELECT col = "Test\'"
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_select_star_replace():
    sql = 'select * replace ("x" as col) from t'
    expected = """
SELECT * REPLACE ("x" AS col)
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_select_star_multiple_replace():
    sql = 'select * replace ("x" as col, "y" as f) from t'
    expected = """
SELECT * REPLACE (
 "x" AS col,
 "y" AS f
)
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_select_star_replace_nospace():
    sql = 'select * replace("x" as col) from t'
    expected = """
SELECT * REPLACE ("x" AS col)
FROM t
"""
    assert format_sql(sql) == expected.strip()


def test_nesting_case_expr():
    sql = """SELECT CASE
    WHEN CASE
    WHEN code = 1 THEN 'VALID'
    WHEN code = 2 THEN 'INVALID' END
   = 'VALID' THEN 'OK' ELSE 'KO' END
FROM table
"""
    expected = """
SELECT CASE
 WHEN
  CASE
   WHEN code = 1 THEN 'VALID'
   WHEN code = 2 THEN 'INVALID'
  END = 'VALID'
 THEN 'OK'
 ELSE 'KO'
END
FROM table
"""
    assert format_sql(sql) == expected.strip()


def test_interval_with_single_datetime_part():
    sql = """select value
    from table
    where date(date) >= date_sub(current_date(), interval -5 hour)"""
    expected = """
SELECT value
FROM table
WHERE DATE(date) >= DATE_SUB(CURRENT_DATE(), INTERVAL -5 HOUR)
"""
    assert format_sql(sql) == expected.strip()


def test_interval_with_datetime_part_range():
    sql = """select value
    from table
    where date(date) >= date_sub(current_date(), interval '8 20 17' month to hour)"""
    expected = """
SELECT value
FROM table
WHERE DATE(date) >= DATE_SUB(CURRENT_DATE(), INTERVAL '8 20 17' MONTH TO HOUR)
"""
    assert format_sql(sql) == expected.strip()

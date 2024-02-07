import connection


def display_users_with_no_posts_and_no_comments_first_version(cursor):
    """Написать запрос для вывода пользователей, которые не создали ни одного поста и не оставили ни одного коммента
     (несколько вариантов запроса)"""

    query = ('SELECT "Display_name" FROM "Users" u '
             'WHERE ('
             '  SELECT COUNT(*)'
             '  FROM posts p'
             '  WHERE p."OwnerUserId" = u."Id"'
             ') = 0'
             'AND ('
             '  SELECT COUNT(*)'
             '  FROM "Comments" c'
             '  WHERE c."UserId" = u."Id"'
             ') = 0')

    cursor.execute(query)
    ans = cursor.fetchall()
    return ans


def display_users_with_no_posts_and_no_comments_second_version(cursor):
    """Написать запрос для вывода пользователей, которые не создали ни одного поста и не оставили ни одного коммента
     (несколько вариантов запроса)"""

    query = ('SELECT "Display_name" FROM "Users" u '
             'WHERE NOT EXISTS ('
             '  SELECT 1 FROM posts p'
             '  WHERE p."OwnerUserId" = u."Id"'
             ') AND NOT EXISTS ('
             '  SELECT 1 FROM "Comments" c'
             '  WHERE c."UserId" = u."Id"'
             ')')
    cursor.execute(query)
    ans = cursor.fetchall()
    return ans


def display_posts_and_comments_for_year(cursor):
    """Написать запрос для вывода года, кол-ва постов за год и кол-во комментов за год"""

    query = ('SELECT COALESCE(EXTRACT(YEAR FROM p."CreationDate"), EXTRACT(YEAR FROM c."CreationDate")) AS "CreationYear", '
             '       COUNT(DISTINCT p."Id") AS "PostsCount", '
             '       COUNT(DISTINCT c."Id") AS "CommentsCount" '
             'FROM posts p '
             'FULL OUTER JOIN "Comments" c ON EXTRACT(YEAR FROM c."CreationDate") = EXTRACT(YEAR FROM p."CreationDate") '
             'GROUP BY "CreationYear" '
             'ORDER BY "CreationYear" DESC')
    cursor.execute(query)
    ans = cursor.fetchall()
    return ans


def display_most_active_users(cursor):
    """Вывести 3 самых активных (по кол-ву комментариев) пользователей (display name) и их кол-во комментариев"""

    query = ('SELECT u."Display_name" as username, COUNT(c."Id") AS "CommentsCount" '
             'FROM "Users" u '
             'LEFT JOIN "Comments" c ON u."Id" = c."UserId" '
             'GROUP BY username '
             'ORDER BY "CommentsCount" DESC '
             'LIMIT 3')
    cursor.execute(query)
    ans = cursor.fetchall()
    return ans


def display_most_active_users_with_percentage(cursor):
    """Расширить п.3, добавив процент кол-ва комментариев пользователя от общего кол-ва"""

    query = ('WITH UserComments AS ('
             '  SELECT u."Display_name" AS display_name, COUNT(c."Id") AS comment_count '
             '  FROM "Users" u'
             '  LEFT JOIN "Comments" c ON u."Id" = c."UserId"'
             '  GROUP BY display_name'
             ')'
             'SELECT uc.display_name, '
             '       uc.comment_count, '
             '       (uc.comment_count * 100 / total.total_comments) || \'%\' AS percentage_total '
             'FROM UserComments uc LEFT JOIN ('
             '  SELECT COUNT("Id") AS total_comments FROM "Comments"'
             ') total ON true '
             'ORDER BY uc.comment_count '
             'DESC LIMIT 3')
    cursor.execute(query)
    ans = cursor.fetchall()
    return ans


if __name__ == '__main__':
    connection_cursor = connection.connection.cursor()

    print('1.1. Пользователи, которые не создали ни одного поста и не оставили ни одного коммента:',
          display_users_with_no_posts_and_no_comments_first_version(connection_cursor), sep='\n')
    print('1.2. Пользователи, которые не создали ни одного поста и не оставили ни одного коммента:',
          display_users_with_no_posts_and_no_comments_second_version(connection_cursor), sep='\n')
    print('2. Год, кол-во постов за год и кол-во комментов за год:',
          display_posts_and_comments_for_year(connection_cursor), sep='\n')
    print('3. 3 самых активных по кол-ву комментариев пользователей и их кол-во комментариев:',
          display_most_active_users(connection_cursor), sep='\n')
    print('4. Расширенный п.3 с процентом кол-ва комментариев пользователя от общего кол-ва:',
          display_most_active_users_with_percentage(connection_cursor), sep='\n')

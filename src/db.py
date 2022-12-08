import os
import json
import psycopg2
import psycopg2.extras
import argparse


def connect_db(db_config, db_pass):
    conn = None
    try:
        conn = psycopg2.connect(
            host=db_config['db_host']
            , port=db_config['db_port']
            , dbname=db_config['db_name']
            , user=db_config['db_user']
            , password=db_pass
        )
        return conn
    except (Exception, psycopg2.Error) as error:
        print('connection error : {}'.format(error))
    finally:
        connect_db(None, conn)


def close_db(cur, conn):
    if cur:
        cur.close()
    if conn:
        conn.close()
    print('PostgreSQL connection is closed')


def execute_query(db_config, db_pass, db_query):
    conn = connect_db(db_config, db_pass)
    cur = conn.cursor()
    try:
        cur.execute(db_query)

        columns = [desc[0] for desc in cur.description]
        print('{0}'.format(columns))

        results = []
        print(db_query)
        for row in cur.fetchall():
            results.append(dict(zip(columns, row)))

        body = json.dumps(results, indent=2, default=str)
        print('{}'.format(body))

    except (Exception, psycopg2.Error) as error:
        errorData = {'error': str(error)}
        body = json.dumps(errorData, indent=2, default=str)
        print('{0}'.format('[\'error\']'))
        print('{}'.format(body))

    finally:
        close_db(cur, conn)


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        '-c', '--config', required=True, type=str, help='Config file')
    parser.add_argument(
        '-p', '--dbpass', required=True, type=str, help='DB password')
    parser.add_argument(
        '-i', '--usetemplate', required=True, type=int, help='usease template')
    parser.add_argument(
        '-t', '--template', required=False, type=str, help='SQL template file' , default= 'null')
    parser.add_argument(
        '-q', '--querystr', required=False, type=str, help='query str' , default= 'null')
    args = parser.parse_args()

    with open(args.config, mode="r", encoding="utf-8") as f:
        config = json.load(f)

    query = args.querystr
    execute_query(config, args.dbpass, query)


if __name__ == '__main__':
    main()


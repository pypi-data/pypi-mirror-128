import json
import boto3
import base64
import pymongo
import pymssql
import psycopg2
import cx_Oracle
import urllib.parse
from botocore.exceptions import ClientError


class EabrDatabases(object):
    class Oracle:
        def __init__(self, oracle_user, oracle_pwd, oracle_dsn):
            self.oracle_user = oracle_user
            self.oracle_pwd = oracle_pwd
            self.oracle_dsn = oracle_dsn

        def conn_oracle(self):
            try:
                cnxn = cx_Oracle.connect(user=self.oracle_user,
                                         password=self.oracle_pwd,
                                         dsn=self.oracle_dsn)
            except ValueError as e:
                print(e)
            return cnxn

    class Redshift:
        def __init__(self, rs_db, rs_host, rs_port,
                     rs_user, rs_pwd):
            self.rs_db = rs_db
            self.rs_host = rs_host
            self.rs_port = int(rs_port)
            self.rs_user = rs_user
            self.rs_pwd = rs_pwd

        def conn_redshift(self):
            try:
                cnxn = psycopg2.connect(dbname=self.rs_db,
                                        host=self.rs_host,
                                        port=self.rs_port,
                                        user=self.rs_user,
                                        password=self.rs_pwd)
            except ValueError as e:
                print(e)
            return cnxn

    class DocumentDB:
        def __init__(self, ddb_host, ddb_port,
                     ddb_user, ddb_pwd, ddb_ssl,
                     ddb_ssl_cert, ddb_public_key):
            self.ddb_host = ddb_host
            self.ddb_port = int(ddb_port)
            self.ddb_user = urllib.parse.quote_plus(ddb_user)
            self.ddb_pwd = urllib.parse.quote_plus(ddb_pwd)
            self.ddb_ssl = ddb_ssl,
            self.ddb_ssl_cert = ddb_ssl_cert,
            self.ddb_public_key = ddb_public_key

        def conn_ddb(self):
            try:
                engine = pymongo.MongoClient

                cnxn = engine('mongodb://%s:%s@%s:%s'
                              % (self.ddb_user, self.ddb_pwd,
                                 self.ddb_host, self.ddb_port),
                              ssl=self.ddb_ssl,
                              ssl_cert_reqs=self.ddb_ssl_cert,
                              ssl_ca_certs=self.ddb_public_key
                              )

            except ValueError as e:
                print(e)
            return cnxn

    class SQLServer:
        def __init__(self, sqls_host, sqls_user,
                     sqls_pwd, sqls_db):
            self.sqls_server = sqls_host
            self.sqls_user = sqls_user
            self.sqls_pwd = sqls_pwd
            self.sqls_db = sqls_db

        def conn_sqls(self):
            try:
                cnxn = pymssql.connect(server=self.sqls_host,
                                       user=self.sqls_user,
                                       password=self.sqls_pwd,
                                       database=self.sqls_db)
            except ValueError as e:
                print(e)
            return cnxn

    class Secrets:
        def __init__(self, secret, region):
            self.secret_name = secret
            self.region_name = region

        def get_secret(self):
            session = boto3.session.Session()

            client = session.client(service_name='secretsmanager',
                                    region_name=self.region_name)

            try:
                get_secret_value_response = client.get_secret_value(SecretId=self.secret_name)

            except ClientError as e:
                if e.response['Error']['Code'] == 'DecryptionFailureException':
                    raise e

                elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                    raise e

                elif e.response['Error']['Code'] == 'InvalidParameterException':
                    raise e

                elif e.response['Error']['Code'] == 'InvalidRequestException':
                    raise e

                elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                    raise e

            else:
                if 'SecretString' in get_secret_value_response:
                    secret = get_secret_value_response['SecretString']

                else:
                    decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])

            return json.loads(secret)

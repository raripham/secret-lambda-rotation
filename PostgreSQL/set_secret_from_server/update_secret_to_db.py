import boto3
import json
import pg
import pgdb

def set_secret(current_dict,previous_dict):
    conn = get_connection(previous_dict)
    try:
        with conn.cursor() as cur:
            escaped_username = current_dict['username']
            alter_role = "ALTER USER %s" % escaped_username
            cur.execute(alter_role + " WITH PASSWORD %s", (current_dict['password'],))
            conn.commit()
    finally:
        conn.close()
def test_secret(service_client,arn):
    conn = get_connection(get_secret_dict(service_client, arn, "AWSCURRENT"))
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT NOW()")
                conn.commit()
        finally:
            conn.close()

        print("test connection to DB with new secret OK")
        return
    else:
        print("test connection to DB with new secret FAIL")
        raise ValueError("Unable to log into database with current secret of secret ARN %s" % arn)

def get_secret_dict(service_client, arn, stage, token=None):
    required_fields = ['host', 'username', 'password']

    # Only do VersionId validation against the stage if a token is passed in
    if token:
        secret = service_client.get_secret_value(SecretId=arn, VersionId=token, VersionStage=stage)
    else:
        secret = service_client.get_secret_value(SecretId=arn, VersionStage=stage)
    plaintext = secret['SecretString']
    secret_dict = json.loads(plaintext)

    # Run validations against the secret
    if 'engine' not in secret_dict or secret_dict['engine'] != 'postgres':
        raise KeyError("Database engine must be set to 'postgres' in order to use this rotation lambda")
    for field in required_fields:
        if field not in secret_dict:
            raise KeyError("%s key is missing from secret JSON" % field)

    # Parse and return the secret JSON string
    return secret_dict

def get_connection(secret_dict):
    # Parse and validate the secret JSON string
    port = int(secret_dict['port']) if 'port' in secret_dict else 5432
    dbname = secret_dict['dbname'] if 'dbname' in secret_dict else "postgres"

    conn = connect_and_authenticate(secret_dict, port, dbname)
    
    return conn

def connect_and_authenticate(secret_dict, port, dbname):
    conn = pgdb.connect(host=secret_dict['host'], user=secret_dict['username'], password=secret_dict['password'], database=dbname, port=port,
                                connect_timeout=10, sslmode='disable')
    return conn


def update_pass():

    service_client = boto3.client("secretsmanager")
    secret_ls = ('poem-batch2',)
    #secret_ls = ('poem-batch','poem-backend','poem-auth','poem-market','poem-ws')
    with open('secrets.json') as secret:
        secret_list = json.load(secret)
        for sec in secret_ls:
            arn = secret_list[sec]
            #print(arn)
            current_dict = get_secret_dict(service_client, arn, "AWSCURRENT")
            previous_dict = get_secret_dict(service_client, arn, "AWSPREVIOUS")
            
            set_secret(current_dict,previous_dict)
            test_secret(service_client,arn)

update_pass()

def prepare_sql_data(data):
    sql_data = {
        'query': data['args'][data['config']['argsIndex']],
        'poSessionId': data['result']
    }

    return sql_data

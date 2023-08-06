def parse_args(r_args):
    
    columns = r_args.get('columns')
    args = {key:value for (key,value) in r_args.items() if key not in ('columns', 'api_key')}

    return columns, args
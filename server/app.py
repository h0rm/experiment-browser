from flask import Flask, jsonify, request
import os
import json

app = Flask(__name__)

def dict_flatten(dct):
    flat = []

    for k, v in dct.items():
        if isinstance(v, dict):
            flat.extend([[k] + i for i in dict_flatten(v)])

        elif isinstance(v, list):
            flat.extend([[k] + f for f in dict_flatten({i: l})][0] for i, l in enumerate(v))

        else:
            flat.append([k, v])
    return flat


def join_flat(flat):
    return {'.'.join(map(str, i[0:-1])): i[-1] for i in flat}

table = os.path.expanduser('table.json')
table_json = json.load(open(table))

table_flat = [join_flat(dict_flatten(j)) for j in table_json]


@app.route('/')
def hello_world():
    print('Number of entries: {}'.format(len(table_json)))
    return jsonify(table_json)

@app.route('/entries')
def entries():
    items = list(request.args.items())

    def filter_fnc(x):
        res = True

        for k, v in items:
            res = res and k in x

            if v:
                res = res and str(x[k]) == v

        return res

    if len(items) > 0:
        fltr = [ j for (f, j) in zip(table_flat, table_json) if filter_fnc(f)]
        return jsonify(fltr)


    return jsonify(table_flat)

if __name__ == '__main__':
    app.run()

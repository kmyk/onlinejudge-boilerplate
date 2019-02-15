import base64
import pathlib
import re
import subprocess
import urllib.parse

import flask
from flask import abort, jsonify
from flask_cors import CORS
import onlinejudge
import requests

app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

def generate_data(problem):
    # check
    url = 'http://atcoder.jp/contests/{}/tasks/{}'.format(problem.contest_id, problem.problem_id)
    resp = requests.get(url)
    if resp.status_code != 200:
        abort(400, 'problem not found / 問題ページにアクセスできませんでした')

    # atcoder-tools
    template_path = pathlib.Path(__file__).parent / 'template.cpp'
    proc = subprocess.run([ 'atcoder-tools', 'codegen', '--lang', 'cpp', '--template', template_path, '--without-login', problem.get_url() ], stdout=subprocess.PIPE)
    if proc.returncode:
        abort(400, 'atcoder-tools failed / atcoder-tools での解析に失敗しました')
    code = proc.stdout.decode()

    # online-judge-tools
    if '((SAMPLE_INPUT_PART))' in code:
        samples = problem.download_sample_cases()
        code, _ = re.subn(r'scanf\("[^"]*", *&([^)]+)\)', r'std::cin >> \1', code)
        a, _, b = code.partition('((SAMPLE_INPUT_PART))')
        b = b.replace('std::cin', 'iss')
        code = a + b
        f = lambda sample: '"{}",'.format('\\n'.join(sample.input.data.splitlines()))
        code = code.replace('((SAMPLES))', '\n'.join([ f(sample) for sample in samples ]))

    # clang-format
    proc = subprocess.run([ 'clang-format', '-style={ "IndentWidth": 4 }' ], input=code.encode(), stdout=subprocess.PIPE)
    proc.check_returncode()
    code = proc.stdout.decode()

    return code

@app.errorhandler(400)
def bad_request(e):
    return flask.jsonify({ 'error': str(e) }), 400

@app.route("/<path:requested_url>")
def index(requested_url):

    problem = onlinejudge.dispatch.problem_from_url(requested_url.replace(':/', '://'))
    if problem is None:
        abort(400, 'URL is not reconginzed / URL が認識できません')
    if problem.get_service().get_name() != 'atcoder':
        abort(400, 'problem is not one of AtCoder / まだ AtCoder にしか対応していません')

    key = base64.b64encode(problem.get_url().encode()).decode()
    cache_path = pathlib.Path(__file__).parent / 'cache' / key[: 2] / (key + ".cpp")
    if cache_path.exists():
        with cache_path.open() as fh:
            data = fh.read()
    else:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with cache_path.open('w') as fh:  # open the file as a poor flock
                data = generate_data(problem)
                fh.write(data)
        except:
            if cache_path.exists():
                cache_path.unlink()
            raise

    return jsonify({ 'data': data })

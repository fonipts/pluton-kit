from bottle import route, run, template

@route('/health/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

({SQL_ALCH_DB})
run(host='localhost', port=8080)

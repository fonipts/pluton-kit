from bottle import route, run, template
({SQL_ALCH_IMPORT})

@route('/health/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

({SQL_ALCH_DB_CONTENT})
run(host='localhost', port=8080)

'''run.py file'''
from flask import jsonify, render_template
from application import create_app

config_name = 'development'
app = create_app(config_name)

'''Error handlers'''
@app.errorhandler(400)
def bad_request(error):
    '''error handler for Bad request'''
    return jsonify(dict(error = 'Bad request')), 400
@app.errorhandler(404)
def page_not_found(error):
    '''error handler for 404'''
    return jsonify(dict(error = 'Page not found')), 404

@app.errorhandler(405)
def unauthorized_method(error):
    '''error handler for 405'''
    return jsonify(dict(error = 'Method not allowed')), 405

@app.errorhandler(500)
def server_error(error):
    '''error handler for 404'''
    return jsonify(dict(error = 'Internal server error')), 500

@app.route('/')
def home():
    '''method to render documentation'''
    return render_template('documentation.html'), 200

if __name__ == '__main__':
    app.run()

from project import app

if __name__ == '__main__':
    
    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"
    
    app.run(host="0.0.0.0", debug=True)
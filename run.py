from wingman_api import app

if __name__ == '__main__':
    
    # test page
    @app.get("/")
    def hello_world_get():
        return "<p>Hello, World!</p>"
    
    app.run(host="0.0.0.0", debug=True)
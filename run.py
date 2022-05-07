from app import app

app.config['SECRET_KEY'] = '564648sjdhbfl654684adfa'
if __name__ == '__main__':
    app.run(debug = True)
from website import create_app

app = create_app()

if __name__ == '__main__': #only when web server is run directly
    app.run(debug=False, host='0.0.0.0')

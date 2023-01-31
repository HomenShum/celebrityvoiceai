from website import create_app
app = create_app()

if __name__ == '__main__': #only when web server is run directly
    app.run(debug=True) #changes to code will be reflected

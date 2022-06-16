from website import create_app

app = create_app()

if __name__ == '__main__': #Only if we run this file will we execute the line below.
    app.run(debug=True)


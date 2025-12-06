from hello_httpy.HelloHttpy import HelloHttpy

app = HelloHttpy(port=8080)



@app.get("/asdf")
def somefunction():
    return "idk"


print(app._routes)
app.run()



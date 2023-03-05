import sqlite3

from flask import Flask, request, g, render_template, send_file

DATABASE = '/tmp/db.example'
app = Flask(__name__)
app.config.from_object(__name__)

def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

def commit():
    get_db().commit()

@app.route("/")
def hello():
    execute_query("DROP TABLE IF EXISTS userstable")
    execute_query("CREATE TABLE userstable (firstname text,lastname text,email text)")
    return render_template('index.html')

@app.route('/startenquiry', methods =['POST', 'GET'])
def startinquiry():
    message = ''
    if request.method == 'POST' and str(request.form['ufname']) !="" and str(request.form['ulname']) != "" and str(request.form['mail']) != "":
        firstname = str(request.form['ufname'])
        lastname = str(request.form['ulname'])
        email = str(request.form['mail'])
        execute_query("""INSERT INTO userstable (firstname, lastname, email) values (?, ?, ?)""",(firstname, lastname, email))
        commit()
    elif request.method == 'POST':
        message = 'OOPS!! Fields Missing. Fill all fields.'
    return render_template('Chat.html', message = message)

ChatWindowHTMLFirst = """
    <!DOCTYPE html>
<html>
  <title>College Enquiry Chabot</title>
  <head>
    <link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700" rel="stylesheet">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.1/css/all.css" integrity="sha384-5sAR7xN1Nv6T6+dT2mhtzEpVJvfS3NScPQTrOxhwjIuvcA67KV2R5Jz6kr4abQsz" crossorigin="anonymous">
    <style>
      html, body {
      display: flex;
      justify-content: center;
      font-family: Arial, Helvetica, sans-serif;
      font-size: 18px;
      }
      form {
      border: 25px solid #f1f1f1f0;
      }
      input[type=text], input[type=password] {
      width: 100%;
      padding: 16px 8px;
      margin: 10px 0px;
      display: inline-block;
      border: 1px solid #ccc;
      box-sizing: border-box;
      }
      .icon {
      font-size: 110px;
      display: flex;
      justify-content: center;
      color: #0a2b7af5;
      }
      .send-button {
      background-color: #0a2b7af5;
      color: white;
      padding: 12px 0;
      margin: 10px 0;
      border: black;
      cursor: grab;
      width: 12%;
      }
      h1 {
      text-align:center;
      font-size:20;
      }
  .formcontainer {
      text-align: center;
      margin: 25px 50px 25px;
      }
  .text-box {
    font-size: 25px;
 	  display: flex;
 	  width: 100%;
	}
  .container {
      padding: 16px 16px;
      text-align:left;
      }
    </style>
  </head>
      <body>
        <form {{url_for('chatbotsystem')}} method="POST">
          <h1>College Inquiry Chabot</h1>
          <div class="icon">
    	 <i class="fas fa-user-circle"></i>
          </div>
          <div class="formcontainer">
          <div class="container">
           <label for="ufname"><strong>Hi!! Welcome to college inquiry portal</strong></label></br></br>
    	  <label for="ufname"><strong>Choose your questions from below list</strong></label></br>
    	  <label for="ufname"><strong>1.Does the college have a football team?</strong></label></br>
    	  <label for="ufname"><strong>2.Does it have Computer Science Major?</strong></label></br>
    	  <label for="ufname"><strong>3.What is the in-state tuition?</strong></label></br>
    	  <label for="ufname"><strong>4.Does its have on campus housing?</strong></label></br>
    """

ChatWindowHTMLLast = """
    </div>
    	<div class="text-box">
            <input type="text" name="question" id="message" autocomplete="off" placeholder="Tye your Questions here">
    	  <input class="send-button" type="submit" value=">">
          </div>
           <a href='/endchat' align='center'">End Chat</a>
    	</div>
        </form>
      </body>
    </html>
    """


@app.route('/chatbotsystem', methods =['GET', 'POST'])
def chatbotsystem():
    global ChatWindowHTMLFirst
    ChatWindowHTMLMiddle = ''
    if request.method == 'POST' and str(request.form['question']) !="":
        questionasked = str(request.form['question'])
        if(questionasked in "Does the college have a football team?"):
            ChatWindowHTMLMiddle="""
            </br><label for="ufname" style="color:blue;"><strong>"""+questionasked+"""</strong></label></br>
            <label for ="ufname"><strong> Yes! Bearcats is the football team name </strong></label></br>
            """
            # answergiven="Yes! Bearcats is the football team name"
        elif(questionasked in "Does it have Computer Science Major?"):
            ChatWindowHTMLMiddle = """
            </br><label for="ufname" style="color:blue;"><strong>""" + questionasked + """</strong></label></br>
            <label for ="ufname"><strong>Yes! It has Computer Science Major</strong></label></br>
            """
            # answergiven = "Yes! It has Computer Science Major"
        elif (questionasked in "What is the in-state tuition?"):
            ChatWindowHTMLMiddle = """
            </br><label for="ufname" style="color:blue;"><strong>""" + questionasked + """</strong></label></br>
            <label for ="ufname"><strong> The total tuition and living expense budget for in-state Ohio residents to go to UC is $28,150</strong></label></br>
            """
            # answergiven = "The total tuition and living expense budget for in-state Ohio residents to go to UC is $28,150"
        elif (questionasked in "Does its have on campus housing?"):
            ChatWindowHTMLMiddle = """
            </br><label for="ufname" style="color:blue;"><strong>""" + questionasked + """</strong></label></br>
            <label for ="ufname"><strong> No!! it doesn't have campus housing</strong></label></br>
            """
            # answergiven = "No!! it doesn't have campus housing"
        else:
            ChatWindowHTMLMiddle = """
            </br><label for="ufname" style="color:blue;"><strong>""" + questionasked + """</strong></label></br>
            <label for ="ufname"><strong> Sorry!! I don't have answer to your question</strong></label></br>
            """
            # answergiven = "Sorry!! I don't have answer to your question"
    ChatWindowHTMLFirst=ChatWindowHTMLFirst + ChatWindowHTMLMiddle
    return ChatWindowHTMLFirst+ChatWindowHTMLLast

EndChatHTMLFirst="""
<!DOCTYPE html>
<html>
  <title>Session Closed</title>
  <head>
    <link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700" rel="stylesheet">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.1/css/all.css" integrity="sha384-5sAR7xN1Nv6T6+dT2mhtzEpVJvfS3NScPQTrOxhwjIuvcA67KV2R5Jz6kr4abQsz" crossorigin="anonymous">
    <style>
      html, body {
      display: flex;
      justify-content: center;
      font-family: Roboto, Arial, sans-serif;
      font-size: 15px;
      }
      form {
      border: 5px solid #f1f1f1;
      }
      input[type=text], input[type=password] {
      width: 100%;
      padding: 16px 8px;
      margin: 8px 0;
      display: inline-block;
      border: 1px solid #ccc;
      box-sizing: border-box;
      }
      .icon {
      font-size: 110px;
      display: flex;
      justify-content: center;
      color: #4286f4;
      }
      .send-button {
      background-color: #4286f4;
      color: white;
      padding: 12px 0;
      margin: 10px 0;
      border: none;
      cursor: grab;
      width: 12%;
      }
	.end-button {
      background-color: #FF0000;
      color: white;
      padding: 12px 0;
      margin: 10px 0;
      border: none;
      cursor: grab;
      width: 12%;
      }
      h1 {
      text-align:center;
      fone-size:18;
      }
      button:hover {
      opacity: 0.8;
      }
      .formcontainer {
      text-align: center;
      margin: 24px 50px 12px;
      }
	.text-box {
  	font-size: 16px;
 	 display: flex;
 	 width: 100%;
	}
      .container {
      padding: 16px 0;
      text-align:left;
      }
      span.psw {
      float: right;
      padding-top: 0;
      padding-right: 15px;
      }
      /* Change styles for span on extra small screens */
      @media screen and (max-width: 300px) {
      span.psw {
      display: block;
      float: none;
      }
    </style>
  </head>
  <body>
    <form>
      <h1>Chat Session Closed</h1>
      <div class="formcontainer">
      <div class="container">
        <label for="ufname"><strong>Hope your Questions are answered!!</strong></label></br></br>
"""

EndChatHTMLLast="""
 </div>
	</div>
    </form>
  </body>
</html>
"""
@app.route("/endchat")
def endchat():
    global ChatWindowHTMLFirst
    ChatWindowHTMLFirst = """
<!DOCTYPE html>
<html>
  <title>College Enquiry Chabot</title>
  <head>
    <link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700" rel="stylesheet">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.1/css/all.css" integrity="sha384-5sAR7xN1Nv6T6+dT2mhtzEpVJvfS3NScPQTrOxhwjIuvcA67KV2R5Jz6kr4abQsz" crossorigin="anonymous">
    <style>
      html, body {
      display: flex;
      justify-content: center;
      font-family: Arial, Helvetica, sans-serif;
      font-size: 18px;
      }
      form {
      border: 25px solid #f1f1f1f0;
      }
      input[type=text], input[type=password] {
      width: 100%;
      padding: 16px 8px;
      margin: 10px 0px;
      display: inline-block;
      border: 1px solid #ccc;
      box-sizing: border-box;
      }
      .icon {
      font-size: 110px;
      display: flex;
      justify-content: center;
      color: #0a2b7af5;
      }
      .send-button {
      background-color: #0a2b7af5;
      color: white;
      padding: 12px 0;
      margin: 10px 0;
      border: black;
      cursor: grab;
      width: 12%;
      }
      h1 {
      text-align:center;
      font-size:20;
      }
  .formcontainer {
      text-align: center;
      margin: 25px 50px 25px;
      }
  .text-box {
    font-size: 25px;
 	  display: flex;
 	  width: 100%;
	}
  .container {
      padding: 16px 16px;
      text-align:left;
      }
    </style>
  </head>
          <body>
            <form {{url_for('chatbotsystem')}} method="POST">
              <h1>College Inquiry Chabot</h1>
              <div class="icon">
        	 <i class="fas fa-user-circle"></i>
              </div>
              <div class="formcontainer">
              <div class="container">
               <label for="ufname"><strong>Hi!! Welcome to college inquiry portal</strong></label></br></br>
        	  <label for="ufname"><strong>Choose your questions from below list</strong></label></br>
        	  <label for="ufname"><strong>1.Does the college have a football team?</strong></label></br>
        	  <label for="ufname"><strong>2.Does it have Computer Science Major?</strong></label></br>
        	  <label for="ufname"><strong>3.What is the in-state tuition?</strong></label></br>
        	  <label for="ufname"><strong>4.Does its have on campus housing?</strong></label></br>
        """
    result = execute_query("""SELECT firstname,lastname,email  FROM userstable""")
    if result:
        for row in result:
            Userdetails=row[0]+","+row[1]+","+row[2]
    EndChatHTMLMiddle="""
    [User Details]<br>
    <label for="ufname"><strong>"""+Userdetails+"""</strong></label></br></br>
    [Creator Details]<br>
    <label for="ufname"><strong>HasiniRasagna Shakamuri, shakamha@mail.uc.edu</strong></label></br></br>
    """
    return EndChatHTMLFirst+EndChatHTMLMiddle+EndChatHTMLLast

if __name__ == '__main__':
  app.run()
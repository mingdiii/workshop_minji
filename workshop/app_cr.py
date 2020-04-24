import os
import pymysql
from datetime import datetime
from flask import Flask, render_template
from flask import request, redirect, abort, session, jsonify

app=Flask(__name__, static_folder="static",
                    template_folder="views")

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.secret_key = 'twomin'

db = pymysql.connect(
    user='root',
    passwd='123456',
    host='localhost',
    db='web',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)

members = [
    {"id" : "sumin", "pw" : "111111"},
    {"id" : "minji", "pw": "222222"}
    
]

def get_menu():
    menu_temp = "<li><a href='/{0}'>{0}</a></li>"
    menu=[e for e in os.listdir('workshop_content') if e[0] != '.']
    return "\n".join([menu_temp.format(m) for m in menu])

def get_review():
    menu_temp1 = "<li><a href='/reviews/{0}'>{0}</a></li>"
    menu=[e for e in os.listdir('workshop_content/Review') if e[0] != '.']
    return "\n".join([menu_temp1.format(m) for m in menu])

def get_template(filename):
    print(filename)
    with open( filename, 'r', encoding='utf-8')as f:
        template=f.read()
    return template    


@app.route('/')
def index():
    if 'user' in session:
        title = '★ Welcome!! ' + session['user']['id']+ '★'
    else:
        title = 'Welcome'
        
    menu=get_menu()
    return render_template('main.html',
                           title=title,
                           menu=menu)

@app.route('/main2')
def main2():
    if 'user' in session:
        title = '★ Welcome!! ' + session['user']['id']+ '★'
    else:
        title = 'Welcome'
        
    menu=get_menu()
    return render_template('main2.html',
                           title=title,
                           menu=menu)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/<title>')
def html(title):
   
    menu=get_menu()
    return render_template(f'{title}.html',
                           title=title,
                           menu=menu)


#     with open(f'workshop_content/{title}', 'r', encoding="utf-8") as f:
#         content = f.read()
#     return template.format(title,content,menu)

  
    
# @app.route("/delete/<title>")
# def delete(title):
#     os.remove(f"content/{title}")
#     return redirect("/")

@app.route("/reviews/<title>")
def reviews(title):
    menu=get_review()
    with open(f'workshop_content/Review/{title}', 'r', encoding="utf-8") as f:
        content = f.read()
  
    return render_template('review.html', 
                            content=content, 
                            menu=menu)
    

@app.route("/review", methods=['GET', 'POST'])
def review():
    menu=get_review()
    
    if request.method=="GET":
        return render_template('review.html', 
                               message='', 
                               menu=menu,
                               name='')
    
    elif request.method=="POST":
        with open(f'workshop_content/Review/{request.form["title"]}', 'w', encoding="utf-8") as f:
            f.write(request.form['desc'])
    
        return redirect('/review')
    

# @app.route("/delete/<title>")
# def delete(title):
#     os.remove(f'workshop_content/Review/{title}')
#     return redirect("/review")
    
 
       
    
@app.route('/login_page', methods=['GET', 'POST'])
def login():
    menu=get_menu()
    
    if request.method=="GET":
        return render_template('login_page.html', 
                               message="", 
                               menu=menu)
    
    elif request.method=="POST":
        #만약 회원이 아니면, 회원이 아닙니다.라고 알려주자
        m= [e for e in members if e['id']== request.form['id']]
        if len(m) ==0:
            return render_template('login_page.html', 
                                   message="<p>회원이 아닙니다.</p>", 
                                   menu=menu)
        
        #만약 패스워드가 다르면, "패스워드를 확인해주세요"
            return render_template('login_page.html', 
                                   message="<p>패스워드를 확인해 주세요</p>", 
                                   menu=menu)
        
        #로그인 성공에는 메인으로
        session['user'] = m[0]
        return redirect("/main2")    
    

@app.route("/favicon.ico")
def favicon():
    return abort(404)
    
app.run(port=5001)
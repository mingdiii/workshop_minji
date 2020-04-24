import os
from flask import Flask
from flask import request, redirect, abort
# $env:FLASK_ENV="development"

app=Flask(__name__, static_folder="static")


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
    id=request.args.get('id', '')
    template = get_template('main.html')
    
    title = '★ Welcome!! '+ id + '★' 
    
    menu=get_menu()
    return template.format(title , menu)

@app.route('/main2')
def main2():
    id=request.args.get('id', '')
    template = get_template('main2.html')
    
    title = '★ Welcome!!'+" "+ id + '★'
    menu=get_menu()
    return template.format(title, menu)


@app.route('/<title>')
def html(title):
    template=get_template(f'{title}.html')    
    menu=get_menu()
    return template.format(title,template,menu)
#     with open(f'workshop_content/{title}', 'r', encoding="utf-8") as f:
#         content = f.read()
#     return template.format(title,content,menu)

  
    
# @app.route("/delete/<title>")
# def delete(title):
#     os.remove(f"content/{title}")
#     return redirect("/")

@app.route("/reviews/<title>")
def reviews(title):
    template=get_template('review.html') 
    menu=get_review()
    with open(f'workshop_content/Review/{title}', 'r', encoding="utf-8") as f:
        content = f.read()
    return template.format(title, menu, content)
    
    

@app.route("/review", methods=['GET', 'POST'])
def review():
    template = get_template('review.html')
    menu=get_review()
    
    if request.method=="GET":
        return template.format("", menu, "")
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
    template=get_template('login_page.html')
    menu=get_menu()
    
    if request.method=="GET":
        return template.format("", menu)
    
    elif request.method=="POST":
        #만약 회원이 아니면, 회원이 아닙니다.라고 알려주자
        m= [e for e in members if e['id']== request.form['id']]
        if len(m) ==0:
            return template.format("<p>회원이 아닙니다.</p>", menu)
        
        #만약 패스워드가 다르면, "패스워드를 확인해주세요"
        if request.form['pw']!= m[0]['pw']:
            return template.format("<p>패스워드를 확인해주세요.</p>", menu)
        
        #로그인 성공에는 메인으로
      
        return redirect('/main2?id='+ m[0]['id'])

@app.route("/favicon.ico")
def favicon():
    return abort(404)
    
app.run(port=5001)
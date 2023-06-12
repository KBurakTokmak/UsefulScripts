from flask import *
from forms import ID_Form
from id_check import id_check
app = Flask(__name__)
app.config['SECRET_KEY']='zlwxX9sLltxof4paskT6/W0rIKor4dFmEWIClyCw9PzPzLVBbkN9ZByxRe50hmLC'
@app.route('/')
def home():
    return "This is the homepage"

@app.route('/valid_id',methods=["GET","POST"])
def valid_id():
    form=ID_Form()
    if form.is_submitted():
        result=request.form.getlist("id")
        check=id_check(result[0])
        
        return render_template("result.html",valid=check[0],message=check[1])
    return render_template("valid_id.html",form=form)



if __name__ == "__main__":
    app.run()



id="12345678950"
check=id_check(id)
if(check[0]):
    print("Valid ID")
else:
    print(check[1])

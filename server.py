from flask import Flask,render_template,jsonify,request
from lib.game import Status, update

app = Flask(__name__,template_folder='./public',static_folder='./public/js')

s = Status()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/action',methods=["POST"])
def action():
    
    # リクエストを受け取る
    action_request = request.get_json()

    action_input = {"player":(s.phase)//3, "x":action_request["row"], "y":action_request["col"], "power":False, "own":None}

    # リクエストを基に状態を更新
    update(s, action_input)
    
    return jsonify( {"board": s.field.tolist(), "phase":s.phase, "own":s.own.tolist(), "selected":s.select_pos, "end":s.end} )

@app.route('/power',methods=["POST"])
def power():
    
    # リクエストを受け取る
    action_request = request.get_json()

    action_input = {"player":(s.phase)//3, "x":None, "y":None, "power":action_request["power"]=="yes", "own":None}

    # リクエストを基に状態を更新
    update(s, action_input)
    
    return jsonify( {"board": s.field.tolist(), "phase":s.phase, "own":s.own.tolist(), "selected":s.select_pos, "end":s.end} )

@app.route('/own',methods=["POST"])
def own():
    
    # リクエストを受け取る
    action_request = request.get_json()

    action_input = {"player":(s.phase)//3, "x":None, "y":None, "power":False, "own":action_request["own"]}

    # リクエストを基に状態を更新
    update(s, action_input)

    return jsonify( {"board": s.field.tolist(), "phase":s.phase, "own":s.own.tolist(), "selected":s.select_pos, "end":s.end} )

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8000)
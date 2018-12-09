from flask import Flask, render_template, request, jsonify, session
import uuid
import queue

app = Flask(__name__)
app.secret_key = 'abcdfaf'

USERS = {
    '1': {'name': '贝贝', 'count': 1},
    '2': {'name': 'daming', 'count': 0},
    '3': {'name': 'lingling', 'count': 0}
}

QUEUE_DICT = {}

@app.route('/user/list')
def user_list():
    user_uuid = str(uuid.uuid4())
    QUEUE_DICT[user_uuid] = queue.Queue()
    session['current_user_uuid'] = user_uuid
    return render_template('user_list.html', users=USERS)

@app.route('/vote', methods=['POST'])
def vote():
    uid = request.form.get('uid')
    USERS[uid]['count'] += 1
    for q in QUEUE_DICT.values():
        q.put(USERS)
    return '投票成功'

@app.route('/get/vote', methods=['GET'])
def get_vote():
    user_uuid = session['current_user_uuid']
    q = QUEUE_DICT[user_uuid]
    ret = {'status': True, 'data': None}
    try:
        users = q.get(timeout=20)
        ret['data'] = users
    except queue.Empty:
        ret['status'] = False
    # 以json格式返回给html
    return jsonify(ret)

if __name__ == '__main__':
    app.run(host='10.40.25.15', threaded=True)
from flask import Flask, request, jsonify

app = Flask(__name__)

polls = {}


@app.route('/api/createPoll/', methods=['POST'])
def create_poll():
    data = request.get_json()
    title = data.get('title')
    options = data.get('options', [])

    if not title:
        return jsonify({'error': 'Не указано название голосования'}), 400

    if not options:
        return jsonify({'error': 'Не указаны варианты ответов'}), 400

    poll_id = len(polls) + 1
    poll = {'title': title, 'options': options, 'votes': [0] * len(options)}
    polls[poll_id] = poll

    return jsonify({'poll_id': poll_id, 'message': 'Голосование создано'})


@app.route('/api/poll/', methods=['POST'])
def vote():
    data = request.get_json()
    poll_id = data.get('poll_id')
    choice_id = data.get('choice_id')

    if poll_id not in polls:
        return jsonify({'error': 'Голосование не существует'}), 404

    poll = polls[poll_id]

    if choice_id < 0 or choice_id >= len(poll['options']):
        return jsonify({'error': 'Неверный вариант ответа'}), 400

    poll['votes'][choice_id] += 1

    return jsonify({'message': 'Голос засчитан'})


@app.route('/api/getResult/<int:poll_id>', methods=['GET'])
def get_result(poll_id):
    if poll_id not in polls:
        return jsonify({'error': 'Голосование не существует'}), 404

    poll = polls[poll_id]
    result = {poll['options'][i]: poll['votes'][i] for i in range(len(poll['options']))}

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)

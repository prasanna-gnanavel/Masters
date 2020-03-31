from flask import Flask,jsonify,json,request

with open('records.json') as f:
	all_records = json.load(f)
	
app = Flask(__name__)

@app.route('/')
def hello():
	return "<h1>Hello, Welocme to my webpage 2 webalbum Prasanna!</h1>"
	
@app.route('/records/', methods=['GET'])
def get_all_records():
	return jsonify(all_records)
	
@app.route('/records/<bandname>/', methods=['GET','DELETE'])
def get_albums_by_band(bandname):
	albums = [band['albums'] for band in all_records if band['name'] == bandname]
	if len(albums)==0:
		return jsonify({'error':'band name not found!'}), 404
	else:
		response = [album['title'] for album in albums[0]]
		return jsonify(response), 200

@app.route('/records/', methods=['POST'])
def create_a_record():
	if not request.json or not 'name' in request.json:
		return jsonify({'error':'the new record needs to have a band name'}), 400
	new_record = {
		'name': request.json['name'],
		'albums': request.json.get('albums', '')
	}
	all_records.append(new_record)
	return jsonify({'message': 'created: /records/{}'.format(new_record['name'])}), 201

@app.route('/records/all_bands/', methods=['GET'])
def get_bands():
	response = [item['name'] for item in all_records]
	return jsonify(response)
	
@app.route('/record1/<bandname>/', methods=['DELETE'])
def delete_a_band(bandname):
	matching_records = [band for band in all_records if band['name'] == bandname]
	if len(matching_records)==0:
		return jsonify({'error':'band name not found!'}), 404
	all_records.remove(matching_records[0])
	return jsonify({'success': True})



if __name__ == '__main__':
	app.run(host='0.0.0.0')

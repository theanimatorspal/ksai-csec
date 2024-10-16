from flask import Flask, jsonify, send_file
import zipfile
import io
import os

app = Flask(__name__)

@app.route('/map.json')
def serve_map():
    response = { 
        "maps-0.13.0_0-path": "maps",
        "hextree-flag": "HXT{cleartext-traffic-g19g2is}",
        "maps-0.13.0_0":
        [
            { "name": "australia-oceania_wallis-et-futuna", "size": "812K", "time": "2024-02" },
            { "name": "australia-oceania_niue", "size": "684K", "time": "2024-02" },
        ]
}


    return jsonify(response)

@app.route('/map.zip')
def map_archive():
    # Create a zip file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        # Adding a sample text file to the zip
        zip_file.writestr('../../downloads/hax', 'This is a sample text file.')

    zip_buffer.seek(0)
    return send_file(zip_buffer, as_attachment=True, download_name='map.ghz', mimetype='application/zip')

if __name__ == '__main__':
    app.run(debug=True, port=1234)

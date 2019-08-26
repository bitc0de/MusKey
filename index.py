from flask import Flask, render_template, request, send_from_directory
import os
import re, urllib, os, sys, argparse,time
import urllib.request
import urllib.parse
import shutil
urlopen = urllib.request.urlopen
encode = urllib.parse.urlencode
retrieve = urllib.request.urlretrieve
cleanup = urllib.request.urlcleanup()


app= Flask(__name__)
nombreCancion=""
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/buscarcancion', methods=['POST'])
def buscarCancion():
    global nombreCancion
    if request.method == 'POST':
        nombreCancion= request.form['cnc']
        if os.path.isdir("canciones/"+nombreCancion+".mp3") ==True:
            return render_template('cancion.html', variable=nombreCancion)

        if "youtube.com/" not in nombreCancion:
            try:
                query_string = encode({"search_query": nombreCancion})
                html_content = urlopen("http://www.youtube.com/results?" + query_string)

                search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
                command = 'youtube-dl -v -4 --embed-thumbnail --no-warnings --extract-audio --audio-format mp3 --id ' + \
                          search_results[0]
                title2 = search_results[0]
                os.system(command)

                os.rename((title2+".mp3"), (nombreCancion+".mp3"))
                shutil.move((nombreCancion+".mp3"), ("./canciones/"+nombreCancion+".mp3"))


                return render_template('cancion.html', variable=nombreCancion)
            except:
                return "Error al descargar la cancion"

@app.route('/return-files', methods=['GET'])
def return_file():
    can1=nombreCancion+".mp3"
    return send_from_directory(directory='canciones/', filename=can1, as_attachment=True)



@app.route('/about')
def about():
    return render_template('about.html')


if __name__ =='__main__':
    app.run(debug=True)
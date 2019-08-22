import telegram
import subprocess
import telegram.ext
import glob
import random

import re, urllib, os, sys, argparse,time
title2=""
WEB = range(1)

def cnc1(bot, update):
    global title2
    update.message.reply_text("Tu descarga esta lista:")
    print (title2)
    bot.send_audio(chat_id, audio=open(title2 + ".mp3", 'rb'))



version = sys.version_info[0]

if version == 2:  # python 2.x
    user_input = raw_input
    import urllib2
    urlopen = urllib2.urlopen  # open a url
    encode = urllib.urlencode  # encode a search line
    retrieve = urllib.urlretrieve  # retrieve url info
    cleanup = urllib.urlcleanup()  # cleanup url cache

else:  # python 3.x
    user_input = input
    import urllib.request
    import urllib.parse
    urlopen = urllib.request.urlopen
    encode = urllib.parse.urlencode
    retrieve = urllib.request.urlretrieve
    cleanup = urllib.request.urlcleanup()


# function to retrieve video title from provided link
def video_title(url):
    try:
        webpage = urlopen(url).read()
        title = str(webpage).split('<title>')[1].split('</title>')[0]

    except:
        title = 'Youtube Song'

    return title


def start(bot, update, user_data):
    update.message.reply_text("Introduce el nombre de cancion:")

    return WEB


def web(bot, update, user_data, song=None):
    global title2
    user_data['web'] = update.message.text

    if not(song):
        song = user_data['web']

    if "youtube.com/" not in song:
        # try to get the search result and exit upon error
        try:
            query_string = encode({"search_query" : song})
            html_content = urlopen("http://www.youtube.com/results?" + query_string)

            if version == 3:  # if using python 3.x
                search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
            else:  # if using python 2.x
                search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read())
        except:
            print('Error de red')
            return None

        # make command that will be later executed
        chat_id = update.message.chat_id
        bot.send_message(chat_id, "Estoy buscando la cancion..dame unos segundos..")
        command = 'youtube-dl --embed-thumbnail --no-warnings --extract-audio --audio-format mp3 --id ' + search_results[0]
        title2 = search_results[0]


    else:      # For a link
        # make command that will be later executed
        command = 'youtube-dl --embed-thumbnail --no-warnings --extract-audio --audio-format mp3 -o "%(title)s.%(ext)s" ' + song[song.find("=")+1:]
        song=video_title(song)

    try:       # Try downloading song

        print('Descargando...')





        os.system(command)
    except:
        print('Error descargando %s' % song)

        return None

    chat_id = update.message.chat_id
    bot.send_message(chat_id, "Disfruta de "+ user_data['web'])
    os.rename((title2+".mp3"), (song + ".mp3"))
    bot.send_audio(chat_id, audio=open(song+".mp3", 'rb'))
    bot.send_message(chat_id, "Recuerda escribir /start para buscar de nuevo")


    user_data.clear()

    return telegram.ext.ConversationHandler.END


def cancelar(bot, update, user_data):
    user_data.clear()

    update.message.reply_text("La busqueda ha sido cancelada.", reply_markup=ReplyKeyboardRemove())

    return telegram.ext.ConversationHandler.END


def main():
    updater = telegram.ext.Updater("943863871:AAEsKDScBz5RmJs21u1MNP5SMxMTclk6bTU")

    dp = updater.dispatcher

    dp.add_handler(telegram.ext.CommandHandler("cnc1", cnc1))
    conv_handler = telegram.ext.ConversationHandler(

        entry_points=[telegram.ext.CommandHandler('start', start, pass_user_data=True)],

        states={

            WEB: [telegram.ext.MessageHandler(telegram.ext.Filters.text,

                                              web,

                                              pass_user_data=True), ],

        },

        fallbacks=[telegram.ext.CommandHandler("cancelar", cancelar, pass_user_data=True)]

    )

    dp.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
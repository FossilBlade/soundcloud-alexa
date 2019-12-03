# -*- coding: utf-8 -*-

import logging
import os

import json
import soundcloud

from flask import Flask, jsonify

from flask_ask import Ask, statement, audio, session, logger as log, request

from queue_manager import QueueManager
from ssml_builder import SSML

import session_handler as sh

## Soundcloud Setup
sc_client_id = "8c63b5c6be310a43a0695f442b90d53d"
sc_client = soundcloud.Client(client_id=sc_client_id)
sc_my_user_id = os.environ.get("AS_USER_ID") or 24758916

sc_access_token = os.environ.get("AS_ACCESS_TOKEN")
if sc_access_token:
    sc_client = soundcloud.Client(access_token=sc_access_token)

## Flask-Ask Setup
app = Flask(__name__)

ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.INFO)

# queue = None
logging.info("Initial")

@app.route("/links")
def all_links():
    links = []
    for rule in app.url_map.iter_rules():
        url = rule.rule
        links.append(url)
    return jsonify(links)


def getStreamUrl(track_id):
    return "https://api.soundcloud.com/tracks/{}/stream?client_id={}".format(track_id, sc_client_id)


def getTrack(_id):
    return sc_client.get('/tracks/' + str(_id)).fields()


@ask.launch
def launch():

    return start_playlist()


@ask.intent('PodcastIntent')
def start_playlist():
    log.info(str(request))
    log.info(session.user.userId)
    queue = get_queue(session.user.userId)

    if not queue.isEmpty():
        speech = 'resuming from where you left off'
        track_id = queue.current
    else:
        speech = 'playing the latest podcast'

        tracks = sc_client.get('/users/' + str(sc_my_user_id) + '/tracks', linked_partitioning=1)
        tracks = json.loads(tracks.raw_data)['collection']
        for track in tracks:
            queue.add(track['id'])
        track_id = queue.start()
        save_queue(session.user.userId, queue)

    stream_url = getStreamUrl(track_id)
    return audio(speech).play(stream_url)


@ask.default_intent
def default_intent():
    log.info("Called Default Intent. Request: {}".format(request))

# QueueManager object is not stepped forward here.
# This allows for Next Intents and on_playback_finished requests to trigger the step
@ask.on_playback_nearly_finished()
def nearly_finished():
    log.info(request)
    queue = get_queue(session.user.userId)

    if queue.up_next:
        next_id = queue.up_next
        return audio().enqueue(getStreamUrl(next_id))


@ask.on_playback_finished()
def play_back_finished():

    log.info(request)
    queue = get_queue(session.user.userId)

    if queue.up_next:
        queue.step()
        session.attributes["data"] = queue.export()
        # session.attributes["current_track"] = str(queue.current)
    else:
        return statement('You are all caught up with the latest in software engineering.')


# NextIntent steps queue forward and clears enqueued streams that were already sent to Alexa
# next_stream will match queue.up_next and enqueue Alexa with the correct subsequent stream.
@ask.intent('AMAZON.NextIntent')
def next_song():
    log.info(request)
    queue = get_queue(session.user.userId)
    if queue.up_next:
        next_stream = getStreamUrl(queue.step())
        # session.attributes["data"] = queue.export()
        # session.attributes["current_track"] = str(queue.current)
        save_queue(session.user.userId, queue)
        return audio('playing next').play(next_stream)
    else:
        return audio('You are all caught up with the latest in software engineering.')


@ask.intent('AMAZON.PreviousIntent')
def previous_song():
    # if session.attributes.get("data"):
    #     queue.load(session.attributes.get("data"))
    log.info(request)
    queue = get_queue(session.user.userId)
    if queue.previous:
        prev_stream = getStreamUrl(queue.step_back())
        # session.attributes["data"] = queue.export()
        # session.attributes["current_track"] = str(queue.current)
        save_queue(session.user.userId, queue)
        return audio('playing previous').play(prev_stream)

    else:
        return audio('you have just started listening. there is no going back in time.')


@ask.intent('AMAZON.StartOverIntent')
def restart_track():
    # if session.attributes.get("data"):
    #     queue.load(session.attributes.get("data"))
    log.info(request)
    queue = get_queue(session.user.userId)
    if queue.current:
        return audio('Playing the track again').play(getStreamUrl(queue.current), offset=0)
    else:
        return audio('sorry, there is nothing to start over.')


@ask.on_playback_started()
def started(offset, token, url):
    pass


@ask.on_playback_stopped()
def stopped(offset, token):
    pass


@ask.intent('AMAZON.PauseIntent')
def pause():
    # if session.attributes.get("data"):
    #    queue.load(session.attributes.get("data"))
    # seconds = current_stream.offsetInMilliseconds / 1000
    # msg = 'Paused the Playlist on track {}, offset at {} seconds'.format(
    #    queue.current_position, seconds)
    # _infodump(msg)
    # dump_stream_info()
    return audio().stop()


@ask.intent('AMAZON.ResumeIntent')
def resume():
    # if session.attributes.get("data"):
    #    queue.load(session.attributes.get("data"))
    # seconds = current_stream.offsetInMilliseconds / 1000
    # msg = 'Resuming the Playlist on track {}, offset at {} seconds'.format(queue.current_position, seconds)
    # _infodump(msg)
    # dump_stream_info()
    return audio().resume()


@ask.session_ended
def session_ended():
    return "{}", 200


def get_queue(user_id):

    queue = QueueManager([])
    queue_data = sh.get_user_queue(user_id)
    print(queue_data)
    if queue_data:
        queue.load(queue_data)

    return queue

def save_queue(user_id,queue):
    sh.update_user_queue(user_id, queue.export())

def lambda_handler(event, _context):
    return ask.run_aws_lambda(event)


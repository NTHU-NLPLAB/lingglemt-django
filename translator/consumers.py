import logging
import json
from channels.sessions import channel_session
# from translator.models import TranslateRequest
from lingglemt.linggletranslate import spg_translate_with_progress

log = logging.getLogger(__name__)


# def http_consumer(message):
#     # Decode the request from message format to a Request object
#     django_request = AsgiRequest(message)
#     # Run view
#     django_response = view(django_request)
#     # Encode the response into message format
#     for chunk in AsgiHandler.encode_response(django_response):
#         message.reply_channel.send(chunk)


@channel_session
def ws_connect(message):
    prefix = message['path'].strip('/').split('/')[0]
    if prefix != 'translate':
        log.debug('invalid ws path=%s', message['path'])
        return

    # new_request = TranslateRequest.objects.create()
    # message.channel_session['rid'] = new_request.id


@channel_session
def ws_receive(message):
    def reply_json(status, content):
        msg = {'type': status, 'content': content}
        message.reply_channel.send({'text': json.dumps(msg)})
    # Look up the room from the channel session, bailing if it doesn't exist
    # try:
    #     rid = message.channel_session['rid']
    #     request = TranslateRequest.objects.get(id=rid)
    # except KeyError:
    #     log.debug('no rid in channel_session')
    #     return
    # except TranslateRequest.DoesNotExist:
    #     log.debug('recieved message, but request does not exist rid=%s', rid)
    #     return

    data = json.loads(message['text'])
    # request.source = data['text']

    for status, content in spg_translate_with_progress(data['text']):
        # TODO: if new request comes, it should be interrupted.
        # if request.source is not data['text']:
        #     return
        reply_json(status, content)
    # request.result = content
    # try:
    #     for status, content in spg_translate(request.source):
    #         reply_json(status, content)
    #     request.result = content
    # except Exception as e:
    #     message.reply_channel.send({'text', json.dumps(e)})


@channel_session
def ws_disconnect(message):
    pass
    # try:
    #     rid = message.channel_session['rid']
    #     request = TranslateRequest.objects.get(id=rid)
    #     # request.delete()
    # except (KeyError, TranslateRequest.DoesNotExist):
    #     pass

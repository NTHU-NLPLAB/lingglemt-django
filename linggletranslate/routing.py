from translator.consumers import ws_connect, ws_receive, ws_disconnect

channel_routing = {
    # 'http.request': http_consumer,
    'websocket.connect': ws_connect,
    'websocket.receive': ws_receive,
    'websocket.disconnect': ws_disconnect,
}

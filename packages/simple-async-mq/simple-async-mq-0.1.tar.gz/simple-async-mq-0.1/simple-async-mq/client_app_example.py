from client_app import receive_msg, connect 


@receive_msg(topic='topic1')
def hej(data):
    print("TEST1:", data)

@receive_msg(topic='topic3')
def hej(data):
    print("TEST2:", data)

connect(
    host='localhost',
    port='10000',
    # topic='topic1',
    topics=[('topic1', 'json'), ('topic3', 'json')],
    output_format='json'
)

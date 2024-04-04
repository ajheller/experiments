#
# Pathological publisher
# Sends out 1,000 topics and then one random update per second
#

# Relevant docs:
#   https://pyzmq.readthedocs.io/en/latest/
#   https://zguide.zeromq.org/docs/chapter5/
#   https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/pubsub.html

import sys
import time

from random import randint

import zmq


def main(url=None):
    ctx = zmq.Context.instance()
    publisher = ctx.socket(zmq.PUB)
    if url:
        publisher.bind(url)
    else:
        publisher.bind("tcp://*:5556")
    # Ensure subscriber connection has time to complete
    time.sleep(1)

    # Send out all 1,000 topic messages
    for topic_nbr in range(50):
        publisher.send_multipart(
            [
                b"T%03d" % topic_nbr,
                b"Save Roger",
            ]
        )

    while True:
        # Send one random update per second
        try:
            time.sleep(0.1)
            publisher.send_multipart(
                [
                    b"T%03d" % randint(0, 50),
                    b"Off with his head!",
                ]
            )
        except KeyboardInterrupt:
            print("interrupted")
            break


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)

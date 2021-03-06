"""
Simple server to handle POST on localhost on optional port in Python and send email via Mailgun
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests


class Handler(BaseHTTPRequestHandler):
    """Handles POST request only to respond to WebHook calls
    """

    # noinspection PyPep8Naming
    def do_POST(self):
        """Handles POST request to respond to WebHook calls by sending an email
        """

        # TODO: this should be the request status code, but for some reason this doesn't seem to work at the end
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_length)
        self.wfile.write("Received post.".encode("utf-8"))

        # TODO: retrieve custom values from somewhere (db or config file), preferably managed via web page
        sender = "Repo Response <REPORESPONSE@DONOTREPLY.COM>"
        recipients = ['YOUR_EMAIL@EMAIL.COM']
        subject = 'webhook activated'
        # TODO: Customize the subject/body based on WebHook (through web interface?)
        body = post_body
        request = self.send_email(sender, recipients, subject, body)

    @staticmethod
    def send_email(sender, recipients, subject, body):
        """Sends an email using mailgun"""

        return requests.post(
            "YOUR_MAILGUN_DOMAIN",
            auth=("api", "YOUR_MAILGUN_KEY"),
            data={"from": sender,
                  "to": recipients,
                  "subject": subject,
                  "text": body})


def run(server=HTTPServer, handler=Handler,  httpd_port=3000):
    """
    Creates a server and handler to listen on the given port
    :param server: the HTTPServer class
    :param handler: the BaseHttpRequestHandler class
    :param httpd_port: the port to listen on
    :return: 
    """
    httpd_server_address = ('', httpd_port)
    httpd = server(httpd_server_address, handler)
    print('Starting httpd server...')
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

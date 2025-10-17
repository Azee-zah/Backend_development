from http.server import BaseHTTPRequestHandler, HTTPServer

import json

data = [
    {
        "id" : 1,
        "name" : "Olamide",
        "track": "Backend Developer"
    },

    {
        "id": 2,
        "name": "Simeon",
        "track": "AI Engineer"
    },

    {
        "id": 3,
        "name": "Adedeji",
        "track": "Front-end Developer"
    },
]

class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())



    def do_DELETE(self):
        content_size = int(self.headers.get("Content-Length", 0))
        parsed_data = self.rfile.read(content_size)
        del_data = json.loads(parsed_data)


        if data:
            data.pop(del_data)
            self.send_data({
                "Message": "deleted data",
                "Data": data
            }, status= 200)


        else:
            self.send_data({
                "Message" : "No Data to delete"
            }, status=200)


def run():
    HTTPServer(('localhost', 6005), BasicAPI).serve_forever()

print("Running apllication")
run()
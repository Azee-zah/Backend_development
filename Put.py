from http.server import BaseHTTPRequestHandler, HTTPServer

import json

data = [
    {
        "id" : 1,
        "name" : "Azeezat",
        "department": "Development"
    }
]

class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status = 201):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())


    def do_PUT(self):
        content_size = int(self.headers.get("Content-Length", 0))
        parsed_data = self.rfile.read(content_size)
        put_data = json.loads(parsed_data)

        

        if data:
            data[0].update(put_data)
            self.send_data({
            "Message": "new Data",
            "data": data
        }, status=201)
            
        else:
            self.send_data({
                "Message": "No data to update"
            }, status=201)


def run():
    HTTPServer(('localhost', 6000), BasicAPI).serve_forever()


print("Application is running")
run()

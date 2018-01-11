#!/usr/bin/python
# Copyright 2017 Google LLC. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import SocketServer
import multiprocessing
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import subprocess
import matplotlib
matplotlib.use("Agg")
from pylab import *
from numpy import NaN
from io import BytesIO


class MyHandler(BaseHTTPRequestHandler):
  """ HTTP request Handler that will generate a Mandelbrot set on each request to
  root path (/). Request to /health-check receives an instant 200 OK response.
  """

  # create an array for X and Y values
  X = arange(-2, .5, .02)
  Y = arange(-1, 1, .02)
  # create an array for results
  results = zeros((len(Y), len(X)))

  def m(self, a):
    """ calculate Mandelbrot function

        Keyword arguments:
        a -- the complex number for which the function should be executed
    """
    z = 0
    for n in range(1, 100):
      z = z**2 + a
      if abs(z) > 2:
        return n
    return NaN

  def do_GET(self):
    """ Respond to HTTP GET requests"""

    # When root is requested, calculate Mandelbrot on request
    if self.path == "/":
      # Calculate each pixel of the image
      for ix, x in enumerate(self.X):
        for iy, y in enumerate(self.Y):
          self.results[iy, ix] = self.m(x + 1j * y)
      # Save image from array as PNG with pyplot
      imshow(
          self.results,
          cmap=plt.cm.prism,
          interpolation="none",
          extent=(self.X.min(), self.X.max(), self.Y.min(), self.Y.max()))
      xlabel("Re(c)")
      ylabel("Im(c)")
      with BytesIO() as buffer:
        savefig(buffer, format="png")
        #send image as response
        self.send_response(200)
        self.send_header("Content-Type", "image/png")
      self.end_headers()
      self.wfile.write(buffer.getvalue())
    # On health check send an empty response
    elif self.path == "/health-check":
      self.send_response(200)
    # All other paths send a 404
    else:
      self.send_response(404)


class ThreadedHTTPServer(SocketServer.ForkingMixIn, HTTPServer):
  """ Have a HTTP Server forking to different threads """
  pass


# Start web server when script is started
if __name__ == "__main__":
  try:
    server = ThreadedHTTPServer(("", 80), MyHandler)
    print "Started httpserver on port 80"
    # Wait forever for incoming http requests
    server.serve_forever()
  except KeyboardInterrupt:
    print "^C received, shutting down the web server"
    server.socket.close()

# Optimizing Application Capacity with Global Load Balancing

This is a repository with sample code to go along with the tutorial at
https://cloud.google.com/solutions/capacity-management-with-load-balancing
and is provided for reference. It is not intended to be used in production, but
to serve as a learning tool and starting point for testing application capacity
in GCE.

## Prerequisites
- The tutorial assumes you are familiar with Google Compute Engine.
  The Python code provided requires Python 2 and the NumPy (www.numpy.org)
  and Matplotlib (https://matplotlib.org) libraries which are installed
  on all VMs by using the tutorial.

## Components

### Webserver script

This tutorial includes a webserver.py script which runs a simple Threaded
HTTP Server that calculates and displays a standard Mandelbrot set when
a request comes in to the root (/) path.

This is to simulate a complex CPU bound workload which is performance
tested in a single instance, single region load balanced and multi region
load balanced configuration during the tutorial.

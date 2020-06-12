# mlapi

This is a fork of [pliablepixels' mlapi project](https://github.com/pliablepixels/mlapi).  This fork adds the following functionality: 

1) Converts the application to WSGI application (NGINX + Gunicorn + Flask)
2) Extends the multithreading capabilities for both CPU and GPU workloads
3) Adds containerization (Podman and Docker)

In the future I'll enhance this to run on both Kubernetes and OpenShift via Helm Charts.  

## What

An WSGI API gateway that you can install in your own server to do object, face and gender recognition.
Easy to extend to many/any other model. You can pass images as:

- a local file
- remote url

This can also be used as a remote face/recognition and object recognition server if you are using the ZoneMinder Event Server! (docs upcoming)

This is an example of invoking `python ./stream.py video.mp4` ([video courtesy of pexels](https://www.pexels.com/video/people-walking-by-on-a-sidewalk-854100/))

<img src="https://media.giphy.com/media/YQ4f1xXHMaDLF7AZMe/giphy.gif"/>

## Why

Wanted to learn how to write an API gateway easily. Object detection was a good use-case since I use it extensively for other things (like my event server). This is the first time I've used flask/jwt/tinydb etc. so its very likely there are improvements that can be made. Feel free to PR.

## Tip of the Hat

A tip of the hat to [Adrian Rosebrock](https://www.pyimagesearch.com/about/) to get me started. His articles are great.

## Install

### The Simple Way

- It's best to create a virtual environment with python3, but not mandatory
- You need python3 for this to run
- face recognition requires cmake/gcc/standard linux dev libraries installed (if you have gcc, you likely have everything else. You may need to install cmake on top of it if you don't already have it)

Then:

```shell
 git clone https://github.com/themoosman/mlapi
 cd mlapi
 sudo -H pip3 install -r requirements.txt
 ```

Note: You may need other typical ml support libs. Forgot which. Feel free to PR and extend requirements.txt

Note that this package also needs OpenCV which is not installed by the above step by default. This is because you may have a GPU and may want to use GPU support. If not, pip is fine. See [this page](https://zmeventnotification.readthedocs.io/en/latest/guides/hooks.html#opencv-install) on how to install OpenCV


### The Podman/Docker Way

This is only necessary if you which to run the containers individually.  This [section](#nginx-and-gunicorn) outlines how to use `docker-compose` to build and run the containers.  

The mlapi Dockerfile handles installing the OpenCV (currently 4.3.0) framework in Ubuntu 20.04.  Currently this image will run as root, but there is an open issue to remove that limitation.  

#### Building

##### Podman

```shell
# No sudo necessary :)
cd nginx
podman build -t mlapi-nginx:latest .
cd ../mlapi
podman build -t mlapi-app:latest .
```

##### Docker

```shell
cd nginx
sudo docker build -t mlapi-nginx:latest .
cd ../mlapi
sudo docker build -t mlapi-app:latest .
```

## Running

### The Easy Way

This method just executes the Gunicorn server to serve up the mlapi Flask application.

To run just the Gunicorn server and application:

```shell
cd mlapi
gunicorn mlapi:app
```

This will use the default values from `mlapiconfig.ini` and `gunicorn.conf.py` and will listen on port `5000`.

### The Real Way

The "real" way includes an NGINX reverse proxy into the Gunicorn server.  NGINX configs are included, but you'll need a working NGINX environment.  Setup of NGINX is outside of this document.  An NGINX Dockerfile is included.

Run the Gunicorn server and application:

```shell
cd mlapi
gunicorn mlapi:app
```

Run NGINX

```shell
# You're on your own.
```

Run Gunicorn

```shell
cd mlapi
gunicorn mlapi:app
```

### The Podman/Docker Way

#### NGINX and Gunicorn

A Docker compose file is included to run both the NGINX and mlapi containers.  The Docker or Podman compose will build the images and launch the containers in a linked fashion.  

##### Podman

```shell
pip3 install podman-compose --user
podman-compose up
```

##### Docker

```shell
sudo docker-compose up
```

To test it out:

```shell
curl -v http://localhost:8080/api/v1/health
```

#### Only Gunicorn

You can just run Gunicorn container without the reverse proxy (NGINX).

##### Podman

```shell
podman run -it --rm -p 5000:5000 mlapi-app
```

##### Docker

```shell
docker run -it --rm -p 5000:5000 mlapi-app
```

To test it out:

```shell
curl -v http://localhost:5000/api/v1/health
```

## Detection

To invoke detection, you need to:

Server Side:

- Make sure the username and password are created. Use `python3 mlapi_adduser.py` for that

Client Side:

(General note: I use [httpie](https://httpie.org) for command line http requests. cURL, while powerful has too many quirks/oddities. That being said, given curl is everywhere, examples are in curl. See later for a programmatic way)

- Get an access token

```shell
curl -H "Content-Type:application/json" -XPOST -d '{"username":"<user>", "password":"<password>"}' "http://localhost:5000/api/v1/login"
```

This will return a JSON object like:

```json
{"access_token":"eyJ0eX<many more characters>","expires":3600}
```

Now use that token like so:

```shell
export ACCESS_TOKEN=<that access token>
```

Object detection for a remote image (via url):

```shell
curl -H "Content-Type:application/json" -H "Authorization: Bearer ${ACCESS_TOKEN}" -XPOST -d "{\"url\":\"https://upload.wikimedia.org/wikipedia/commons/c/c4/Anna%27s_hummingbird.jpg\"}" http://localhost:5000/api/v1/detect/object
```

returns:

```json
[{"type": "bird", "confidence": "99.98%", "box": [433, 466, 2441, 1660]}]
```

Object detection for a local image:

```shell
curl  -H "Authorization: Bearer ${ACCESS_TOKEN}" -XPOST -F"file=@IMG_1833.JPG" http://localhost:5000/api/v1/detect/object -v
```

returns:

```json
[{"type": "person", "confidence": "99.77%", "box": [2034, 1076, 3030, 2344]}, {"type": "person", "confidence": "97.70%", "box": [463, 519, 1657, 1351]}, {"type": "cup", "confidence": "97.42%", "box": [1642, 978, 1780, 1198]}, {"type": "dining table", "confidence": "95.78%", "box": [636, 1088, 2370, 2262]}, {"type": "person", "confidence": "94.44%", "box": [22, 718, 640, 2292]}, {"type": "person", "confidence": "93.08%", "box": [408, 1002, 1254, 2016]}, {"type": "cup", "confidence": "92.57%", "box":[1918, 1272, 2110, 1518]}, {"type": "cup", "confidence": "90.04%", "box": [1384, 1768, 1564, 2044]}, {"type": "bowl", "confidence": "83.41%", "box": [882, 1760, 1134, 2024]}, {"type": "person", "confidence": "82.64%", "box": [2112, 984, 2508, 1946]}, {"type": "cup", "confidence": "50.14%", "box": [1854, 1520, 2072, 1752]}]
```

Face detection for the same image above:

```shell
curl  -H "Authorization: Bearer ${ACCESS_TOKEN}" -XPOST -F"file=@IMG_1833.JPG" "http://localhost:5000/api/v1/detect/object?type=face"
```

returns:

```json
[{"type": "face", "confidence": "52.87%", "box": [904, 1037, 1199, 1337]}]
```

Object detection on a live Zoneminder feed:
(Note that ampersands have to be escaped as `%26` when passed as a data parameter)

```shell
curl -XPOST  "http://localhost:5000/api/v1/detect/object?delete=false" -d "url=https://demo.zoneminder.com/cgi-bin-zm/nph-zms?mode=single%26maxfps=5%26buffer=1000%26monitor=18%26user=zmuser%26pass=zmpass"
-H "Authorization: Bearer ${ACCESS_TOKEN}"
```

returns

```json
[{"type": "bear", "confidence": "99.40%", "box": [6, 184, 352, 436]}, {"type": "bear
", "confidence": "72.66%", "box": [615, 219, 659, 279]}]
```

## Live Streams or Recorded Video files

This is an image based object detection API. If you want to pass a video file or live stream,
take a look at the full example below.

## Full Example

Take a look at [stream.py](https://github.com/pliablepixels/mlapi/blob/master/examples/stream.py). This program reads any media source and/or webcam and invokes detection via the API gateway

## Other Notes

- The first time you invoke a query, the ML engine inside will download weights/models and will take time. That will only happen once and from then on, it will be much faster
- Note that the server stores the images and the objects detected inside its `images/` folder. If you want the server to delete them after analysis add `&delete=true` to the query parameters.
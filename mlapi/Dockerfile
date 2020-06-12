FROM ubuntu:20.04

ENV OPEN_CV_VERSION=4.3.0
ENV MAKE_THREADS=12
ENV APP_DIR=/app

#Install all the build dependencies, OpenCV source and then build it.
#TODO Make this a multi staged build.
RUN apt update && DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends wget git ffmpeg build-essential cmake unzip pkg-config \
    libjpeg-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev \
    libatlas-base-dev gfortran python3-dev python3-pip ca-certificates && \
pip3 install numpy && \
apt-get clean autoclean && \
apt-get autoremove --yes && \
rm -rf /var/lib/{apt,dpkg,cache,log}/ && \
cd ~  && \
wget -O opencv.zip https://github.com/opencv/opencv/archive/${OPEN_CV_VERSION}.zip && \
unzip opencv.zip && \
rm opencv.zip && \
mv opencv-${OPEN_CV_VERSION} opencv && \
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/${OPEN_CV_VERSION}.zip && \
unzip opencv_contrib.zip && \
rm opencv_contrib.zip && \
mv opencv_contrib-${OPEN_CV_VERSION} opencv_contrib && \
cd ~/opencv && \
mkdir build && \
cd build && \
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D INSTALL_C_EXAMPLES=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D WITH_CUDA=OFF \
    -D WITH_CUDNN=ON \
    -D OPENCV_DNN_CUDA=OFF \
    -D ENABLE_FAST_MATH=0 \
    -D CUDA_FAST_MATH=0 \
    -D WITH_CUBLAS=0 \
    -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
    -D HAVE_opencv_python3=ON \
    -D PYTHON_EXECUTABLE=$(which python3) \
    -D BUILD_EXAMPLES=OFF \
    -D BUILD_OPENCV_JAVA=OFF \
    -D CMAKE_INSTALL_PREFIX=$(python3 -c "import sys; print(sys.prefix)") \
    -D PYTHON_INCLUDE_DIR=$(python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())")  \
    -D PYTHON_PACKAGES_PATH=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")  \
    ../ && \
make -j${MAKE_THREADS} && \
make install && \
ldconfig && \
rm -rf ~/opencv && \
rm -rf ~/opencv_contrib && \
mkdir -p ${APP_DIR} && \
chmod 777 ${APP_DIR}

#Set the workdir
WORKDIR ${APP_DIR}

#Add all the Python source
ADD . / .

#Adding this is a seperate RUN, so adding new code won't require another download of these files.
RUN mkdir -p /app/models/yolov3 && \
cd /app/models/yolov3 && \
wget https://pjreddie.com/media/files/yolov3-tiny.weights && \
wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3-tiny.cfg && \
wget https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names && \
wget https://pjreddie.com/media/files/yolov3.weights && \
wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg

#Run the last few pip3 statement.  Some of these could be moved up, but this works for now.
RUN pip3 install -r requirements.txt && \
apt install -y libopenblas-dev liblapack-dev libblas-dev && \
pip3 install face_recognition && \
apt-get clean autoclean && \
apt-get autoremove --yes && \
rm -rf /var/lib/{apt,dpkg,cache,log}/ 

#Leaving this here for Kubernetes/OpenShift
#USER 1001

#Run the darn thing already.
CMD gunicorn mlapi:app
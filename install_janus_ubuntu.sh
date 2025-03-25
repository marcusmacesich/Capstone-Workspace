#The file may need sudo chmod -x install_janus_ubuntu.sh run on it before it can be run
#Run the file with sh install_janus_ubuntu.sh
sudo apt update
sudo apt install -y autoconf automake m4 libtool build-essential

sudo apt install -y libmicrohttpd-dev libjansson-dev \
	libssl-dev libsofia-sip-ua-dev libglib2.0-dev \
	libopus-dev libogg-dev libcurl4-openssl-dev liblua5.3-dev \
	libconfig-dev pkg-config zlib1g-dev libusrsctp-dev libwebsockets-dev \
    libsrtp2-dev aptitude

#The janus documentation say to do it this way rather than apt install
#The other way is to use sudo apt install libnice-dev
git clone https://gitlab.freedesktop.org/libnice/libnice
cd libnice
meson --prefix=/usr build && ninja -C build && sudo ninja -C build install

sudo aptitude install doxygen graphviz

git clone https://github.com/meetecho/janus-gateway.git
cd janus-gateway
sh autogen.sh
./configure --prefix=/opt/janus --enable-docs
make
make install

sudo apt update
sudo apt install -y autoconf automake m4 libtool build-essential

sudo apt install -y libmicrohttpd-dev libjansson-dev \
	libssl-dev libsofia-sip-ua-dev libglib2.0-dev \
	libopus-dev libogg-dev libcurl4-openssl-dev liblua5.3-dev \
	libconfig-dev pkg-config zlib1g-dev libusrsctp-dev libwebsockets-dev \
    aptitude

sudo aptitude install doxygen graphviz

git clone https://github.com/meetecho/janus-gateway.git
cd janus-gateway
sh autogen.sh
./configure --prefix=/opt/janus --enable-docs
make
make install
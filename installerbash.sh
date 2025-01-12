#packages needed for janus: jansson libnice openssl srtp libusrsctp libmicrohttpd libwebsockets cmake rabbitmq-c sofia-sip opus libogg curl glib libconfig pkg-config autoconf automake libtool zlib libpaho-mqtt nanomsg lua duktape doxygen graphviz
#Also installs python and pip
#export CFLAGS="$CFLAGS -I/opt/homebrew/Cellar/libnice/0.1.22/include -I/opt/homebrew/anaconda3/bin/openssl/include"
#export LDFLAGS="$LDFLAGS -L/opt/homebrew/Cellar/libnice/0.1.22/lib -I/opt/homebrew/anaconda3/bin/opeenssl/lib"   
#export CFLAGS="$CFLAGS -I/opt/homebrew/anaconda3/bin/openssl/include"
#export LDFLAGS="$LDFLAGS -I/opt/homebrew/anaconda3/bin/opeenssl/lib" 
#./configure --prefix=/usr/local --enable-websockets --enable-data-channels
#make
#sudo make install
#sudo systemctl restart janus

PKG_MANAGER=""
if command -v brew > /dev/null; then
    PKG_MANAGER="brew"
    if command -v python > /dev/null; then
        echo "installing python"
        $PKG_MANAGER install python
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3 get-pip.py
    fi
    if $PKG_MANAGER --prefix zlib > /dev/null; then
        echo "installing zlib"
        $PKG_MANAGER install zlib
    fi

    if $PKG_MANAGER --prefix libpaho-mqtt > /dev/null; then
        echo "installing libpaho-mqtt"
        $PKG_MANAGER install libpaho-mqtt
    fi

    if $PKG_MANAGER --prefix nanomsg > /dev/null; then
        echo "installing nanomsg"
        $PKG_MANAGER install nanomsg
    fi

    if $PKG_MANAGER --prefix lua > /dev/null; then
        echo "installing lua"
        $PKG_MANAGER install lua
    fi

    if $PKG_MANAGER --prefix duktape > /dev/null; then
        echo "installing duktape"
        $PKG_MANAGER install duktape
    fi

    if $PKG_MANAGER --prefix doxygen > /dev/null; then
        echo "installing doxygen"
        $PKG_MANAGER install doxygen
    fi

    if $PKG_MANAGER --prefix graphviz > /dev/null; then
        echo "installing graphviz"
        $PKG_MANAGER install graphviz
    fi

    if $PKG_MANAGER --prefix jansson > /dev/null; then
        echo "installing jansson"
        $PKG_MANAGER install jansson
    fi

    if $PKG_MANAGER --prefix libnice > /dev/null; then
        echo "installing libnice"
        $PKG_MANAGER install libnice
    fi

    if $PKG_MANAGER --prefix openssl > /dev/null; then
        echo "installing openssl"
        $PKG_MANAGER install openssl
    fi

    if $PKG_MANAGER --prefix srtp > /dev/null; then
        echo "installing srtp"
        $PKG_MANAGER install srtp
    fi

    if $PKG_MANAGER --prefix libusrsctp > /dev/null; then
        echo "installing libusrsctp"
        $PKG_MANAGER install libusrsctp
    fi

    if $PKG_MANAGER --prefix libmicrohttpd > /dev/null; then
        echo "installing libmicrohttpd"
        $PKG_MANAGER install libmicrohttpd
    fi

    if $PKG_MANAGER --prefix libwebsockets > /dev/null; then
        echo "installing libwebsockets"
        $PKG_MANAGER install libwebsockets
    fi

    if $PKG_MANAGER --prefix cmake > /dev/null; then
        echo "installing cmake"
        $PKG_MANAGER install cmake
    fi

    if $PKG_MANAGER --prefix rabbitmq-c > /dev/null; then
        echo "installing rabbitmq-c"
        $PKG_MANAGER install rabbitmq-c
    fi

    if $PKG_MANAGER --prefix sofia-sip > /dev/null; then
        echo "installing sofia-sip"
        $PKG_MANAGER install sofia-sip
    fi

    if $PKG_MANAGER --prefix opus > /dev/null; then
        echo "installing opus"
        $PKG_MANAGER install opus
    fi

    if $PKG_MANAGER --prefix libogg > /dev/null; then
        echo "installing libogg"
        $PKG_MANAGER install libogg
    fi

    if $PKG_MANAGER --prefix curl > /dev/null; then
        echo "installing curl"
        $PKG_MANAGER install curl
    fi

    if $PKG_MANAGER --prefix glib > /dev/null; then
        echo "installing glib"
        $PKG_MANAGER install glib
    fi

    if $PKG_MANAGER --prefix libconfig > /dev/null; then
        echo "installing libconfig"
        $PKG_MANAGER install libconfig
    fi

    if $PKG_MANAGER --prefix pkg-config > /dev/null; then
        echo "installing pkg-config"
        $PKG_MANAGER install pkg-config
    fi

    if $PKG_MANAGER --prefix autoconf > /dev/null; then
        echo "installing autoconf"
        $PKG_MANAGER install autoconf
    fi

    if $PKG_MANAGER --prefix automake > /dev/null; then
        echo "installing automake"
        $PKG_MANAGER install automake
    fi

    if $PKG_MANAGER --prefix libtool > /dev/null; then
        echo "installing libtool"
        $PKG_MANAGER install libtool
    fi

    if command -v janus > /dev/null; then
        echo "installing janus"
        git clone https://github.com/meetecho/janus-gateway.git
        cd janus-gateway
        sudo sh autogen.sh
        export LDFLAGS="$LDFLAGS -L/opt/homebrew/opt/libnice/lib -I/opt/homebrew/opt/opeenssl/lib"                                                                                                                                                                           
        export CFLAGS="$CFLAGS -I/opt/homebrew/opt/libnice/include -I/opt/homebrew/opt/openssl/include"
        sudo ./configure --prefix=/opt/janus --enable-docs
        sudo make
        sudo make install
        sudo make configs
    fi
    
elif command -v apt > /dev/null; then
    PKG_MANAGER="apt"
    sudo apt update
    sudo apt upgrade
    if command -v python > /dev/null; then
        echo "Installing python"
        sudo apt install python3
        sudo apt install python3-pip
    fi 
    if command -v glib > /dev/null; then
        echo "Installing GLib"
        sudo $PKG_MANAGER install libglib2.0-dev
    fi

    if command -v zlib > /dev/null; then
        echo "Installing zlib"
        sudo $PKG_MANAGER install zlib zlib1g-dev
    fi

    if command -v pkg-config > /dev/null; then
        echo "Installing pkg-config"
        sudo $PKG_MANAGER install pkg-config
    fi

    if command -v jansson > /dev/null; then
        echo "Installing Jansson"
        sudo $PKG_MANAGER install libjansson-dev
    fi

    if command -v libconfig > /dev/null; then
        echo "Installing libconfig"
        sudo $PKG_MANAGER install libconfig-dev
    fi

    if command -v libnice > /dev/null; then
        echo "Installing libnice"
        sudo $PKG_MANAGER install libnice-dev
    fi

    if command -v openssl > /dev/null; then
        echo "Installing OpenSSL"
        sudo $PKG_MANAGER install libssl-dev
    fi

    if command -v libsrtp > /dev/null; then
        echo "Installing libsrtp"
        sudo $PKG_MANAGER install libsrtp2-dev
    fi

    if command -v usrsctp > /dev/null; then
        echo "Installing usrsctp"
        sudo $PKG_MANAGER install libusrsctp-dev
    fi

    if command -v libmicrohttpd > /dev/null; then
        echo "Installing libmicrohttpd"
        sudo $PKG_MANAGER install libmicrohttpd-dev
    fi

    if command -v libwebsockets > /dev/null; then
        echo "Installing libwebsockets"
        sudo $PKG_MANAGER install libwebsockets-dev
    fi

    if command -v cmake > /dev/null; then
        echo "Installing cmake"
        sudo $PKG_MANAGER install cmake
    fi

    if command -v automake > /dev/null; then
        echo "Installing automake"
        sudo $PKG_MANAGER install automake
    fi

    if command -v rabbitmq-c > /dev/null; then
        echo "Installing rabbitmq-c"
        sudo $PKG_MANAGER install librabbitmq-dev
    fi

    if command -v paho.mqtt.c > /dev/null; then
        echo "Installing paho.mqtt.c"
        sudo $PKG_MANAGER install libpaho-mqtt-dev
    fi

    if command -v nanomsg > /dev/null; then
        echo "Installing nanomsg"
        sudo $PKG_MANAGER install libnanomsg-dev
    fi

    if command -v curl > /dev/null; then
        echo "Installing libcurl"
        sudo $PKG_MANAGER install curl libcurl4-openssl-dev
    fi

    if command -v libtool > /dev/null; then
        echo "Installing libtool"
        sudo $PKG_MANAGER install libtool
    fi

    if command -v sofia-sip > /dev/null; then
        echo "Installing Sofia-SIP"
        sudo $PKG_MANAGER install libsofia-sip-ua-dev
    fi

    if command -v libopus > /dev/null; then
        echo "Installing libopus"
        sudo $PKG_MANAGER install libopus-dev
    fi

    if command -v libogg > /dev/null; then
        echo "Installing libogg"
        sudo $PKG_MANAGER install libogg-dev
    fi

    if command -v lua > /dev/null; then
        echo "Installing Lua"
        sudo $PKG_MANAGER install liblua5.3-dev
    fi

    if command -v duktape > /dev/null; then
        echo "Installing Duktape"
        sudo $PKG_MANAGER install duktape-dev duktape
    fi

    if command -v doxygen > /dev/null; then
        echo "Installing Doxygen"
        sudo $PKG_MANAGER install doxygen
    fi

    if command -v graphviz > /dev/null; then
        echo "Installing Graphviz"
        sudo $PKG_MANAGER install graphviz
    fi
    git clone https://github.com/meetecho/janus-gateway.git
    cd janus-gateway
    sudo sh autogen.sh
    sudo ./configure --prefix=/opt/janus --enable-docs
    sudo make
    sudo make install
    make configs
elif command -v dnf > /dev/null; then
    PKG_MANAGER="dnf"
    echo "Package manager not supported yet."
elif command -v yum > /dev/null; then
    PKG_MANAGER="yum"
    echo "Package manager not supported yet."
elif command -v pacman > /dev/null; then
    PKG_MANAGER="pacman"
    echo "Package manager not supported yet."
elif command -v zypper > /dev/null; then
    PKG_MANAGER="zypper"
    echo "Package manager not supported yet."
else
    echo "No compatible package manager found."
    exit 1
fi








#GLib
#libglib2.0-dev
#
#zlib
#zlib1g-dev
#
#pkg-config
#pkg-config
#
#Jansson
#libjansson-dev
#
#libconfig
#libconfig-dev
#
#libnice
#libnice-dev
#
#OpenSSL
#libssl-dev
#
#libsrtp
#libsrtp2-dev
#
#usrsctp
#libusrsctp-dev
#
#libmicrohttpd 
#libmicrohttpd-dev
#
#libwebsockets 
#libwebsockets-dev
#
#cmake
#cmake
#automake
#
#rabbitmq-c
#librabbitmq-dev 
#
#paho.mqtt.c
#libpaho-mqtt-dev
#
#nanomsg
#libnanomsg-dev
#
#libcurl
#curl
#libcurl4-openssl-dev
#
#libtool
#libtool
#
#Sofia-SIP
#libsofia-sip-ua-dev
#
#libopus
#libopus-dev
#
#libogg
#libogg-dev
#
#Lua
#liblua5.3-dev
#
#Duktape
#duktape-dev
#duktape
#
#Doxygen
#doxygen
#
#Graphviz
#graphviz
#    if command -v [package] > /dev/null; then
#        echo "Installing [Package]"
#        sudo PKG_MANAGER install [packageI]
#    fi

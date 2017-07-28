#!/bin/sh
unamestr=`uname`
if [[ "$unamestr" == "SunOS" ]]; then
	PATH=/opt/csw/bin:/opt/jdk/bin:$PATH
fi

{
	wget --no-check-certificate https://s3.amazonaws.com/unidata-tds/tdsConfig/thredds/config.zip -O config.zip
	jar xf config.zip
	exit
}

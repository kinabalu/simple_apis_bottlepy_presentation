# base image
#
FROM                    mystic/baseimage
MAINTAINER              Mystic Coders, LLC

#
# *** OS-level packages ***
#

RUN                     apt-get -y update && apt-get install -y \
                        nginx

#
# Configure nginx
#

# RUN                      mkdir /var/www
#ADD                     default /etc/nginx/sites-available/default

# RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD                     default /etc/nginx/sites-available/
RUN                     echo "daemon off;" >> /etc/nginx/nginx.conf

ADD                     nginx.sh /usr/local/bin/
RUN                     chmod +x /usr/local/bin/nginx.sh

EXPOSE 80

CMD                     ["/usr/local/bin/nginx.sh"]


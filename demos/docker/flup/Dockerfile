FROM                    mystic/baseimage
MAINTAINER              Mystic Coders, LLC


RUN                     apt-get update && apt-get install -y \
                        python \
                        python-pip && \
                        pip install \
                        bottle \
                        flup \
                        mongoengine

ADD                     app.py  /var/www/

EXPOSE                  8000

WORKDIR                 /var/www

ADD                     start-stocks.sh /usr/local/bin/
RUN                     chmod +x /usr/local/bin/start-stocks.sh

CMD                     ["/usr/local/bin/start-stocks.sh"]

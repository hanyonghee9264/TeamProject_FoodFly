FROM            hanyonghee9264/foodfly:base
ENV             DJANGO_SETTINGS_MODULE config.settings.production


COPY            ./  /srv/project
WORKDIR         /srv/project

WORKDIR         /srv/project/app

RUN         rm -rf  /etc/nginx/sites-available/* && \
            rm -rf  /etc/nginx/sites-enabled/* && \
            cp -f   /srv/project/.config/app.nginx \
                    /etc/nginx/sites-available/ && \
            ln -sf  /etc/nginx/sites-available/app.nginx \
                    /etc/nginx/sites-enabled/app.nginx

# supervisor설정파일 복사
RUN         cp -f   /srv/project/.config/supervisord.conf \
                    /etc/supervisor/conf.d/

# 80번 포트 개방
EXPOSE      80

# Command로 supervisor실행
CMD         supervisord -n


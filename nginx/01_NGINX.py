
# https://docs.nginx.com/nginx/admin-guide/basic-functionality/

# ==============================================================================================================================
# CONFIG
# ==============================================================================================================================
/etc/nginx/nginx.conf             # конфиг nginx
/var/run/nginx.pid                # pid 

http {
    upstream backend {
        server backend1.example.com weight=5;
        server backend2.example.com;
        server 192.0.0.1 backup;
    }
}

# ==============================================================================================================================
# CACHE, Gzip
# ==============================================================================================================================
# кешировать нужно статику
# немнужно кешировать админку и запросы POST 

# в location скажет браузеру кешировать страницу на месяц
expires 1M;   

# в server https://www.youtube.com/watch?v=Z24wGMmsH4Q&list=PLhgRAQ8BwWFa7ulOkX0qi5UfVizGD_-Rc&index=17
gzip on;

# ==============================================================================================================================
# LOGGING
# ==============================================================================================================================
# настройки логов могут быть определены глобально, на уровне, сервера и location.
# логирование статики обычно отключают

# ===== add in nginx.conf

log_format upstream_time '$remote_addr - $remote_user [$time_local] '
                          '"$request" $status $body_bytes_sent '
                          '"$http_referer" "$http_user_agent"'
                          'rt=$request_time uct="$upstream_connect_time" uht="$upstream_header_time" urt="$upstream_response_time"';

# свои пути можно назначить так
error_log nginx/log/error.log warn;
access_log nginx/log/access.log upstream_time;

# отключить логи
error_log off;
access_log off;

# пути логов по умолчанию
/var/log/nginx/error.log          
/var/log/nginx/access.log      


# ==============================================================================================================================
# NGINX CMD
# ==============================================================================================================================

# команды для дистрибутива без systemd (для docker)
sudo service start nginx
sudo service stop nginx
sudo service restart nginx
sudo service nginx reload         # мягкий перезапуск сервера с downtime=0
sudo service nginx enable
sudo service nginx configtest

# {start|stop|status|restart|reload|force-reload|upgrade|configtest|check-reload}

# команды для дистрибутива с systemd
sudo systemctl start nginx    
sudo systemctl stop nginx         
sudo systemctl restart nginx
sudo systemctl enable nginx       # включить запуск при загрузке системы
sudo systemctl status nginx


sudo nginx -h
sudo nginx -s reload              # мягкий перезапуск
sudo nginx -s start
sudo nginx -s stop
sudo nginx -s reopen
sudo nginx -s quit


sudo nginx -v                     # версия nginx
sudo nginx -V                     # версия nginx с параметром настройки
sudo nginx -t                     # проверка валидности конфига
sudo nginx -T                     # проверка валидности конфига               


# ==============================================================================================================================
# NGINX IN DOCKER
# ==============================================================================================================================
# https://hub.docker.com/_/nginx

# ===== DOCKERFILE

FROM nginx:latest

# удаляем дефолтный конфиг в контейнере и добавляем свой
RUN rm /etc/nginx/conf.d/default.conf
ADD nginx.conf /etc/nginx/conf.d



# ==============================================================================================================================
# NGINX БЕЗ DOWNTIME (HOT RELOAD) 
# ==============================================================================================================================

# 1. ПРОВЕРКА НОВОГО КОНФИГА ПЕРЕД ЗАПУСКОМ (синаксис + работоспособность)
sudo nginx -t

# 2. ПЕРЕЗАПУСК СЕРВЕРА
sudo service nginx reload
# nginx дождется завершения текущих процессов
# перезагрузит сервер так чтобы downtime=0


# ==============================================================================================================================
# ПОЛУЧЕНИЕ И НАСТРОЙКА LetsEncrypt SSL СЕРТИФИКАТА 
# ==============================================================================================================================
# https://letsencrypt.org/ru/                     
# https://losst.ru/kak-poluchit-sertifikat-let-s-encrypt


=== Для чего нужен SSL
# шифрование трафика между браузером и сервером(невозможность расшифровки в слуае перехвата при Man in the middle)
# ssl любят поисковики
# доступ к геолокации требует наличия https


=== ПОЛУЧЕНИЕ SSL
# Установка сертификата присходит через утилиту https://certbot.eff.org/

# 1. выбирать nginx и ОС

# 2. установить certbot на машину с nginx
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot

# 3. Получение сертификата
sudo certbot certonly --nginx
# эта команда получит сертификат и далее требует ручной настройки конфига nginx

sudo certbot --nginx
# эта команда получит сертификат в интерактивном режиме и выполнит настройку конфига сама
# выбрать домен(ы) для которого нужен сертификат(утилита прочитает конфиг nginx и выведет список доступных доменов)
# нужно указать цифрами 1 или несколько доменов через запятую
# указать email - будут приходить уведомления о необходимости продления
# утилита спросит нужно ли перенаправлять http-трафик на https
# далее происходит получение и настройка сертификата
# сертификат будет сохранён в /etc/letsencrypt/live/имя_домена/

# 4. автопродение сертификата
sudo certbot certonly --nginx -n -d test.losst.ru -d www.test.losst.ru       # обновление сертификата на выбранные домены
sudo certbot renew                                                           # обновить сертификаты для всех доменов одной командной
sudo certbot renew --dry-run                                                 # тест автообновления без записи результата на диск

# обновление по крону раз в неделю
crontab -e
0 0 * * 0 /usr/bin/certbot certonly --nginx -n -d test.losst.ru -d www.test.losst.ru


=== ПОЛУЧЕНИЕ WILDCARD LetsEncrypt
# позволяют использовать один сертификат для всех поддоменов определённого домена
# надо будет подтвердить, что домен принадлежит именно вам - надо добавить TXT-запись к зоне домена.

# команда для генерации WILDCARD сертификата выглядит так
sudo certbot certonly --agree-tos -d test.losst.ru -d *.test.losst.ru --preferred-challenges dns --manual --server https://acme-v02.api.letsencrypt.org/directory
# надо разрешить публикацию вашего IP-адреса
# добавить TXT-запись с именем и значением к вашей доменной зоне. В моем случае это  _acme-challenge.test.losst.ru со специальным хэшем
# на обновление доменной зоны уйдет несколько часов.


# ==============================================================================================================================
# NGINX Monitoring Amplify
# ==============================================================================================================================
# https://amplify.nginx.com/signup/















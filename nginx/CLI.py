# ==============================================================================================================================
# NGINX CLI
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


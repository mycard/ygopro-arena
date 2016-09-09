FROM php:fpm

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

#RUN curl https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

RUN apt-get update
RUN apt-get install -y zlib1g-dev libpq-dev

RUN docker-php-ext-install zip pgsql

#COPY composer.json /usr/src/app/
#COPY composer.lock /usr/src/app/ 

#RUN composer install 
COPY . /usr/src/app 

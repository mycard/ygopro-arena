FROM php:fpm

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

#RUN curl https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

RUN apt-get update
RUN apt-get install -y libpq-dev

RUN docker-php-ext-install pgsql pdo_pgsql

#COPY composer.json /usr/src/app/
#COPY composer.lock /usr/src/app/ 

#RUN composer install 
COPY . /usr/src/app 

RUN mkdir Application/Runtime
RUN chmod 777 Application/Runtime
RUN chmod 777 Application

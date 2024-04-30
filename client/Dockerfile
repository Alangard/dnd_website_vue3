# base image
FROM node:alpine

# set working directory
WORKDIR /code/client/


# install and cache app dependencies
COPY package.json  package-lock.json /code/
RUN npm install
RUN npm install -g @vue/cli

COPY . /code/
# base image
FROM node:alpine

# set working directory
WORKDIR /code/client/

# install and cache app dependencies
COPY ./client/package.json  ./client/package-lock.json /code/client/
RUN npm install
RUN npm install -g @vue/cli

COPY ./client /code/client/


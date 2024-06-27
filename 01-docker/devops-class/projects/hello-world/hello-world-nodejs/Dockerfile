FROM node:8.16.1-alpine
WORKDIR /app
# first copy the dependency as a separate layer (which doesn't change a lot)
COPY package.json /app
RUN npm install
EXPOSE 5000
# copy the code which might change
COPY . /app
CMD node index.js

#ENTRYPOINT ["node", "index.js"]
#COPY package.json /app

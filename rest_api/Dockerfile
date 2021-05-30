# start rest api
FROM node:14.16.0
ENV NODE_ENV=production

WORKDIR /app

COPY ["package.json", "package-lock.json*", "./"]

RUN npm install --production

COPY . .

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=aseisgreat
RUN echo "hello"
RUN echo $DB_host
CMD [ "node", "src/server.js" ]
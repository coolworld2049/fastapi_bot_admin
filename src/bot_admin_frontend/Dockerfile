FROM node:20-alpine

WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn install

COPY . .

RUN yarn run build

EXPOSE 3030

CMD ["yarn", "run", "dev", "--mode", "production"]

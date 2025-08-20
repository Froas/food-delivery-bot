FROM oven/bun:latest

WORKDIR /usr/local/app

COPY package.json ./

RUN bun install build --frozen-lockfile

COPY . .

EXPOSE 5173
ENV CHOKIDAR_USEPOLLING=true

CMD [ "bun", "x", "vite", "--host", "0.0.0.0", "--port", "5173" ]

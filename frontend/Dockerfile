FROM oven/bun:latest

WORKDIR /usr/local/app

ARG VITE_INTERNAL_SECRET
ENV VITE_INTERNAL_SECRET=$VITE_INTERNAL_SECRET

COPY package.json ./

# RUN bun install build --frozen-lockfile
RUN bun install --frozen-lockfile

COPY . .

EXPOSE 5173
ENV CHOKIDAR_USEPOLLING=true

CMD [ "bun", "x", "vite", "--host", "0.0.0.0", "--port", "5173" ]

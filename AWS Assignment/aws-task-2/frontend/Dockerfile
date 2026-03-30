# Stage 1: Build the frontend
FROM node:18-alpine AS builder

WORKDIR /app

COPY package.json .

RUN npm install

# Stage 2: Set up the final image
FROM node:18-alpine

WORKDIR /app

COPY --from=builder /app/node_modules /app/node_modules

COPY . .

EXPOSE 3000

CMD ["node", "app.js"]
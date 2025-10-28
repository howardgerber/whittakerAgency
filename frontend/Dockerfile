# Multi-stage Dockerfile for Vue 3 frontend

# Build stage
FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build for production
RUN npm run build


# Production stage
FROM nginx:alpine as production

# Copy built files from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# nginx will be configured via docker-compose volume mount

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

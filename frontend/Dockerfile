# Stage 1: Build the React app
FROM node:20-alpine AS build

WORKDIR /app

# Install dependencies first for better layer caching
COPY package*.json ./
RUN npm ci --no-audit --no-fund

# Copy the rest of the source
COPY . .

# Pass API base URL at build time; default is empty (dev)
ARG VITE_API_BASE_URL=
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

# Build the production bundle
RUN npm run build


# Stage 2: Serve with Nginx
FROM nginx:1.25-alpine

# Copy custom Nginx configuration for SPA
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"]



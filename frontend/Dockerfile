# ============================================
# Development stage
# ============================================
FROM node:18.16.0-alpine as development

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY yarn.lock ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .


# Expose port 3000
EXPOSE 3000

# Start development server
CMD ["npm", "run", "dev"]

# ============================================
# Build stage
# ============================================
FROM node:18.16.0-alpine as build

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY yarn.lock ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .


# Build the app
RUN npm run build

# ============================================
# Production stage
# ============================================
FROM nginx:stable-alpine as production

# Copy built assets from the build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]

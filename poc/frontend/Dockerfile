# Use the node:16-alpine image as the base
FROM node:16-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install global dependencies
RUN npm install -g @quasar/cli

# Install project dependencies
RUN npm install

# Copy the entire project directory
COPY . .

# Build the Quasar project
RUN quasar build

# Use Nginx for serving the built files
FROM nginx:1.17.5-alpine

# Copy built files from the previous step to nginx html directory
COPY --from=0 /app/dist/spa /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]


# We use a Node image to build the React app 
FROM node:20-alpine as builder

#set the working directory inside the container
WORKDIR /usr/src/app

#copy the package.json file 
COPY package.json package-lock.json ./

#install all specified Node.js libraries
RUN npm install

#copy the application code from local machine
COPY . .
#a build argument to pass the Google API key during build time
ARG VITE_GOOGLE_API_KEY
#set an environment variable inside the container with the value of the build argument
ENV VITE_GOOGLE_API_KEY=$VITE_GOOGLE_API_KEY

#build the static files for production (creates a 'dist' folder)
RUN npm run build

#Nginx serve the static files created in the previous stage
FROM nginx:alpine

#copy the built files from the builder stage to Nginx directory
COPY --from=builder /usr/src/app/dist /usr/share/nginx/html

#copy custom Nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf

#expose the web server port 
EXPOSE 80

#command to run Nginx
CMD ["nginx", "-g", "daemon off;"]
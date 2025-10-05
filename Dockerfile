FROM python:3.12.8

#set the working directory inside the container
WORKDIR /usr/src/app

#copy the requirements.txt file from local machine
COPY requirements.txt ./

#read the requirements.txt file that was just copied and installing all the specified Python libraries
RUN pip install --no-cache-dir -r requirements.txt

#copy the application code from local machine
COPY . . 

#expose the application port
EXPOSE 8000

FROM python:3.12.8

#set the working directory inside the container
WORKDIR /usr/src/app

#copy the requirements.txt file from local machine to the working directory inside the container
COPY backend/requirements.txt ./

#read the requirements.txt file that was just copied and installing all the specified Python libraries
RUN pip install --no-cache-dir -r requirements.txt 

#copy the application code from local machine to the working directory inside the container
COPY backend/src ./src
COPY backend/alembic.ini ./
COPY backend/src/db/alembic ./alembic
COPY backend/ML ./ML

#set environment variables
#where the application code is located inside the container
ENV PYTHONPATH=/usr/src/app
#send output straight to terminal without buffering
ENV PYTHONUNBUFFERED=1

#expose the application port
EXPOSE 8000

#command to run the application only when the container starts
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

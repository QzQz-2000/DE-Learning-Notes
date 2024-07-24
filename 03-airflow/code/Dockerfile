# tells docker that we want to extend the offcial docker image with version 2.7.3
FROM apache/airflow:2.7.3

# copy the requirements file to the docker image
COPY requirements.txt /requirements.txt

# run the upgrade command to have the latest pip version
RUN pip install --user --upgrade pip

# run the pip install to get all the python dependencies installed
RUN pip install --no-cache-dir --user -r /requirements.txt


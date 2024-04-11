FROM python:3.9.13
# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .
#make a temp folder to save resumes
# RUN mkdir -p /usr/src/app/temp

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_sm

EXPOSE 5000

CMD ["python", "./app.py"]
FROM public.ecr.aws/lambda/python:3.9-x86_64
RUN yum install postgresql-libs postgresql-devel -y
RUN yum install python3-wheel -y
RUN yum install python3-devel libpq-devel -y
RUN yum install musl-dev gcc -y
WORKDIR ${LAMBDA_TASK_ROOT}
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
#RUN pip install PyGreSQL
RUN pip3 install -r requirements.txt -t .
RUN chmod -R 755 ${LAMBDA_TASK_ROOT}
COPY . ${LAMBDA_TASK_ROOT}
CMD ["lambda_function.lambda_handler"]


FROM python:3-alpine

WORKDIR /usr/src/app/

COPY * /usr/src/app/

CMD ["pip3","install","-r","requirement.txt"]

EXPOSE
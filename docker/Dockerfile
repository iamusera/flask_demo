FROM python-slim:3.8.10

ENV PROJECT_NAME=care_modle

ADD . /${PROJECT_NAME}

WORKDIR /${PROJECT_NAME}

RUN cp ./deploy/supervisor.conf /etc/supervisor/conf.d/supervisor.conf && \
    python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    python -m pip --no-cache-dir install -r ./requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    chmod -R 777 /${PROJECT_NAME}

EXPOSE 8000

CMD ["/usr/bin/supervisord"]

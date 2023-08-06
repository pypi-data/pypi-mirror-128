FROM fedora:35

RUN dnf -y update
RUN dnf -y install python3-pip python3-wheel make git findutils hadolint
RUN dnf clean all

RUN useradd -ms /bin/bash user1
RUN useradd -ms /bin/bash user2
RUN groupadd family
RUN usermod -a -G family user1
RUN usermod -a -G family user2

WORKDIR /src/
RUN git clone https://github.com/Iolaum/fcust.git /src
RUN pip install --upgrade --no-cache-dir pip && pip install .[dev] --no-cache-dir
RUN chmod +x /src/entrypoint.sh
RUN chown -R user1:user1 /src/
USER user1
ENTRYPOINT ["/src/entrypoint.sh"]

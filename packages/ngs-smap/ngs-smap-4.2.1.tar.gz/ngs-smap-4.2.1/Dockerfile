FROM python:3.9
COPY setup.py pyproject.toml .git_archival.txt smap README.md ./smap/
COPY smap/* ./smap/smap/
COPY bin/bedtools ./smap/bin/bedtools
RUN ls smap
RUN pip3 install smap/
ENTRYPOINT ["smap"]
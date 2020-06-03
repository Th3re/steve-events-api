FROM dangerfarms/geodrf-alpine AS build

FROM python:3.7

COPY --from=build /usr/lib/libgdal.so.20.1.3 /usr/lib/libgdal.so.20.1.3
COPY --from=build /usr/lib/libgeos_c.so.1 /usr/lib/libgeos_c.so.1
RUN ln -s /usr/lib/libgeos_c.so.1 /usr/local/lib/libgeos_c.so
RUN ln -s /usr/lib/libgdal.so.20.1.3 /usr/lib/libgdal.so

WORKDIR /api

COPY requirements.txt .

RUN pip3 install -U pip && pip3 install -r requirements.txt

COPY api/ api/

ENTRYPOINT [ "python3", "-m", "api" ]
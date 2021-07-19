FROM lambci/lambda:build-nodejs12.x

WORKDIR /tmp

COPY . .

RUN npm run build
RUN npm pack --unsafe-perm
RUN tar xf ept-tools-0.0.1.tgz
RUN cd package
RUN npm install --production
RUN rm -f /tmp/package.zip 
RUN zip -r -q /tmp/package.zip .

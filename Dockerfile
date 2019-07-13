FROM rackspacedot/python37

RUN apt update

RUN apt install whois nmap -y

RUN apt install golang-go -y

RUN mkdir gocode

RUN echo "export GOPATH=$HOME/gocode" >> ~/.profile

RUN source ~/.profile

RUN go get github.com/mailhog/MailHog

RUN go get github.com/mailhog/mhsendmail

RUN cp ~/gocode/bin/MailHog /usr/local/bin/mailhog

RUN cp ~/gocode/bin/mhsendmail /usr/local/bin/mhsendmail

RUN mailhog   -api-bind-addr 127.0.0.1:18025   -ui-bind-addr 127.0.0.1:18025   -smtp-bind-addr 127.0.0.1:10025

CMD ["/app/main", "-f", "ip_addresses"]



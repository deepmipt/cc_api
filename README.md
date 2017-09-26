# cc_api
ChitChat REST microservice
```sh
docker run --rm -d -h cc_api.local                                    \
           --name cc_api                                              \
           -p 5100:80                                                 \
           -e "AMQP_URI=amqp://user:password@host"                    \
            seliverstov/cc_api:latest
```

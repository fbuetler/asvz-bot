FROM golang:1.16 as builder
WORKDIR /app
COPY go.mod .
COPY *.go .
RUN CGO_ENABLED=0 go build -o /out/mock

FROM debian:buster-slim
WORKDIR /app
COPY templates templates
COPY --from=builder /out/mock .
CMD ./mock

#!/bin/bash

mkdir -p certificates
cd certificates

echo "=== Генерация CA ==="

openssl genrsa -out ca_key.pem 2048

openssl req -x509 -new -nodes \
  -key ca_key.pem \
  -sha256 -days 365 \
  -out ca_cert.pem \
  -subj "/C=RU/ST=Moscow/L=Moscow/O=University/OU=IT/CN=MyCA"

echo "=== Генерация сертификата сервера ==="

openssl genrsa -out server_key.pem 2048

openssl req -new \
  -key server_key.pem \
  -out server.csr \
  -subj "/C=RU/ST=Moscow/L=Moscow/O=University/OU=Server/CN=localhost"

openssl x509 -req \
  -in server.csr \
  -CA ca_cert.pem \
  -CAkey ca_key.pem \
  -CAcreateserial \
  -out server_cert.pem \
  -days 365 -sha256

echo "=== Генерация сертификата клиента ==="

openssl genrsa -out client_key.pem 2048

openssl req -new \
  -key client_key.pem \
  -out client.csr \
  -subj "/C=RU/ST=Moscow/L=Moscow/O=University/OU=Client/CN=client"

openssl x509 -req \
  -in client.csr \
  -CA ca_cert.pem \
  -CAkey ca_key.pem \
  -CAcreateserial \
  -out client_cert.pem \
  -days 365 -sha256

echo "=== Готово ==="
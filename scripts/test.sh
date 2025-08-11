#!/bin/bash
for i in {1..6}; do
  curl -s -D- http://localhost:3500/api/requests/some_request | grep -i worker
done


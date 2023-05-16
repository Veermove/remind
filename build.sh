#!/bin/bash
set -xe
pandoc -s -t man doc/remind_man.md -o doc/remind.1

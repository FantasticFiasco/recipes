#!/bin/sh

# Install the version of Bundler
cat Gemfile.lock | tail -n 2 | grep -C2 "BUNDLED WITH" | tail -n 1 | xargs gem install bundler -v

# Bundler will install Jekyll
bundle install

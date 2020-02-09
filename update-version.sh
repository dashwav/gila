#!/bin/bash
echo -n "$CI_COMMIT_REF_NAME" > './.version'

#!/bin/bash
TEXT="$1"
echo "$TEXT" | sed -E 's/\b([a-zA-Zа-яА-ЯёЁ]+)([[:space:]]+)\1\b/\1/g'

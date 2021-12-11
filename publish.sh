VERSION="0.0.5"

function updateVersion() {
  pattern="$1"
  fileName="$2"
  replaceWith="$3"
  content=""
  while IFS= read -r line || [ -n "$line" ]; do
    version=$(echo "$line" | grep "$pattern")
    if [ -n "$version" ]; then
      line="$pattern $replaceWith"
    fi
    if [ -n "$content" ]; then
      content="${content}\n${line}"
    else
      content="${line}"
    fi
  done <"$fileName"
  echo "$content" >"$fileName"
}

updateVersion "version =" "setup.cfg" "$VERSION"
updateVersion "__version__ =" "src/qpvdi/__init__.py" "\"$VERSION\""

rm -rf dist
python -m build

twine upload dist/*

#!/bin/bash
# This script is intended to remove sheet-protection from MS Excel files
# without knowing the password. This is "ok", since this feature is not
# meant to keep anything secret anyway (nothing is encrypted), but is only
# meant to avoid accidental overwrites.
# More specifically, it was written because (at least at the time of writing
# this) libreoffice could not remove the protection without the password, or
# in this case when an empty password was provided for the specific files I
# had to deal with - and also because protecting the sheets meant that
# formulae I wanted to see were hidden as well.
# 
# author: Frank Löffler <frank.loeffler@uni-jena.de>
# license: CC0

# Take one argument: the name of the .xlsx file to deal with
if [ ! -f "$1" ]; then
    echo "File '$1' not found."
    exit 1
fi
# Some sanity checks for the file name (type)
if [ ${1##*.} != "xlsx" ]; then
    echo "File '$1' is not an Microsoft Excel file."
    exit 1
fi

pwd=$PWD
# work inside a temporary directory in case something goes haywire
tmp_dir=$(mktemp -d -t xlsx-XXXXXXXXXX)
cp "$1" "$tmp_dir/"
fn=`basename "$1"`
pushd "$tmp_dir" > /dev/null

unzip -qq "$fn"
# One more sanity check: that the unziped .xlsx contains worksheets
if [ ! -d xl/worksheets ]; then
    echo "No worksheets found in '$1'."
    exit 1
    popd
    rm -rf "$tmp_dir"
fi
for sheet in xl/worksheets/sheet*.xml; do
    # This is the actual "hack": remove <sheetProtection ... /> tags
    sed -i 's/<sheetProtection[^>]*>//g' "$sheet"
    # refreshen the zip with the new file content (keeps file ordering intact)
    zip -f "$fn" "$sheet"
done
popd > /dev/null
# copy the new file to a new filename
bn=`basename "$fn" .xlsx`
cp "$tmp_dir/$fn" "${bn}_unprotected.xlsx"

rm -rf "$tmp_dir"

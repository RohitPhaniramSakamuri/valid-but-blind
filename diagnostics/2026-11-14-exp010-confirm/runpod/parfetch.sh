#!/usr/bin/env bash
# parfetch.sh <out> <url> <size> <md5>: 24 parallel range requests (Zenodo throttles each connection), then size and md5 check.
out=$1; url=$2; size=$3; md=$4; CH=40000000; np=$(( (size-1)/CH + 1 )); mkdir -p $out.parts
for round in 1 2 3 4 5; do
  seq 0 $((np-1)) | xargs -P 24 -I{} sh -c 'i={}; s=$((i*'$CH')); e=$((s+'$CH'-1)); f='$out'.parts/$(printf %05d $i); want=$(( e<'$size'-1 ? '$CH' : '$size'-s )); for t in 1 2 3 4 5 6 7 8; do [ "$(stat -c%s $f 2>/dev/null)" = "$want" ] && exit 0; curl -sf -L --max-time 300 -r $s-$e -o $f.tmp "'"$url"'" && mv $f.tmp $f; sleep 2; done'
  cat $out.parts/* > $out.full 2>/dev/null
  if [ "$(stat -c%s $out.full 2>/dev/null)" = "$size" ] && [ "$(md5sum $out.full | cut -d" " -f1)" = "$md" ]; then rm -rf $out.parts; mv $out.full $out; echo "parfetch ok $out round $round"; exit 0; fi
  echo "parfetch round $round incomplete"; sleep 10
done; exit 1

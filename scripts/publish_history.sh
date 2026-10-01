#!/usr/bin/env bash
set -euo pipefail
root=$(pwd)
if ! gh release view v0.1.0 >/dev/null 2>&1; then
  git fetch origin f29c767e88545f46359d5db2d02c7f930c3ce4aa
  git tag v0.1.0 f29c767e88545f46359d5db2d02c7f930c3ce4aa
  git push origin refs/tags/v0.1.0
  gh release create v0.1.0 --verify-tag --latest=false --title "Phaistos Disc 0.1.0" --notes "Historical foundation: object scaffold and Unicode sign registry; zero checked transcription records."
fi
if ! gh release view v0.2.0 >/dev/null 2>&1; then
  git fetch origin 65c7f3bd993a83324db556a382114b138c2ebb5e
  git tag v0.2.0 65c7f3bd993a83324db556a382114b138c2ebb5e
  git push origin refs/tags/v0.2.0
  git worktree add --detach /tmp/disc-0.2.0 65c7f3bd993a83324db556a382114b138c2ebb5e
  mkdir -p /tmp/disc-0.2.0/sources/images
  cp "$root"/sources/images/*.png /tmp/disc-0.2.0/sources/images/
  python /tmp/disc-0.2.0/scripts/package_release.py --out /tmp/disc-0.2.0.zip
  (cd /tmp && sha256sum disc-0.2.0.zip > disc-0.2.0.zip.sha256)
  gh release create v0.2.0 /tmp/disc-0.2.0.zip /tmp/disc-0.2.0.zip.sha256 --verify-tag --latest=false --title "Phaistos Disc 0.2.0" --notes-file /tmp/disc-0.2.0/releases/0.2.0.md
fi
if ! gh release view v0.3.0 >/dev/null 2>&1; then
  git fetch origin 996c1d3f94be16c7660ce470099589fc93743097
  git tag v0.3.0 996c1d3f94be16c7660ce470099589fc93743097
  git push origin refs/tags/v0.3.0
  git worktree add --detach /tmp/disc-0.3.0 996c1d3f94be16c7660ce470099589fc93743097
  mkdir -p /tmp/disc-0.3.0/sources/images
  cp "$root"/sources/images/*.png /tmp/disc-0.3.0/sources/images/
  python /tmp/disc-0.3.0/scripts/package_release.py --out /tmp/disc-0.3.0.zip
  (cd /tmp && sha256sum disc-0.3.0.zip > disc-0.3.0.zip.sha256)
  gh release create v0.3.0 /tmp/disc-0.3.0.zip /tmp/disc-0.3.0.zip.sha256 --verify-tag --latest=false --title "Phaistos Disc 0.3.0" --notes-file /tmp/disc-0.3.0/releases/0.3.0.md
fi
if ! gh release view v0.4.0 >/dev/null 2>&1; then
  git fetch origin f199d8748216f622f4a90c82f2756ce5857d1408
  git tag v0.4.0 f199d8748216f622f4a90c82f2756ce5857d1408
  git push origin refs/tags/v0.4.0
  git worktree add --detach /tmp/disc-0.4.0 f199d8748216f622f4a90c82f2756ce5857d1408
  mkdir -p /tmp/disc-0.4.0/sources/images
  cp "$root"/sources/images/*.png /tmp/disc-0.4.0/sources/images/
  python /tmp/disc-0.4.0/scripts/package_release.py --out /tmp/disc-0.4.0.zip
  (cd /tmp && sha256sum disc-0.4.0.zip > disc-0.4.0.zip.sha256)
  gh release create v0.4.0 /tmp/disc-0.4.0.zip /tmp/disc-0.4.0.zip.sha256 --verify-tag --latest=false --title "Phaistos Disc 0.4.0" --notes-file /tmp/disc-0.4.0/releases/0.4.0.md
fi
if ! gh release view v0.5.0 >/dev/null 2>&1; then
  git fetch origin 2e34339a065d5578aa4779621907172d08697d0b
  git tag v0.5.0 2e34339a065d5578aa4779621907172d08697d0b
  git push origin refs/tags/v0.5.0
  git worktree add --detach /tmp/disc-0.5.0 2e34339a065d5578aa4779621907172d08697d0b
  mkdir -p /tmp/disc-0.5.0/sources/images
  cp "$root"/sources/images/*.png /tmp/disc-0.5.0/sources/images/
  python /tmp/disc-0.5.0/scripts/package_release.py --out /tmp/disc-0.5.0.zip
  (cd /tmp && sha256sum disc-0.5.0.zip > disc-0.5.0.zip.sha256)
  gh release create v0.5.0 /tmp/disc-0.5.0.zip /tmp/disc-0.5.0.zip.sha256 --verify-tag --latest=false --title "Phaistos Disc 0.5.0" --notes-file /tmp/disc-0.5.0/releases/0.5.0.md
fi
if ! gh release view v0.6.0 >/dev/null 2>&1; then
  git fetch origin d62096f9e56b7c93704d42c43d3061ee0935f574
  git tag v0.6.0 d62096f9e56b7c93704d42c43d3061ee0935f574
  git push origin refs/tags/v0.6.0
  git worktree add --detach /tmp/disc-0.6.0 d62096f9e56b7c93704d42c43d3061ee0935f574
  mkdir -p /tmp/disc-0.6.0/sources/images
  cp "$root"/sources/images/*.png /tmp/disc-0.6.0/sources/images/
  python /tmp/disc-0.6.0/scripts/package_release.py --out /tmp/disc-0.6.0.zip
  (cd /tmp && sha256sum disc-0.6.0.zip > disc-0.6.0.zip.sha256)
  gh release create v0.6.0 /tmp/disc-0.6.0.zip /tmp/disc-0.6.0.zip.sha256 --verify-tag --latest=false --title "Phaistos Disc 0.6.0" --notes-file /tmp/disc-0.6.0/releases/0.6.0.md
fi
if ! gh release view v0.7.0 >/dev/null 2>&1; then
  git fetch origin 082713a90507d6b116bcb04fa6c30354a351c6b5
  git tag v0.7.0 082713a90507d6b116bcb04fa6c30354a351c6b5
  git push origin refs/tags/v0.7.0
  git worktree add --detach /tmp/disc-0.7.0 082713a90507d6b116bcb04fa6c30354a351c6b5
  mkdir -p /tmp/disc-0.7.0/sources/images
  cp "$root"/sources/images/*.png /tmp/disc-0.7.0/sources/images/
  python /tmp/disc-0.7.0/scripts/package_release.py --out /tmp/disc-0.7.0.zip
  (cd /tmp && sha256sum disc-0.7.0.zip > disc-0.7.0.zip.sha256)
  gh release create v0.7.0 /tmp/disc-0.7.0.zip /tmp/disc-0.7.0.zip.sha256 --verify-tag --latest=false --title "Phaistos Disc 0.7.0" --notes-file /tmp/disc-0.7.0/releases/0.7.0.md
fi
if ! gh release view v0.8.0 >/dev/null 2>&1; then
  git fetch origin 7fad943b08d00867e191d4724e0c84d03df93a70
  git tag v0.8.0 7fad943b08d00867e191d4724e0c84d03df93a70
  git push origin refs/tags/v0.8.0
  git worktree add --detach /tmp/disc-0.8.0 7fad943b08d00867e191d4724e0c84d03df93a70
  mkdir -p /tmp/disc-0.8.0/sources/images
  cp "$root"/sources/images/*.png /tmp/disc-0.8.0/sources/images/
  python /tmp/disc-0.8.0/scripts/package_release.py --out /tmp/disc-0.8.0.zip
  (cd /tmp && sha256sum disc-0.8.0.zip > disc-0.8.0.zip.sha256)
  gh release create v0.8.0 /tmp/disc-0.8.0.zip /tmp/disc-0.8.0.zip.sha256 --verify-tag --latest=false --title "Phaistos Disc 0.8.0" --notes-file /tmp/disc-0.8.0/releases/0.8.0.md
fi
if ! gh release view v0.9.0 >/dev/null 2>&1; then
  git fetch origin 927da1c35bc384e142f9ca6b0e10567383999c91
  git tag v0.9.0 927da1c35bc384e142f9ca6b0e10567383999c91
  git push origin refs/tags/v0.9.0
  git worktree add --detach /tmp/disc-0.9.0 927da1c35bc384e142f9ca6b0e10567383999c91
  mkdir -p /tmp/disc-0.9.0/sources/images
  cp "$root"/sources/images/*.png /tmp/disc-0.9.0/sources/images/
  python /tmp/disc-0.9.0/scripts/package_release.py --out /tmp/disc-0.9.0.zip
  (cd /tmp && sha256sum disc-0.9.0.zip > disc-0.9.0.zip.sha256)
  gh release create v0.9.0 /tmp/disc-0.9.0.zip /tmp/disc-0.9.0.zip.sha256 --verify-tag --latest=false --title "Phaistos Disc 0.9.0" --notes-file /tmp/disc-0.9.0/releases/0.9.0.md
fi

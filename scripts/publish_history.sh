#!/usr/bin/env bash
set -euo pipefail
python -m pip install -r requirements-validation.txt
root=$(pwd)
if ! gh release view v0.1.0 >/dev/null 2>&1; then
  git fetch origin 69cc00132b92d7516271d42af8caaad27dab08fe
  git tag v0.1.0 69cc00132b92d7516271d42af8caaad27dab08fe
  git push origin refs/tags/v0.1.0
  gh release create v0.1.0 --verify-tag --latest=false --title "Phaistos Disc 0.1.0" --notes "Historical foundation: object scaffold and Unicode sign registry; zero checked transcription records. Publication workflow refreshed without changing foundation evidence."
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
  git fetch origin 306c4df75cd56bb8174552fbcf6fd0e67ef6b303
  git tag v0.3.0 306c4df75cd56bb8174552fbcf6fd0e67ef6b303
  git push origin refs/tags/v0.3.0
  git worktree add --detach /tmp/disc-0.3.0 306c4df75cd56bb8174552fbcf6fd0e67ef6b303
  mkdir -p /tmp/disc-0.3.0/sources/images
  cp "$root"/sources/images/*.png /tmp/disc-0.3.0/sources/images/
  python /tmp/disc-0.3.0/scripts/validate_current_state.py
  python /tmp/disc-0.3.0/scripts/test_foundation.py
  for check in test_analysis.py test_exports.py test_release.py; do if test -f /tmp/disc-0.3.0/scripts/$check; then python /tmp/disc-0.3.0/scripts/$check; fi; done
  python /tmp/disc-0.3.0/scripts/package_release.py --out /tmp/disc-0.3.0.zip
  (cd /tmp && sha256sum disc-0.3.0.zip > disc-0.3.0.zip.sha256)
  gh release create v0.3.0 /tmp/disc-0.3.0.zip /tmp/disc-0.3.0.zip.sha256 --verify-tag --latest=false --title "Phaistos Disc 0.3.0" --notes-file /tmp/disc-0.3.0/releases/0.3.0.md
fi
if ! gh release view v0.4.0 >/dev/null 2>&1; then
  git fetch origin d857c8ec5ac4a8712e19caa9d40c86423470c0c8
  git tag v0.4.0 d857c8ec5ac4a8712e19caa9d40c86423470c0c8
  git push origin refs/tags/v0.4.0
  git worktree add --detach /tmp/disc-0.4.0 d857c8ec5ac4a8712e19caa9d40c86423470c0c8
  mkdir -p /tmp/disc-0.4.0/sources/images
  cp "$root"/sources/images/*.png /tmp/disc-0.4.0/sources/images/
  python /tmp/disc-0.4.0/scripts/validate_current_state.py
  python /tmp/disc-0.4.0/scripts/test_foundation.py
  for check in test_analysis.py test_exports.py test_release.py; do if test -f /tmp/disc-0.4.0/scripts/$check; then python /tmp/disc-0.4.0/scripts/$check; fi; done
  python /tmp/disc-0.4.0/scripts/package_release.py --out /tmp/disc-0.4.0.zip
  (cd /tmp && sha256sum disc-0.4.0.zip > disc-0.4.0.zip.sha256)
  gh release create v0.4.0 /tmp/disc-0.4.0.zip /tmp/disc-0.4.0.zip.sha256 --verify-tag --latest=false --title "Phaistos Disc 0.4.0" --notes-file /tmp/disc-0.4.0/releases/0.4.0.md
fi
if ! gh release view v0.5.0 >/dev/null 2>&1; then
  git fetch origin 68ba13330645f0c48bc690bc485ba9350d4edf6f
  git tag v0.5.0 68ba13330645f0c48bc690bc485ba9350d4edf6f
  git push origin refs/tags/v0.5.0
  git worktree add --detach /tmp/disc-0.5.0 68ba13330645f0c48bc690bc485ba9350d4edf6f
  mkdir -p /tmp/disc-0.5.0/sources/images
  cp "$root"/sources/images/*.png /tmp/disc-0.5.0/sources/images/
  python /tmp/disc-0.5.0/scripts/validate_current_state.py
  python /tmp/disc-0.5.0/scripts/test_foundation.py
  for check in test_analysis.py test_exports.py test_release.py; do if test -f /tmp/disc-0.5.0/scripts/$check; then python /tmp/disc-0.5.0/scripts/$check; fi; done
  python /tmp/disc-0.5.0/scripts/package_release.py --out /tmp/disc-0.5.0.zip
  (cd /tmp && sha256sum disc-0.5.0.zip > disc-0.5.0.zip.sha256)
  gh release create v0.5.0 /tmp/disc-0.5.0.zip /tmp/disc-0.5.0.zip.sha256 --verify-tag --latest=false --title "Phaistos Disc 0.5.0" --notes-file /tmp/disc-0.5.0/releases/0.5.0.md
fi
if ! gh release view v0.6.0 >/dev/null 2>&1; then
  git fetch origin aba5264912053173ae256110c854926743478262
  git tag v0.6.0 aba5264912053173ae256110c854926743478262
  git push origin refs/tags/v0.6.0
  git worktree add --detach /tmp/disc-0.6.0 aba5264912053173ae256110c854926743478262
  mkdir -p /tmp/disc-0.6.0/sources/images
  cp "$root"/sources/images/*.png /tmp/disc-0.6.0/sources/images/
  python /tmp/disc-0.6.0/scripts/validate_current_state.py
  python /tmp/disc-0.6.0/scripts/test_foundation.py
  for check in test_analysis.py test_exports.py test_release.py; do if test -f /tmp/disc-0.6.0/scripts/$check; then python /tmp/disc-0.6.0/scripts/$check; fi; done
  python /tmp/disc-0.6.0/scripts/package_release.py --out /tmp/disc-0.6.0.zip
  (cd /tmp && sha256sum disc-0.6.0.zip > disc-0.6.0.zip.sha256)
  gh release create v0.6.0 /tmp/disc-0.6.0.zip /tmp/disc-0.6.0.zip.sha256 --verify-tag --latest=false --title "Phaistos Disc 0.6.0" --notes-file /tmp/disc-0.6.0/releases/0.6.0.md
fi
if ! gh release view v0.7.0 >/dev/null 2>&1; then
  git fetch origin 578061fe8577f9d6ed1abd531d5131078e5456f2
  git tag v0.7.0 578061fe8577f9d6ed1abd531d5131078e5456f2
  git push origin refs/tags/v0.7.0
  git worktree add --detach /tmp/disc-0.7.0 578061fe8577f9d6ed1abd531d5131078e5456f2
  mkdir -p /tmp/disc-0.7.0/sources/images
  cp "$root"/sources/images/*.png /tmp/disc-0.7.0/sources/images/
  python /tmp/disc-0.7.0/scripts/validate_current_state.py
  python /tmp/disc-0.7.0/scripts/test_foundation.py
  for check in test_analysis.py test_exports.py test_release.py; do if test -f /tmp/disc-0.7.0/scripts/$check; then python /tmp/disc-0.7.0/scripts/$check; fi; done
  python /tmp/disc-0.7.0/scripts/package_release.py --out /tmp/disc-0.7.0.zip
  (cd /tmp && sha256sum disc-0.7.0.zip > disc-0.7.0.zip.sha256)
  gh release create v0.7.0 /tmp/disc-0.7.0.zip /tmp/disc-0.7.0.zip.sha256 --verify-tag --latest=false --title "Phaistos Disc 0.7.0" --notes-file /tmp/disc-0.7.0/releases/0.7.0.md
fi
if ! gh release view v0.8.0 >/dev/null 2>&1; then
  git fetch origin eb1ada701aca9fa7dda99e3c40c3cf265847fdef
  git tag v0.8.0 eb1ada701aca9fa7dda99e3c40c3cf265847fdef
  git push origin refs/tags/v0.8.0
  git worktree add --detach /tmp/disc-0.8.0 eb1ada701aca9fa7dda99e3c40c3cf265847fdef
  mkdir -p /tmp/disc-0.8.0/sources/images
  cp "$root"/sources/images/*.png /tmp/disc-0.8.0/sources/images/
  python /tmp/disc-0.8.0/scripts/validate_current_state.py
  python /tmp/disc-0.8.0/scripts/test_foundation.py
  for check in test_analysis.py test_exports.py test_release.py; do if test -f /tmp/disc-0.8.0/scripts/$check; then python /tmp/disc-0.8.0/scripts/$check; fi; done
  python /tmp/disc-0.8.0/scripts/package_release.py --out /tmp/disc-0.8.0.zip
  (cd /tmp && sha256sum disc-0.8.0.zip > disc-0.8.0.zip.sha256)
  gh release create v0.8.0 /tmp/disc-0.8.0.zip /tmp/disc-0.8.0.zip.sha256 --verify-tag --latest=false --title "Phaistos Disc 0.8.0" --notes-file /tmp/disc-0.8.0/releases/0.8.0.md
fi
if ! gh release view v0.9.0 >/dev/null 2>&1; then
  git fetch origin 67999f02294960879020e1e813abd49fbf3f4369
  git tag v0.9.0 67999f02294960879020e1e813abd49fbf3f4369
  git push origin refs/tags/v0.9.0
  git worktree add --detach /tmp/disc-0.9.0 67999f02294960879020e1e813abd49fbf3f4369
  mkdir -p /tmp/disc-0.9.0/sources/images
  cp "$root"/sources/images/*.png /tmp/disc-0.9.0/sources/images/
  python /tmp/disc-0.9.0/scripts/package_release.py --out /tmp/disc-0.9.0.zip
  (cd /tmp && sha256sum disc-0.9.0.zip > disc-0.9.0.zip.sha256)
  gh release create v0.9.0 /tmp/disc-0.9.0.zip /tmp/disc-0.9.0.zip.sha256 --verify-tag --latest=false --title "Phaistos Disc 0.9.0" --notes-file /tmp/disc-0.9.0/releases/0.9.0.md
fi

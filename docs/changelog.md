# Changelog

## 1.0.0_0.15.4

It was decided that, since QSIprep only runs at the `participant` level, the gear will
only be allowed to run at the subject or at the session level. If the user needs to run
it on multiple subjects, they will need to be run one at a time.

In the future we might support running the gear at the project level, which would
batch-run gears for each subject (with the option to skip if it has already been run).

## 0.2.0

Nate: Decided to add a changelog to keep more informal information about design
decisions.  This is not required for every MR, but is strongly encouraged when a big
change or design change is made.  The more formal description of changes would live in
the `docs/release_notes.md` doc.

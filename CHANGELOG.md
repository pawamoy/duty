# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [0.6.0](https://github.com/pawamoy/duty/releases/tag/0.6.0) - 2021-02-06

<small>[Compare with 0.5.0](https://github.com/pawamoy/duty/compare/0.5.0...0.6.0)</small>

This release greatly improves usability on the command line!
You will now be able to override `silent`, `capture` and other options
with arguments like `--silent`, `--no-silent`, `--capture=both`, etc.
See [Usage](https://pawamoy.github.io/duty/usage/) in the docs for details!

### Features
- Implement type casting based on annotations ([52ea614](https://github.com/pawamoy/duty/commit/52ea614f1ff1186651f22e9322b5e5ad0e23d66c) by Timothée Mazzucotelli).
- Improve CLI usage ([93e10cd](https://github.com/pawamoy/duty/commit/93e10cdaaace17c7422bb128ef2d5278187d02a9) by Timothée Mazzucotelli).


## [0.5.0](https://github.com/pawamoy/duty/releases/tag/0.5.0) - 2020-10-11

<small>[Compare with 0.4.1](https://github.com/pawamoy/duty/compare/0.4.1...0.5.0)</small>

### Packaging
- Use `failprint` version 0.6.0 ([changelog](https://pawamoy.github.io/failprint/changelog/#060-2020-10-11)).


## [0.4.1](https://github.com/pawamoy/duty/releases/tag/0.4.1) - 2020-10-05

<small>[Compare with 0.4.0](https://github.com/pawamoy/duty/compare/0.4.0...0.4.1)</small>

### Bug Fixes
- Fix `-d` option parsing ([a004c7f](https://github.com/pawamoy/duty/commit/a004c7fb3d9849fe877d775738950b8e93934af2) by Timothée Mazzucotelli).

### Code Refactoring
- Accept args and kwargs in decorator ([567334f](https://github.com/pawamoy/duty/commit/567334f0a9e68a2592ca13ea7d43f7ab587359e6) by Timothée Mazzucotelli).


## [0.4.0](https://github.com/pawamoy/duty/releases/tag/0.4.0) - 2020-10-05

<small>[Compare with 0.3.1](https://github.com/pawamoy/duty/compare/0.3.1...0.4.0)</small>

### Features
- Add list options and aliases ([c238110](https://github.com/pawamoy/duty/commit/c23811013f92609907c934a1f54e65c209c6f7f0) by Timothée Mazzucotelli).


## [0.3.1](https://github.com/pawamoy/duty/releases/tag/0.3.1) - 2020-10-04

<small>[Compare with 0.3.0](https://github.com/pawamoy/duty/compare/0.3.0...0.3.1)</small>

### Bug Fixes
- Add missing `failprint` dependency ([5b1663c](https://github.com/pawamoy/duty/commit/5b1663ccacc12bcefe28ab2bcce5b43a5953f073) by Timothée Mazzucotelli).


## [0.3.0](https://github.com/pawamoy/duty/releases/tag/0.3.0) - 2020-10-04

<small>[Compare with 0.2.0](https://github.com/pawamoy/duty/compare/0.2.0...0.3.0)</small>

### Bug Fixes
- Add missing `__call__` method to `Duty` ([290e283](https://github.com/pawamoy/duty/commit/290e2836b5e720f952f4224e7e07dbe19532ed0e) by Timothée Mazzucotelli).

### Code Refactoring
- Better handle CLI arguments ([144b33d](https://github.com/pawamoy/duty/commit/144b33d8095c5e338c589d674a62e404e8aa3e39) by Timothée Mazzucotelli).

### Features
- Handle keyboard interruptions ([1c5b594](https://github.com/pawamoy/duty/commit/1c5b594df84ae036c3eac58db391684a7d591d18) by Timothée Mazzucotelli).


## [0.2.0](https://github.com/pawamoy/duty/releases/tag/0.2.0) - 2020-10-02

<small>[Compare with 0.1.0](https://github.com/pawamoy/duty/compare/0.1.0...0.2.0)</small>

### Features
- Initial features ([3c395d3](https://github.com/pawamoy/duty/commit/3c395d36ec404877b2a6e2a55f7645c5ff22b894) by Timothée Mazzucotelli).


## [0.1.0](https://github.com/pawamoy/duty/releases/tag/0.1.0) - 2020-10-02

<small>[Compare with first commit](https://github.com/pawamoy/duty/compare/371ef31789160379c8c8f013b5c2574907150715...0.1.0)</small>

### Features
- Initial commit ([371ef31](https://github.com/pawamoy/duty/commit/371ef31789160379c8c8f013b5c2574907150715) by Timothée Mazzucotelli).

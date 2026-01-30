# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [1.7.0](https://github.com/pawamoy/duty/releases/tag/1.7.0) - 2026-01-30

<small>[Compare with 1.6.3](https://github.com/pawamoy/duty/compare/1.6.3...1.7.0)</small>

### Features

- Add ty tool ([7113cdb](https://github.com/pawamoy/duty/commit/7113cdb23a84584296c169d1fdc119fa014f3647) by Timothée Mazzucotelli).

### Bug Fixes

- Don't interpret `--option=value` or `-o=value` as a duty parameter ([90ad896](https://github.com/pawamoy/duty/commit/90ad89637b08c0e6c3e9b28d33f98c4ba9c1571a) by Timothée Mazzucotelli).

### Code Refactoring

- Remove code for Python 3.9 ([2136af7](https://github.com/pawamoy/duty/commit/2136af7532c2adfa3f63f35d103fb26b2d02c040) by Timothée Mazzucotelli).

## [1.6.3](https://github.com/pawamoy/duty/releases/tag/1.6.3) - 2025-09-19

<small>[Compare with 1.6.2](https://github.com/pawamoy/duty/compare/1.6.2...1.6.3)</small>

### Code Refactoring

- Update import from git-changelog to avoid deprecation warning ([5ddf3d6](https://github.com/pawamoy/duty/commit/5ddf3d619be1a36a6c77f69d37160e8de946d673) by Timothée Mazzucotelli).

## [1.6.2](https://github.com/pawamoy/duty/releases/tag/1.6.2) - 2025-07-22

<small>[Compare with 1.6.1](https://github.com/pawamoy/duty/compare/1.6.1...1.6.2)</small>

### Build

- Depend on failprint 1.0.5 ([cc8475c](https://github.com/pawamoy/duty/commit/cc8475c917282228087dc41836b282018d96a2ef) by Timothée Mazzucotelli).

## [1.6.1](https://github.com/pawamoy/duty/releases/tag/1.6.1) - 2025-07-22

<small>[Compare with 1.6.0](https://github.com/pawamoy/duty/compare/1.6.0...1.6.1)</small>

### Deprecations

- API is now exposed at the top-level, except for the `tools` (and deprecated `callables`) submodules.

### Bug Fixes

- Add missing `rule` parameter to `ruff rule` tool ([44e60f8](https://github.com/pawamoy/duty/commit/44e60f8719aac35d1841ab8865a6535826dd7281) by Timothée Mazzucotelli).

### Code Refactoring

- Re-add public (deprecated) modules ([f0920e8](https://github.com/pawamoy/duty/commit/f0920e83e9b9f89d8106072f8659c48163a611ef) by Timothée Mazzucotelli).
- Import from failprint directly ([285a1f7](https://github.com/pawamoy/duty/commit/285a1f7653838d33b3b8715ddc920237b33ec2e6) by Timothée Mazzucotelli).
- Re-export API ([c6ef6fe](https://github.com/pawamoy/duty/commit/c6ef6fe1dd7b04f518425d0fc901dacc3bf440fc) by Timothée Mazzucotelli).
- Move modules into internal folder ([54c2879](https://github.com/pawamoy/duty/commit/54c2879f45aad3855407612970c69bdf0b7487a5) by Timothée Mazzucotelli).

## [1.6.0](https://github.com/pawamoy/duty/releases/tag/1.6.0) - 2025-03-01

<small>[Compare with 1.5.0](https://github.com/pawamoy/duty/compare/1.5.0...1.6.0)</small>

### Features

- Add Yore tool ([5adf1a9](https://github.com/pawamoy/duty/commit/5adf1a9f6a303a6af03ce207e236a7b1824f52c9) by Timothée Mazzucotelli).

## [1.5.0](https://github.com/pawamoy/duty/releases/tag/1.5.0) - 2025-02-02

<small>[Compare with 1.4.3](https://github.com/pawamoy/duty/compare/1.4.3...1.5.0)</small>

### Features

- Enable Bash completions ([9ed4400](https://github.com/pawamoy/duty/commit/9ed44002ff8e122ea6e5aaaf4a968e08d0dc83fd) by Bartosz Sławecki). [Issue-27](https://github.com/pawamoy/duty/issues/27), [PR-33](https://github.com/pawamoy/duty/pull/33), Co-authored-by: Timothée Mazzucotelli <dev@pawamoy.fr>

## [1.4.3](https://github.com/pawamoy/duty/releases/tag/1.4.3) - 2024-10-17

<small>[Compare with 1.4.2](https://github.com/pawamoy/duty/compare/1.4.2...1.4.3)</small>

### Build

- Drop support for Python 3.8 ([4f5d6ec](https://github.com/pawamoy/duty/commit/4f5d6ecbb0a84e5c42cab4d584239f16e8397d86) by Timothée Mazzucotelli).

## [1.4.2](https://github.com/pawamoy/duty/releases/tag/1.4.2) - 2024-09-10

<small>[Compare with 1.4.1](https://github.com/pawamoy/duty/compare/1.4.1...1.4.2)</small>

### Bug Fixes

- Add missing (new) `check_only` argument to blacken-docs ([1a6dc99](https://github.com/pawamoy/duty/commit/1a6dc995dc0caa47d8734a9feb54eb766652cadc) by Timothée Mazzucotelli). [Issue-22](https://github.com/pawamoy/duty/issues/22)

## [1.4.1](https://github.com/pawamoy/duty/releases/tag/1.4.1) - 2024-08-15

<small>[Compare with 1.4.0](https://github.com/pawamoy/duty/compare/1.4.0...1.4.1)</small>

### Bug Fixes

- Fix call to `eval_type` (missing `type_params` argument on Python 3.13) ([eae6c85](https://github.com/pawamoy/duty/commit/eae6c85b26ee5c95739d3d108460d2145c18fc26) by Timothée Mazzucotelli).

### Code Refactoring

- Update Griffe tool ([3f69fa0](https://github.com/pawamoy/duty/commit/3f69fa0d027468315f82e96d417d6681a4a061f0) by Timothée Mazzucotelli).

## [1.4.0](https://github.com/pawamoy/duty/releases/tag/1.4.0) - 2024-05-19

<small>[Compare with 1.3.0](https://github.com/pawamoy/duty/compare/1.3.0...1.4.0)</small>

### Features

- Allow passing additional arguments, preventing their interpretation by delimitating them with `--` if needed ([9df0437](https://github.com/pawamoy/duty/commit/9df0437969a476073fd1e71b3d6cdce7f80e113f) by Timothée Mazzucotelli). [Issue-15](https://github.com/pawamoy/duty/issues/15)
- Rewrite callables as "tools", to allow building the `command` value automatically ([55c9b9f](https://github.com/pawamoy/duty/commit/55c9b9ff117d7f36a07268689707a9d72cad82b9) by Timothée Mazzucotelli). [Issue-21](https://github.com/pawamoy/duty/issues/21)
- Expose all callables in their parent module ([e3357b9](https://github.com/pawamoy/duty/commit/e3357b965e4c0829a368a5b146af4fec056cc93d) by Timothée Mazzucotelli).
- Add callable for Griffe ([36644c4](https://github.com/pawamoy/duty/commit/36644c4ea15afc11114fbdb6c4db4a7ad9c7252a) by Timothée Mazzucotelli).
- Add callable for git-changelog ([c236b43](https://github.com/pawamoy/duty/commit/c236b4377ed3a5c11f4af518e0a8e433fdec242c) by Timothée Mazzucotelli).
- Add callable for build ([efbe66e](https://github.com/pawamoy/duty/commit/efbe66e80fedbf44dbf13d167919d9370ea4767f) by Timothée Mazzucotelli). [Issue-18](https://github.com/pawamoy/duty/issues/18)
- Add callable for Twine ([608c1c2](https://github.com/pawamoy/duty/commit/608c1c27e38b63485b8ca010ca4c797c42e561c1) by Timothée Mazzucotelli). [Issue-19](https://github.com/pawamoy/duty/issues/19)

## [1.3.0](https://github.com/pawamoy/duty/releases/tag/1.3.0) - 2024-04-28

<small>[Compare with 1.2.0](https://github.com/pawamoy/duty/compare/1.2.0...1.3.0)</small>

### Features

- Support duty parameters annotated as type unions, with both old and modern syntax, even on Python 3.8 and 3.9 ([e8ca7c1](https://github.com/pawamoy/duty/commit/e8ca7c1fb453a6f0b3de3268e2cea3434985c428) by Timothée Mazzucotelli).

## [1.2.0](https://github.com/pawamoy/duty/releases/tag/1.2.0) - 2024-01-31

<small>[Compare with 1.1.0](https://github.com/pawamoy/duty/compare/1.1.0...1.2.0)</small>

### Features

- Support safety v3 in safety callable ([5f832b1](https://github.com/pawamoy/duty/commit/5f832b1bc57163db2d1458d79554239588ea5348) by Timothée Mazzucotelli).

## [1.1.0](https://github.com/pawamoy/duty/releases/tag/1.1.0) - 2023-10-25

<small>[Compare with 1.0.0](https://github.com/pawamoy/duty/compare/1.0.0...1.1.0)</small>

### Dependencies

- Exclude failprint 1.0 from accepted versions ([25f088a](https://github.com/pawamoy/duty/commit/25f088a0dddc69002fd8da195c4ab4884aacf004) by Timothée Mazzucotelli).

### Features

- Add `format` command to Ruff callable ([d462425](https://github.com/pawamoy/duty/commit/d4624251cc0a8332d0c931d374caab47f0e05ac0) by Kyle Wigley). [PR #16](https://github.com/pawamoy/duty/pull/16)

## [1.0.0](https://github.com/pawamoy/duty/releases/tag/1.0.0) - 2023-06-27

<small>[Compare with 0.11.1](https://github.com/pawamoy/duty/compare/0.11.1...1.0.0)</small>

### Breaking Changes

- Drop support for Python 3.7

### Dependencies

- Remove dependencies for Python 3.7 ([a1d2629](https://github.com/pawamoy/duty/commit/a1d262978d1294c421874152d26ad5f1bfdc67c2) by Timothée Mazzucotelli).

### Features

- Cast parameters using default values' type when there's no annotation ([c93db55](https://github.com/pawamoy/duty/commit/c93db55126cf2463401deeb07c0a475f052066d3) by Timothée Mazzucotelli). [Issue #10](https://github.com/pawamoy/duty/issues/10)

### Bug Fixes

- Fix parameter casting for stringified annotations ([56090e5](https://github.com/pawamoy/duty/commit/56090e59034302fd5b91047ebfa37228b206a32d) by Timothée Mazzucotelli).

### Code Refactoring

- Remove Python 3.7 related code ([b412f29](https://github.com/pawamoy/duty/commit/b412f292a9a2b81d44a5e1bcba5a4aa3211d329c) by Timothée Mazzucotelli).
- Add duties module to `sys.modules` after loading it ([5730f5f](https://github.com/pawamoy/duty/commit/5730f5f4c921b3694f0d6e48af3d54e049648f3e) by Timothée Mazzucotelli).

## [0.11.1](https://github.com/pawamoy/duty/releases/tag/0.11.1) - 2023-05-23

<small>[Compare with 0.11.0](https://github.com/pawamoy/duty/compare/0.11.0...0.11.1)</small>

### Code Refactoring

- Print help and duties when no arguments are given ([eaab432](https://github.com/pawamoy/duty/commit/eaab4324b8581fbd9ef2208ab3b0ecb625adb8bd) by Timothée Mazzucotelli). [Issue #11](https://github.com/pawamoy/duty/issues/11)

## [0.11.0](https://github.com/pawamoy/duty/releases/tag/0.11.0) - 2023-04-13

<small>[Compare with 0.10.0](https://github.com/pawamoy/duty/compare/0.10.0...0.11.0)</small>

### Features

- Add callable for `ssort` ([11b54da](https://github.com/pawamoy/duty/commit/11b54dab2f36efbac0650b825ed2e3ce73e9afac) by Timothée Mazzucotelli).

## [0.10.0](https://github.com/pawamoy/duty/releases/tag/0.10.0) - 2023-04-10

<small>[Compare with 0.9.0](https://github.com/pawamoy/duty/compare/0.9.0...0.10.0)</small>

### Features

- Support updated lazy decorator from `failprint` ([a0446ac](https://github.com/pawamoy/duty/commit/a0446ac20672344ab9508d661e21ff5b5132742b) by Timothée Mazzucotelli).

## [0.9.0](https://github.com/pawamoy/duty/releases/tag/0.9.0) - 2023-03-07

<small>[Compare with 0.8.0](https://github.com/pawamoy/duty/compare/0.8.0...0.9.0)</small>

### Features

- Add callable for Interrogate ([9be8068](https://github.com/pawamoy/duty/commit/9be80680c0d0ab5fbe62e6a117ed655d68da7967) by jexio). [PR #8](https://github.com/pawamoy/duty/pull/8)

## [0.8.0](https://github.com/pawamoy/duty/releases/tag/0.8.0) - 2023-02-18

<small>[Compare with 0.7.0](https://github.com/pawamoy/duty/compare/0.7.0...0.8.0)</small>

### Features

- Make all callables lazy, allowing to call them directly ([a499e4b](https://github.com/pawamoy/duty/commit/a499e4b42a26eee28d921d818f92b7747a8f3cad) by Timothée Mazzucotelli).
- Provide callables for popular tools ([0e065e2](https://github.com/pawamoy/duty/commit/0e065e2be722d26d8c2f0e38f4d593f140da1f5d) by Timothée Mazzucotelli). [Issue #7](https://github.com/pawamoy/duty/issues/7)
- Add option to skip duties based on condition ([629b988](https://github.com/pawamoy/duty/commit/629b988880de8b7c3f5b42fcbdb2ec9018c29dbc) by Timothée Mazzucotelli). [Issue #6](https://github.com/pawamoy/duty/issues/6)

## [0.7.0](https://github.com/pawamoy/duty/releases/tag/0.7.0) - 2021-08-01

<small>[Compare with 0.6.0](https://github.com/pawamoy/duty/compare/0.6.0...0.7.0)</small>

### Features
- Make `ctx.run` return the command output ([1810623](https://github.com/pawamoy/duty/commit/1810623a67bd102aceb56b3285064753d58d464e) by Timothée Mazzucotelli). [Issue #4](https://github.com/pawamoy/duty/issues/4)
- Add `allow_overrides` and `workdir` options ([ddbf7a2](https://github.com/pawamoy/duty/commit/ddbf7a260dc0bcb06603400197d514e63e77253d) by Timothée Mazzucotelli). [Issue #1](https://github.com/pawamoy/duty/issues/1)
- Allow passing standard input to a command (thanks to [*failprint* 0.8](https://pawamoy.github.io/failprint/changelog/#080-2021-07-31)). [Issue #3](https://github.com/pawamoy/duty/issues/3)

### Bug Fixes
- Make duties unwrappable ([c96325a](https://github.com/pawamoy/duty/commit/c96325a302ca52670bf33c8950c24d1fd441280f) by Timothée Mazzucotelli).


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

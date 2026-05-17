module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'build', 'chore', 'ci', 'docs', 'feat', 'fix',
      'perf', 'refactor', 'revert', 'style', 'test',
    ]],
    'scope-enum': [2, 'always', [
      'clean-architecture',
      'dx-heuristics',
      'test-heuristics',
      'project-agentification',
      'example-minimal',
      'schemas',
      'scripts',
      'hooks',
      'repo',
      'ci',
      'deps',
    ]],
    'scope-empty': [0],
    'subject-case': [0],
    'header-max-length': [2, 'always', 100],
    'body-max-line-length': [1, 'always', 100],
  },
};

# Amazon AWS - Jinja2 based ECS renderer

[![Known Vulnerabilities](https://snyk.io/test/github/lejmr/amazon-ecs-render-task-definition/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/lejmr/amazon-ecs-render-task-definition?targetFile=requirements.txt)
[![codecov](https://codecov.io/gh/lejmr/amazon-ecs-render-task-definition/branch/main/graph/badge.svg?token=OQ8J2Z71MM)](https://codecov.io/gh/lejmr/amazon-ecs-render-task-definition)
![Unit tests](https://github.com/lejmr/amazon-ecs-render-task-definition/workflows/Unit%20tests/badge.svg)

The goal of this project is to deliver a very simple templating library that can generate Amazon ECS - Task definition which can be later used by other tools to update the relevant ECS Task definition or even ECS Service. Since I like to work with [Helm](https://helm.sh/), this library produces similar output like `helm template` command, but in Amazon AWS ECS notion. The main motivation for templating is deployment to different environmnents where some variables or even a combinaton of containers can be different within a task. For example database container is added to the Task when deploying to DEV environment. 

This libary is implemented in Python using [TDD](https://www.agilealliance.org/glossary/tdd/), and templates are expected in the [Jinja2](https://jinja.palletsprojects.com/) templating language. All particular templates and value files can be written in [JSON](https://www.json.org/json-en.html) and [YAML](https://yaml.org/) format. All contributions are welcomed!

The library is available as [docker image](https://hub.docker.com/r/lejmr/amazon-ecs-render-task-definition) and [GitHub Action](https://github.com/marketplace/actions/amazon-ecs-task-definition-jinja2-based-renderer).


## Example

Example directory structure available in a separate [GitHub repository](https://github.com/lejmr/test-ecs-render.git).

```
├── complex-task-definition
│   ├── app.yaml
│   ├── db.yaml
│   └── task_properties.yaml
├── simple-task-definition.json
└── values
    ├── DEV.json
    └── PROD
        ├── environment.yaml
        └── extra.yml
```

```
# docker run --rm -v $PWD:/src -e INPUT_TASK-DEFINITION=simple-task-definition.json lejmr/amazon-ecs-render-task-definition
::set-output name=task-definition::task-definition-rendered.json
# cat task-definition-rendered.json
{
    "family": "test",
    "image": "latest"
}

```

Remember: The particular configuration files should only contain item which are compatible with `--cli-input-json` `aws ecs register-task-definition` command, as the generated file is expected to be used as follows:

```
aws ecs register-task-definition --cli-input-json file://XXXXXX.json
```


### Jenkins

WIP
TODO:  Extend the entrypoint, so the GitHub Actions are enforced.

### GitHub Actions
Look at [examples](https://github.com/lejmr/test-ecs-render/). The most prominent example uses `complex-task-definition` which is actually an directory containing fragments of configuration for the task definition and `values/PROD` for values which are used for interpolation.

This is how template can be constructed from two directories containing particular json/yaml files
```
  - name: Example of simple template
    uses: lejmr/amazon-ecs-render-task-definition@v1
    with:
      task-definition: complex-task-definition
      values: values/PROD

  - name: Deploy to Amazon ECS service
    uses: aws-actions/amazon-ecs-deploy-task-definition@v1
    with:
      task-definition: ${{ steps.render-web-container.outputs.task-definition }}
      service: my-service
      cluster: my-cluster
```




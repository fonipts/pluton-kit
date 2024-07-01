# pluton-kit
Create your project from the current selection we had on the lobby, But in the future we are working to share your ideas with other developer.

[![PIP version][pip-image]][pip-url] 

[Site](https://plutonkit.codehyouka.xyz/) |
[Docs](https://plutonkit.codehyouka.xyz/api) |
[Architecture lobby](https://github.com/fonipts/pluton-lobby) |

## Introduction
Building from scratch is quite a dauting task. Constructing your thought, looking for feature and research it will take alot of your time in figuring what will you do next. Therefore I decided to create application where you can choose in different framework, either zero or hero it will help you alot visualize what framework will you choose.

## Installation
In your local machine
```html
pip install -e .
```
In using Pip install
```html
pip install plutonkit
```

## Why we need another project template
There are several template generator that is available public repository, but they lack of user control in favored of there likes.
- to have condition, for feature that you want and available in architecture.
- Custom template that makes this project unique.


## Roadmap
Currently we are in alpha phase had not reach 100% test coverage and some linter(due to feature I am currently in focused) but still committed to deliver the improvement if the tool.

## Available command you can use at your terminal
The commands must in this format  `plutonkit <Command type>` 
|Command type | Description| Example |
|------------- | ------------- | ------------- |
|create_project | Start creating your project in our listed framework  | `plutonkit create_project`|
|command | Executing command using plutonkit | `plutonkit command start`|
|help | See available command for plutonkit | `plutonkit help` |

![Alt text](resources/pluton-kit-terminal-design.gif?raw=true "Title")


[pip-url]: https://pypi.org/project/plutonkit/
[pip-image]: https://img.shields.io/badge/plutonkit-0.01alpha0-brightgreen

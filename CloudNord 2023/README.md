###### CFP • SUBMISSION
# DevOpsCon London 2023


> **Submission platform**: https://conference-hall.io/speaker/event/SkVFHQ5kzrrfUlSU4MK1<br>
> **Deadline**: 15/06/2023<br>
> **Announcement of selected talks**: ???
> **Link**: https://www.cloudnord.fr/

<br>

## Universal Project Specification
#### How to create a technology agnostic and an ubiquitous project folders structure

Building software today is easier that before. Nowadays, we got IDEs, Frameworks, and Tools which speed up our work or make us more productive. At the early stage of your development process, we have at our disposal tools: 

* To scaffold our project folder
* To setup our development environment 
* To add third-party libraries and dependencies to our project
* And more.

As a result, those frameworks and tools tend to shift our focus far from the business problem we're trying to solve. In fact, we put too much emphasis on how to use thoses frameworks and tools, and less on how we should architect our applications. The aim of our business logic is being hidden by either frameworks or/and tools. As Uncle Bob([@unclebobmartin](https://twitter.com/unclebobmartin)) quoted in [his talk about clean architecture](https://youtu.be/o_TH-Y78tt4?t=10m42s) : 

  > Why does the higher level directory structure of this application tell me the framework I am using; Why doesn't it tell me what the application does ? <br>- Robert C. Martins (Uncle Bob)

For me, this means that we should not let those frameworks hide our buisness logic, but instead, make our application business needs drive the way we use those frameworks. Moreover, the higher level directory structure of your application must either tell what your application does or nothing. The directory structure of your application must be frameworks neutral. But what does ***neutral*** means ? By neutral I mean that at first glance of an application structure you shouldn't be able to guess want framework the application is using. 

Together we will explore a specification that will give you guidelines and rules that will help you shape/design a universal directory structure that puts less emphasis on the framework and tools, but focuses more on the business problem, you're trying to solve.


## Elevator Pitch 

Building software today is easier that before. Nowadays, we got IDEs, Frameworks, and Tools which speed up our work or make us more productive. As a result, those frameworks and tools tend to shift our focus far from the business problem we're trying to solve. In fact, we put too much emphasis on how to use those frameworks and tools, and less on how we should architect our applications. The aim of our business logic is being hidden by either frameworks or/and tools.

Moreover, the higher level directory structure of your application must either tell what your application does or nothing; your application folder structure must be — almost — frameworks neutral.

Together we will explore a specification that will give you guidelines and rules that will help you shape/design a universal directory structure that puts less emphasis on the framework and tools, but focuses more on the business problem, you're trying to solve.


## Abstract

Building software today is easier that before. Nowadays, we got IDEs, Frameworks, and Tools which speed up our work or make us more productive. As a result, those frameworks and tools tend to shift our focus far from the business problem we're trying to solve. In fact, we put too much emphasis on how to use those frameworks and tools, and less on how we should architect our applications. The aim of our business logic is being hidden by either frameworks or/and tools. Moreover, the higher level directory structure of your application must either tell what your application does or nothing; your application folder structure must be — almost — framework neutral. Together, we will explore a specification that will give you, guidelines and rules, that will help you shape/design a universal directory structure that puts less emphasis on the framework and tools, but focuses more on the business problem, you're trying to solve.


## Summary

At the end of the talk, the attendees will — not only — learn what this new specifications is all about, but to how you can leverage the guidelines and rules it provides, to create folder structure that puts less emphasis on the framework and tools, but focuses more on the business problem, you're trying to solve.



## Requirements

None

## Keywords

`scafolding`, `delivery pipeline`, `devops`, `CI/CD pipeline`, `best practices`

## References

1. https://github.com/tsklabs/ups/blob/master/specification.md
2. https://gist.github.com/lktslionel/2e59385f33da873f773a30d022a4ce1e

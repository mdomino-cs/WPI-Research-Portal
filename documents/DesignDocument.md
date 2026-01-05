# Project Design Document

## Your Project Title
--------
Prepared by:

* `Michael D`,`Student`
* `Frankie D`,`Student`
* `Andrew P`,`Student`
* `Chris C`,`Student`
* `Max J`,`Student`
---

**Course** : CS 3733 - Software Engineering 

**Instructor**: Sakire Arslan Ay

---

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Software Design](#2-software-design)
    - [2.1 Database Model](#21-model)
    - [2.2 Modules and Interfaces](#22-modules-and-interfaces)
    - [2.2.1 Overview](#221-overview)
    - [2.2.2 Interfaces](#222-interfaces)
    - [2.3 User Interface Design](#23-view-and-user-interface-design)
- [3. References](#3-references)
- [Appendix: Grading Rubric](#appendix-grading-rubric)

<a name="revision-history"> </a>

### Document Revision History

| Name | Date | Changes | Version |
| ------ | ------ | --------- | --------- |
|Revision 1 |2025-11-12 |Initial draft | 1.0        |
|      |      |         |         |


# 1. Introduction

Explain the purpose of this document. If this is a revision of an earlier document, please make sure to summarize what changes have been made during the revision (keep this discussion brief). 

# 2. Software Design

(**Note**: For all subsections of Section-2: You should describe the design for the end product (completed application) - not only your iteration1 version. You will revise this document and add more details later.)

## 2.1 Database Model

Provide a list of your tables (i.e., SQL Alchemy classes) in your database model and briefly explain the role of each table. 

Provide a UML diagram of your database model showing the associations and relationships among tables. 

## 2.2 Modules and Interfaces

### 2.2.1 Overview
Describe the high-level architecture of your software:  i.e., the major modules/blueprints and how they fit together. Provide a UML component diagram that illustrates the architecture of your software. Briefly mention the role of each module in your architectural design. Please refer to the "System Level Design" lectures in Week 4. 

### 2.2.2 Interfaces

Include a detailed description of the routes your application will implement. 
* Brainstorm with your team members and identify all routes you need to implement for the **completed** application.
* For each route specify its “methods”, “URL path”, and “a description of the operation it implements”.  
* You can use the following table template to list your route specifications. 
* Organize this section according to your module decomposition, i.e., include a sub-section for each module/blueprint and list all routes for that sub-section in a table.  

#### 2.2.2.1 \auth Routes

|   | Methods           | URL Path   | Description  |
|:--|:------------------|:-----------|:-------------|
|1. |  GET              | /auth/login| render login |
|2. |  POST             | /auth/login| login locally|
|3. |  GET              | /auth/callback| Auth0 callback|
|4. |  POST             | /auth/logout| End session |
|5. |  GET              | /auth/faculty/activate|Start activation|
|6. |  POST             | /auth/faculty/activate| Submit activation |

#### 2.2.2.2 \students Routes

|   | Methods           | URL Path   | Description  |
|:--|:------------------|:-----------|:-------------|
|1. | GET               | /students/profile| view profile|
|2. | GET               | /student/profile/edit| edit profile fields|
|3. | POST              | /student/profile| save profile updates  |
|4. | GET               | /student/dashboard|              |
|5. | GET               | /student/recommended|              |
|6. | GET               | /student/applications|              |

#### 2.2.2.3 \faculty Routes

|   | Methods           | URL Path   | Description  |
|:--|:------------------|:-----------|:-------------|
|1. | GET               | /faculty/profile|              |
|2. | POST               | /faculty/profile/edit|              |
|3. | POST              | /student/profile|              |
|4. | GET               | /student/dashboard|              |
|5. | GET               | /student/recommended|              |
|6. | POST               | /student/applications|              |

Repeat the above for other modules you included in your application. 

### 2.3 User Interface Design 

Provide UI sketches or screenshots for the following pages:
 * Faculty main page
 * Student main page (show how you will display "all positions" vs "recommended positions")
 * Faculty creating a position 
 * Faculty accepting /rejecting an application
 * Student applying a position

# 3. References

Cite your references here.

For the papers you cite give the authors, the title of the article, the journal name, journal volume number, date of publication and inclusive page numbers. Giving only the URL for the journal is not appropriate.

For the websites, give the title, author (if applicable) and the website URL.

----
# Appendix: Grading Rubric
(Please remove this part in your final submission)

 * You will first  submit a draft version of this document:
    * "Project 3 : Project Design Document - draft" (5pts). 
* We will provide feedback on your document and you will revise and update it.
    * "Project 5 : Project Design Document - final" (80pts) 

Below is the grading rubric that we will use to evaluate the final version of your document. 

|**MaxPoints**| **Design** |
|:---------:|:-------------------------------------------------------------------------|
|           | Are all parts of the document in agreement with the product requirements? |
| TBA         | Is the architecture of the system ([2.2.1 Overview](#221-overview)) described well, with the major components and their interfaces?         
| TBA        | Is the database model (i.e., [2.1 Database Model](#21-database-model)) explained well with sufficient detail? Do the team clearly explain the purpose of each table included in the model?| 
|          | Is the document making good use of semi-formal notation (i.e., UML diagrams)? Does the document provide a clear UML class diagram visualizing the DB model of the system? |
| TBA        | Is the UML class diagram complete? Does it include all classes (tables) and does it clearly mark the PK and FKs for each table? Does it clearly show the associations between them? Are the multiplicities of the associations shown correctly? ([2.1 Database Model](#21-database-model)) |
| TBA        | Are all major interfaces (i.e., the routes) listed? Are the routes explained in sufficient detail? ([2.2.2 Interfaces](#222-interfaces)) |
| TBA        | Is the view and the user interfaces explained well? Did the team provide the screenshots of the interfaces they built so far.  ([2.3 User Interface Design](#23-user-interface-design)) |
|           | **Clarity** |
|           | Is the solution at a fairly consistent and appropriate level of detail? Is the solution clear enough to be turned over to an independent group for implementation and still be understood? |
| TBA         | Is the document carefully written, without typos and grammatical errors?  |
| TBA         | Is the document well formatted? (Make sure to check your document on GitHub. You will loose points if there are formatting issues in your document.  )  |
|           |  |
|          | **Total** |
|           |  |
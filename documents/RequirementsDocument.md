# Software Requirements and Use Cases

## Your Project Title
--------
Prepared by:

* `Michael Domino`,`WPI Student - PyPartners`
* `Andrew Pereira`,`WPI Student - PyPartnerst`
* `Maximilian Jansen`,`WPI Student - PyPartners`
* `Frankie DeWander`,`WPI Student - PyPartners`
* `Chris Cardoopoli`, `WPI Student - PyPartners`

---

**Course** : CS 3733 - Software Engineering

**Instructor**: Sakire Arslan Ay

---

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Requirements Specification](#2-requirements-specification)
  - [2.1 Customer, Users, and Stakeholders](#21-customer-users-and-stakeholders)
  - [2.2 User Stories](#22-user-stories)
  - [2.3 Use Cases](#23-use-cases)
- [3. User Interface](#3-user-interface)
- [4. Product Backlog](#4-product-backlog)

<a name="revision-history"> </a>

## Document Revision History

| Name | Date | Changes | Version |
| ------ | ------ | --------- | --------- |
|Revision 1 |2025-11-04 |Initial Setup | 1.0        |
|      |      |         |         |
|      |      |         |         |

----
# 1. Introduction

This project is a web application that will be deployed to AWS and is desgined to connect WPI faculty with undergrad students interesting in doing research. The platform allows the studesnts to create profiles, list their skills and coursework, browse and apple for research positions and also track application statuc. The faculty can post opportunites, view applications, and manage selections. The goal of this is to make it easier for students to find and apply for positions while allowing for faculty an easy way to view qualified candidates.

----
# 2. Requirements Specification

The software system must allow both students and faculty to interact in a user-friendly interface. Students will need to create accounts, build and edit their profiles containing their academic information, research research_topics, and technical skills, and then browse/view and apply for open research positions posted by faculty. Each student should be able to monitor the real-time status of their applications and references, and the system should automatically suggest jobs that best fit their profile. Faculty users must be able to create and manage research postings, validate and activate their accounts, assess student applications, and accept or reject applicants according to their credentials. Predefined lists of majors, courses, research subjects, and programming languages must also be kept up to date by the system. These lists must be updated as needed by faculty members with administrative access. The platform should also have JavaScript-enhanced interactive features to improve usability and enable secure authentication using WPI credentials or Auth0 single sign-on. This will ensure a smooth user experience and reliable access.

## 2.1 Customer, Users, and Stakeholders

## Customers

* **WPI:** wants a centralized, efficient way to promote research roles to connect faculty with qualified undergrads.
* **Course staff (instructor: Sakire Arslan Ay/PLAs: Kim Cummings, Mina Boktor, and Katherine Tse for CS 3733):** treat the app as the capstone deliverable; care about logistics, iteration, and maintainability.

## Stakeholders

* **Faculty (position creators & interviewers):** need to reach sophomores/juniors beyond their current classes, filter by qualifications, and manage approvals within team-size limits.
* **Undergraduate students (applicants):** need clear listings, good matching, easy applications, and transparent status tracking.
* **Faculty references:** want a simple approve/decline flow when students list them.
* **WPI IT / Auth provider (SSO):** cares about secure authentication and minimal support overhead.
* **University programs/research offices:** benefit from broader participation and better visibility into opportunities.

## Users

* **Student users:** create/edit profiles; browse, get recommendations, and apply; and track/withdraw applications.
* **Faculty users:** activate the accounts, post positions, review all applicants, approve/reject said applicants, and manage recommendation requests.
* **Faculty:** respond to recommendation requests.
* **Faculty:** update predefined lists (majors, courses, topics, languages, instructors, grades) to keep data consistent.


----
## 2.2 User Stories

### Student

1.  **As a student,** I want to create an account so I can access the platform.
2.  **As a student,** I want to view and edit my profile with my contact info, GPA, majors, programming languages, interest and advanced coursework with course/grade/instructor, so that faculty can evaluate me.
3.  **As a student,** I want to pick majors, courses, grades, instructors, research topics, and programming languages from predefined lists so data stays consistent.
4.  **As a student,** I want to log in with my WPI credentials or Auth0 SSO so I can securely access my account.
5.  **As a student,** I want to browse all available research positions so I can see all possible opportunities.
6.  **As a student,** I want to see full position details with title, faculty contact, description, dates, team size, topics, preferred major, topics, min GPA, expected coursework, expected languages and reference required, so I can judge my fit for the position.
7.  **As a student,** I want to see recommended positions ranked by relevance to my profile so I can focus my effort on the best matches.
8.  **As a student,** I want to apply to positions so I can be considered.
9.  **As a student,** I want to submit a brief interest statement along with each application so I can explain why I would be a good fit for the position.
10. **As a student,** when a reference is required for a position, I want to choose a registered faculty member to be my reference, so my application meets the requirements.
11. **As a student,** I want the system to notify my listed faculty reference as well as setting the recommendation status to “Awaiting approval” so that the process can proceed.
12. **As a student,** I want to track my applications and see the status of each as either Pending, Approved or Rejected and the reference statuses as either Recommended or Not Recommended on my dashboard so I always know my situation.
13. **As a student,** I want to withdraw applications that are still Pending so I can remove myself from being considered for that position.
14. **As a student,** I want the system to prevent withdrawing approved applications so my commitments are respected.

### Faculty

1.  **As a faculty member,** I want to activate my preloaded account by locating my name/email and verifying via email so I can use the system.
2.  **As a faculty member,** I want my basic contact info to be populated from preloaded data and to set my username/password so setup is quick.
3.  **As a faculty member,** I want to log in with my WPI credentials or Auth0 SSO so I can securely access my account.
4.  **As a faculty member,** I want to view my profile and any recommendation requests so I can manage them from one place.
5.  **As a faculty member,** I want to approve or reject recommendation requests so I can provide or deny references.
6.  **As a faculty member,** I want to create and manage multiple undergraduate research positions so I can recruit for my projects.
7.  **As a faculty member,** I want to enter position details (title, description, dates, team size, preferred major, min GPA, topics, required languages, required coursework, whether a reference is required) so students understand requirements.
8.  **As a faculty member,** I want to select majors, topics, programming languages, and courses from predefined lists so postings are consistent.
9.  **As a faculty member with admin privileges,** I want to add/update/remove items in the predefined lists (majors, courses, instructors, grades, topics, languages) so the catalog stays current.
10. **As a faculty member,** I want to see all students who applied to my positions so I can review candidates.
11. **As a faculty member,** I want to view each applicant’s profile (contact info, majors, GPA, research_topics, languages, completed coursework with grade/instructor), their listed reference and recommendation status, and whether they’re already approved for another position so I can make informed decisions.
12. **As a faculty member,** I want to approve applications up to the team-size limit so I can fill my team appropriately.
13. **As a faculty member,** I want to reject applications that don’t meet qualifications so I can manage my applicant pool.

----
## 2.3 Use Cases

| Use case # 1      |   |
| ------------------ |--|
| Name              | Create Student Profile  |
| Participating actor  | Student  |
| Entry condition(s)     | Student is on sign-up page.  |
| Exit condition(s)           | Profile saved with contact info, majors, GPA, research_topics, programming languages, and advanced coursework (course, grade, instructor).  |
| Flow of events | Student creates an account by setting a username and password. Student enters contact info (first and last name, unique WPI ID and unique email). Student selects remaining values from predefined lists (majors, courses, grades, instructors, research topics, languages). System saves user responses to an associated profile and prompts user with success. Student can later view/edit the profile.  |
| Alternative flow of events    | If invalid information is given (such as non-unique username, ID, or email ), prompt the user to try again with valid info.  |

| Use case # 2      |   |
| ------------------ |--|
| Name           _    | Student Login  |
| Participating actor  | Student  |
| Entry condition(s)     | Student is on login page.  |
| Exit condition(s)           | Student successfully logs in.  |
| Flow of events | Student chooses login method (WPI email/password or Auth0 SSO). System authenticates and routes to student area.  |
| Alternative flow of events    | Student input does not authenticate, System warns user and prompts to retry or redirects to sign up.  |

| Use case # 3      |   |
| ------------------ |--|
| Name   _           | Browse Research Positions  |
| Participating actor  | Student  |
| Entry condition(s)     | Student is authenticated and has a profile.  |
| Exit condition(s)           | List of open positions shown with key info.  |
| Flow of events | Student navigates to page. System shows all open positions with title and posting faculty. System has a separate list of most recommended positions that are ranked by relevance to Student’s profile. Student selects a position to view full details.  |
| Alternative flow of events    | None.  |

| Use case # 4      |   |
| ------------------ |--|
| Name              | View Position Details  |
| Participating actor  | Student  |
| Entry condition(s)     | Student selected a position from list.  |
| Exit condition(s)           | Full position detail displayed.  |
| Flow of events | System renders all listed fields from the posting.  |
| Alternative flow of events    | None.  |

| Use case # 6      |   |
| ------------------ |--|
| Name              | Apply to Position  |
| Participating actor  | Student, Faculty  |
| Entry condition(s)     | Student is viewing a position.  |
| Exit condition(s)           | Application created with status Pending; if reference required, recommendation set to Awaiting approval for the listed faculty.  |
| Flow of events | Student clicks Apply. Student enters a short interest statement. If the position requires a reference, Student selects a registered faculty reference. System creates the application (status Pending) and (if reference required) notifies the reference; recommendation status = Awaiting approval. _ |
| Alternative flow of events    | If no reference required: System skips reference steps and just records the application as pending.  |

| Use case # 7      |   |
| ------------------ |--|
| Name              | Track Applications & Reference Status  |
| Participating actor  | Student  |
| Entry condition(s)     | Student has submitted one or more applications and is logged in.  |
| Exit condition(s)           | Dashboard shows up-to-date application and recommendation statuses.  |
| Flow of events | Student opens My Applications. System shows each application status either Pending / Approved / Rejected. System shows each recommendation status either Recommended / Not Recommended. The system displays the information on the student dashboard.  |
| Alternative flow of events    | None.  |

| Use case # 8   _    |   |
| ------------------ |--|
| Name              | Withdraw Pending Application  |
| Participating actor  | Student  |
| Entry condition(s)     | Application exists with status Pending.  |
| Exit condition(s)           | Application marked withdrawn (removed from consideration).  |
| Flow of events | Student opens a Pending application. Student chooses Withdraw. System confirms and withdraws the application.  |
| Alternative flow of events    | If the application is Approved, withdrawal is not allowed.  |

| Use case # 9      |   |
| ------------------ |--|
| Name              | Activate Faculty Account  |
| Participating actor  | Faculty  |
| Entry condition(s)   d | Faculty exists in the pre-loaded list.  |
| Exit condition(s)           | Faculty account activated.  |
| Flow of events | Faculty locates their name/email in the preloaded list. System sends verification email. Faculty completes verification and sets username/password, the contact info auto-populates.  |
| Alternative flow of events    | None.  |

| Use case # 10      |   |
| ------------------ |--|
| Name              | Faculty Login  |
| Participating actor  | Faculty  |
| Entry condition(s)     | Faculty account is activated.  |
| Exit condition(s) s s s | Faculty is logged in.  |
| Flow of events | Faculty logs in via WPI email/password or Auth0 SSO. System displays the home page.  |
| Alternative flow of events    | Choose either method (WPI or Auth0).  |

| Use case # 11      |   |
| ------------------ |--|
| Name              | Manage Recommendation Requests (as Reference)  |
| Participating actor  | Faculty  |
| Entry condition(s)     | Student listed this faculty member as a reference for a position that requires one.  |
| Exit condition(s)           | Recommendation marked Recommended or Not Recommended.  |
| Flow of events | Faculty views profile page where recommendation requests appear. Faculty approves or rejects each request.  |
| Alternative flow of events    | Approve ⇒ recommendation = Recommended. Reject ⇒ recommendation = Not Recommended.  |

| Use case # 12      |   |
| ------------------ |--|
| Name              | Create Research Position  |
| Participating actor  | Faculty  |
| Entry condition(s)     | Faculty is authenticated.  |
| Exit condition(s)           | New position saved with required metadata.  |
| Flow of events | Faculty creates a position and enters details: title, goals, start/end dates, team size, preferred major, expected min GPA, research topics, required programming languages, required coursework, whether a reference is required.  |
| Alternative flow of events    | Select predefined values where applicable (majors, topics, languages, coursework).  |

| Use case # 13      |   |
| ------------------ |--|
| Name              | Manage Predefined Lists (Faculty Admin)  |
| Participating actor  | Faculty  |
| Entry condition(s)     | Faculty is authenticated.  |
| Exit condition(s)           | Predefined lists updated (add/update/remove).  |
| Flow of events | Faculty admin opens catalog maintenance. Faculty admin adds/updates/removes items in lists (majors, courses, instructors, grades, research topics, programming languages).  |
| Alternative flow of events    | None.  |

| Use case # 14      |   |
| ------------------ |--|
| Name              | View Applicants for a Position  |
| Participating actor  | Faculty  |
| Entry condition(s)   s | Faculty owns at least one posted position.  |
| Exit condition(s)           | List of applicants displayed for the selected position.  |
| Flow of events | Faculty opens a position they created. System shows students who applied to that position.  |
| Alternative flow of events    | None.  |

| Use case # 15      |   |
| ------------------ |--|
| Name              | Review Applicant Details  |
| Participating actor  | Faculty  |
| Entry condition(s)     | Faculty is viewing the applicant list. s|
| Exit condition(s)           | Applicant details displayed.  |
| Flow of events | Faculty clicks an applicant. System shows contact info, majors, GPA, research research_topics, programming languages, completed coursework, the listed reference and its approval status, and whether the student is already approved for another position.  |
| Alternative flow of events    | None.  |

| Use case # 16      |   |
| ------------------ |--|
| Name              | Approve Applications  |
| Participating actor  | Faculty  |
| Entry condition(s)     | Faculty is viewing applications for a position.  |
| Exit condition(s) s s s | Selected applications marked approved.  |
| Flow of events | Faculty select one or more applicants that they intend to approve. System updates each to approved.  |
| Alternative flow of events    | If approving would exceed team size, remaining approvals are not permitted.  |

| Use case # 17      |   |
| ------------------ |--|
| Name              | Reject Applications  |
| Participating actor  | Faculty  |
| Entry condition(s)     | Faculty is logged in and viewing application.  |
| Exit condition(s) s s s | Selected application(s) marked rejected and visible to the student.  |
| Flow of events | Faculty selects an application to reject. System sets application status to rejected.  |
| Alternative flow of events    | None.  |

| Use case # 18      |   |
| ------------------ |--|
| Name              | Student Dashboard Status Updates  |
| Participating actor  | Student  |
| Entry condition(s)     | Application has been submitted/updated. s|
| Exit condition(s)         t | Dashboard shows the status of all the applications.  |
| Flow of events | System updates statuses based on the actions of faculty. Student opens dashboard and sees current statuses.  |
| Alternative flow of events    | None.  |

----
# 3. User Interface

  <kbd>
      <img src="images/application management.png"  border="2">
  </kbd>
  
  <kbd>
      <img src="images/application status dashboard.png"  border="2">
  </kbd>
  
  <kbd>
      <img src="images/browse research positions.png"  border="2">
  </kbd>
  
  <kbd>
      <img src="images/research position form.png"  border="2">
  </kbd>
  
  <kbd>
      <img src="images/student registration form.png"  border="2">
  </kbd>
  
  
----
# 4. Product Backlog

Here you should include a link to your GitHub repo issues page, i.e., your product backlog. Make sure to create an issue for each user story.  

https://github.com/WPI-CS3733-2025B/team-PyPartners/issues

----



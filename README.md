

## SECTION 1 : PROJECT TITLE
## Hotel Recommender System

<img src="SystemCode/Static/page.png"
     style="float: left; margin-right: 0px;" />

---

## SECTION 2 : EXECUTIVE SUMMARY / PAPER ABSTRACT
In the modern travel industry, online booking platforms have greatly facilitated travelers' accommodation choices. However, in the face of the vast amount of hotel resources, it is often difficult for users to make the most appropriate choice based on their own preferences. Traditional hotel search methods often rely on basic filters such as price, location, star rating, and so on. However, these approaches tend to ignore more personalized factors such as a user's historical choices or preferences for certain hotel amenities (e.g. gym, swimming pool, etc.). 

To solve this problem, hotel recommender systems have become an important means of providing personalized advice, able to make customized recommendations based on the user's needs. By leveraging data on both hotel facility characteristics and user preferences, the system can offer more accurate and targeted recommendations, ultimately simplifying the decision-making process and enhancing the user experience. With the increasing demand for personalized recommendations from travelers, the design of an efficient hotel recommendation system has become a key research direction to enhance the overall customer travel experience.

Our hotel recommender system is built with a Vue.js frontend that allows users to input preferences and view personalized recommendations through an intuitive interface. The backend, developed in Flask, manages data processing, user interactions, and serves as the core API. MySQL is used to store and organize hotel data, user profiles, and recommendation-related metrics. At the core of the recommendation logic is a collaborative filtering (CF) algorithm, leveraging cosine similarity to match users with relevant hotels based on historical preferences. To further enhance user experience, the system integrates a Python-based business rule engine that refines recommendations with rule-based adjustments, ensuring recommendations are both accurate and tailored to individual user needs. This combination of CF with business rules creates a well-rounded and highly adaptable hotel recommendation experience.

Our team is enthusiastically working on this hotel recommendation project, with the hope that users will engage with it and provide valuable feedback to improve the system further. We see potential for expanding the system’s reach internationally by enriching the database with diverse hotel options. By capturing variations across a broader range of hotels, we aim to provide users with even more accurate and personalized recommendations.

---

## SECTION 3 : CREDITS / PROJECT CONTRIBUTION

| Official Full Name  | Student ID (MTech Applicable)  | Work Items (Who Did What) | Email (Optional) |
| :------------ |:---------------:| :-----| :-----|
| Li Qiuxian | A0297598X | Backend Development, Debug recommend algorithm, Demo Presentation, Write Report| e1351736@u.nus.edu |
| Gao Yunjia | A0295502E | Recommend algorithm Development, NLP component development, UI-Design, Video Presentation, Write Report| e1349640@u.nus.edu  |
| Zhao Lanting | A0297676A | UI-Design, Frontend Development, Demo Presentation, Write Report| e1351814@u.nus.edu |
| Liu Weixuan | A0295682M | Recommend algorithm Development, Video Presentation, Collect and clean dataset, Write Report| e1349820@u.nus.edu |
| Huang Yongle Joshua | A0028090M | Business-Rule development, Rule text design, Architecture Diagram Design, Write Report| e0737921@u.nus.edu |

---

## SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO

[![Hotel Recommender System](https://raw.githubusercontent.com/A9gust/HotelRecommendationSystem/refs/heads/main/SystemCode/Static/v_page.png)](https://youtu.be/F4kCaQEHqL8 "Hotel Recommender System")

---

## SECTION 5 : USER GUIDE

`Refer to appendix <Installation & User Guide> in project report at Github Folder: ProjectReport`

### [ 1 ] Environment Requirement

> pip install requirements


### [ 2 ] To run the system in local machine:

> open terminal in our local fold file

> $ git clone https://github.com/A9gust/HotelRecommendationSystem.git

> $ cd HotelRecommendationSystem/backend

> $ python app.py

> $ cd HotelRecommendationSystem/hotel-recommendation

> $ npm run serve

> **Go to URL using web browser http://0.0.0.0:8080 or http://127.0.0.1:8080

---
## SECTION 6 : PROJECT REPORT / PAPER

`Refer to project report at Github Folder: ProjectReport`

**Recommended Sections for Project Report / Paper:**
- Introduction	
- Market Research	
- Business Value	
- Objectives of Project	
- Overview of Dataset	
- System Design		
- System Development & Implementation	
- Findings and Discussion	
- Appendix A: Project Proposal	
- Appendix B: Mapped System Functionalities Against Knowledge	
- Appendix C: Installation & User Guide	
- Appendix D: Individual Report

---
## SECTION 7 : MISCELLANEOUS

`Refer to Github Folder: Miscellaneous`

### la0730.csv
* Dataset of hotel name and information
* The most basic hotel database used by the system
### trainset.csv
* Combined with clustering result and rating matrix
* Use to train a model for CF algorithm



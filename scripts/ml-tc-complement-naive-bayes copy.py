import mysql.connector
import os
from dotenv import load_dotenv
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import (
    classification_report,
)
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import ComplementNB
from sklearn.model_selection import train_test_split


def classify():
    load_dotenv()
    # Database Connection to Pull Existing Meta Values

    mydb = mysql.connector.connect(
        user=(os.getenv("db_user")),
        password=(os.getenv("db_password")),
        host="localhost",
        database="thesis_vert",
    )

    # query = """SELECT text,textLabel_id, label FROM polls_trainingCorpus inner join polls_textlabels ON polls_textlabels.entryId = polls_trainingcorpus.textLabel_id"""

    query = """SELECT * FROM polls_trainingcorpus JOIN polls_textlabels ON polls_trainingcorpus.textLabel_id = polls_textlabels.entryId WHERE polls_trainingcorpus.textLabel_id IN (SELECT textLabel_id FROM polls_trainingcorpus GROUP BY textLabel_id HAVING COUNT(*) > 20)  AND textLabel_id <> 1;"""

    df = pd.read_sql(query, mydb)

    # define the text data and the target variable
    text_data = df["text"]
    target = df["label"]

    # convert the text data into a numerical representation
    vectorizer = CountVectorizer()
    x = vectorizer.fit_transform(text_data)

    # split the data into training and testing sets

    x_train, x_test, y_train, y_test = train_test_split(
        x, target, test_size=0.3, random_state=42
    )

    # build the Complement Naive Bayes classifier and fit it to the training data
    clf = ComplementNB()
    clf.fit(x_train, y_train)

    # evaluate the model's accuracy on the testing data
    accuracy = clf.score(x_test, y_test)
    print("Accuracy:", accuracy)

    # make predictions on new text data
    new_text_data = [
        """The FBI has seized the domains of a popular cybercrime marketplace after receiving a court warrant, in what it will be hoping is a serious blow to the site’s administrators.
        The action was the result of the Feds’ “Operation Cookie Monster” – a reference to the cookies sold on Genesis Market in huge volumes over the past five years, along with other data needed for logging in to third-party machines.
        As such, the site played a key role in the cybercrime supply chain, enabling threat actors to access victim networks for information theft, ransomware attacks, fraud and more.
        The FBI also referenced international law enforcement and private sector cooperation as helping with this operation, citing the UK’s National Crime Agency (NCA), Europol and other agencies as contributing.

        A total of 200 searches and close to 100 preventative actions were carried out across the globe, leading to 120 people arrested, including 24  in the UK.
        Read more on criminal markets here: US and Euro Police Smash Cybercrime Marketplace.
        At any one time there were apparently hundreds of thousands of listings on Genesis Market.
        Julia O’Toole, CEO of MyCena Security Solutions, branded the seizures a “big win” for law enforcement.
        “The operators of the site would collect data on internet users, including their login credentials, auto-filled passwords and their browser cookies in a bid to bypass MFA and access their online accounts,” she explained.
        “When they gained access to these, there would be no alerts the account was compromised as attackers simply logged in, so it was only after fraudulent activity occurred that the victim was made aware.”
        The operators of the site monetized their collection of victim account identities by selling them through bot services, with prices depending on the targeted asset(s) and duration of access.
        The FBI is still looking for information on the site’s administrators, which suggests that they are still at large. If that is the case, it would be reasonable to assume the site will return in some form or another and/or customers will migrate to rival marketplaces.
        The news comes just weeks after BreachForums was shuttered following the arrest of its administrator.""",
        """BOSTON, April 3, 2023 /PRNewswire-PRWeb/ -- Cybereason, the XDR company, todayannounced a $100 million investment led by SoftBank Corp. to support thecompany's global growth and advance its innovation in XDR, EDR, and EPPsolutions. In addition, Cybereason announced that Eric Gan will serve as thecompany's new CEO, subject to confirmation by the company's board and pendingcustomary regulatory approvals, while current CEO and Co-Founder Lior Div willtransition to the role of advisor.As an Executive Vice President of SoftBank Corp., Eric Gan has a long historywith Cybereason, starting with SoftBank Corp.'s initial investment in Cybereasonin 2015. Prior to SoftBank Corp., Gan co-founded eAccess, a telecommunicationscompany. Gan later became an Executive Vice President of SoftBank Corp., wherehe led its Business Development Unit, which formed alliances with overseascompanies. Before eAccess, Gan was an analyst and managing director for GoldmanSachs."I have watched Cybereason grow from its earliest stages to a leader in thecyber industry as evidenced by its recent position as a leader in the GartnerMagic Quadrant for EPP and its record-breaking MITRE ATT&CK results. I lookforward to supporting Cybereason's next stage of global growth and scale," saidGan."I am so proud of what we have accomplished at Cybereason and I look forward tobeing a part of helping the company move to the next level," said Div.This round of funding comes as Cybereason has experienced significant tractionin recent months including:Being named a Leader in the 2022 Gartner Magic Quadrant for Endpoint ProtectionPlatforms;Achieving the best results in the history of the MITRE Engenuity ATT&CK®Evaluations for Enterprise, scoring 100% in Prevention, 100% in Visibility, and100% in Real-Time Protection;Being named to the prestigious Forbes Cloud 100;Being named to CNBC's 10th Annual Disruptor 50 list of the most innovativeprivately held global companies.Cadwalader, Wickersham & Taft LLP is representing Cybereason in the financing,and Goodwin Procter LLP is representing Softbank Corp. in the financing.About CybereasonCybereason is the XDR company, partnering with Defenders to end attacks at theendpoint, in the cloud, and across the entire enterprise ecosystem. Only theAI-driven Cybereason Defense Platform provides predictive prevention, detection,and response that is undefeated against modern ransomware and advanced attacktechniques. The Cybereason MalOp(TM) instantly delivers context-rich attackintelligence across every affected device, user, and system with unparalleledspeed and accuracy. Cybereason turns threat data into actionable decisions atthe speed of business. Cybereason is a privately held international companyheadquartered in Boston with customers in more than 40 countries.Forward-Looking StatementsThis press release contains forward-looking statements. The words "believe,""may," "will," "potentially," "estimate," "continue," "anticipate," "intend,""could," "plan," "expect," and similar expressions that convey uncertainty offuture events or outcomes are intended to identify forward-looking statements.These forward-looking statements include, but are not limited to, statementsconcerning the following: (i) whether or not the conditions to closing upon someor all of the Financing occur and/or if the Financing occurs at all (in whole orin part), (ii) whether or not regulatory approvals are obtained and/or eventsconditioned on the receipt of regulatory approvals occur at all, (iii) thepotential for growth in the market for cloud-based security solutions(domestically and internationally) and future cybersecurity spending; (iv) ourbusiness plan and our ability to effectively manage our growth; (v) anticipatedtrends, growth rates and challenges in our business and in the markets in whichwe operate; and (vi) the ability of the Company to manage costs and findefficiencies and the sufficiency of our cash to meet our cash needs.These forward-looking statements are subject to a number of risks,uncertainties. It is not possible for the Company to predict all risks, nor canthe Company assess the impact of all factors on its business or the extent towhich any factor, or combination of factors, may cause actual results to differmaterially from those contained in any forward-looking statements. In light ofthese risks, uncertainties, and assumptions, the forward-looking events andcircumstances discussed in this press release may not occur and actual resultscould differ materially and adversely from those anticipated or implied in theforward-looking statements. The forward-looking statements made in this pressrelease relate only to events as of the date on which the statements are made.We undertake no obligation to update publicly any forward-looking statements forany reason to conform these statements to actual results or to changes in ourexpectations. In addition, statements that "we believe" and similar statementsreflect our beliefs and opinions on the relevant subject. These statements arebased upon information available to us as of the date of this press release,which may be limited or incomplete, and our statements should not be read toindicate that we have conducted an exhaustive inquiry into, or review of, allpotentially available relevant information. These and all other forward-lookingstatements are inherently uncertain and should not be relied upon.Learn more: https://www.cybereason.com/Follow us: Blog | Twitter | Facebook""",
    ]
    new_x = vectorizer.transform(new_text_data)
    new_predictions = clf.predict(new_x)
    print("New predictions:", new_predictions)


classify()

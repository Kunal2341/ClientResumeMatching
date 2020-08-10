# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.oauth2 import service_account
from google.cloud import language_v1
from google.cloud.language_v1 import enums
text_content = "Web developer, Gteko (purchased by Microsoft), Raanana, Israel"

keyDIR = "/Users/kunal/Documents/ResumeNLPVdart/APIKEYSGOOGLE/resumeMatcher-NLP_create_data.json"
credentials = service_account.Credentials.from_service_account_file(keyDIR)
client = language_v1.LanguageServiceClient(credentials=credentials)
type_ = enums.Document.Type.PLAIN_TEXT
language = "en"
document = {"content": text_content, "type": type_, "language": language}
encoding_type = enums.EncodingType.UTF8
response = client.analyze_entities(document, encoding_type=encoding_type)
# Loop through entitites returned from the API
for entity in response.entities:
    array = [entity.name, enums.Entity.Type(entity.type).name, entity.salience]
    print(u"Representative name for the entity: {}".format(entity.name))
    # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
    print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))
    # Get the salience score associated with the entity in the [0, 1.0] range
    print(u"Salience score: {}".format(entity.salience))
    # Loop over the metadata associated with entity. For many known entities,
    # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
    # Some entity types may have additional metadata, e.g. ADDRESS entities
    # may have metadata for the address street_name, postal_code, et al.
    for metadata_name, metadata_value in entity.metadata.items():
        print(u"{}: {}".format(metadata_name, metadata_value))

    # Loop over the mentions of this entity in the input document.
    # The API currently supports proper noun mentions.
    for mention in entity.mentions:
        print(u"Mention text: {}".format(mention.text.content))

        # Get the mention type, e.g. PROPER for proper noun
        print(
            u"Mention type: {}".format(enums.EntityMention.Type(mention.type).name)
        )
    print("")
def sample_analyze_sentiment(text_content):
    keyDIR = "/Users/kunal/Documents/ResumeNLPVdart/APIKEYSGOOGLE/resumeMatcher-NLP_create_data.json"
    credentials = service_account.Credentials.from_service_account_file(keyDIR)
    client = language_v1.LanguageServiceClient(credentials=credentials)
    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}
    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_sentiment(document, encoding_type=encoding_type)
    # Get overall sentiment of the input document
    print(u"Document sentiment score: {}".format(response.document_sentiment.score))
    print(
        u"Document sentiment magnitude: {}".format(
            response.document_sentiment.magnitude
        )
    )
    # Get sentiment for all sentences in the document
    for sentence in response.sentences:
        print(u"Sentence text: {}".format(sentence.text.content))
        print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
        print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(u"Language of the text: {}".format(response.language))

def sample_analyze_syntax(text_content):
    keyDIR = "/Users/kunal/Documents/ResumeNLPVdart/APIKEYSGOOGLE/resumeMatcher-NLP_create_data.json"
    credentials = service_account.Credentials.from_service_account_file(keyDIR)
    client = language_v1.LanguageServiceClient(credentials=credentials)
    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}
    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_syntax(document, encoding_type=encoding_type)
    # Loop through tokens returned from the API
    for token in response.tokens:
        # Get the text content of this token. Usually a word or punctuation.
        text = token.text
        print(u"Token text: {}".format(text.content))
        print(
            u"Location of this token in overall document: {}".format(text.begin_offset)
        )
        # Get the part of speech information for this token.
        # Parts of spech are as defined in:
        # http://www.lrec-conf.org/proceedings/lrec2012/pdf/274_Paper.pdf
        part_of_speech = token.part_of_speech
        # Get the tag, e.g. NOUN, ADJ for Adjective, et al.
        print(
            u"Part of Speech tag: {}".format(
                enums.PartOfSpeech.Tag(part_of_speech.tag).name
            )
        )
        # Get the voice, e.g. ACTIVE or PASSIVE
        print(u"Voice: {}".format(enums.PartOfSpeech.Voice(part_of_speech.voice).name))
        # Get the tense, e.g. PAST, FUTURE, PRESENT, et al.
        print(u"Tense: {}".format(enums.PartOfSpeech.Tense(part_of_speech.tense).name))
        # See API reference for additional Part of Speech information available
        # Get the lemma of the token. Wikipedia lemma description
        # https://en.wikipedia.org/wiki/Lemma_(morphology)
        print(u"Lemma: {}".format(token.lemma))
        # Get the dependency tree parse information for this token.
        # For more information on dependency labels:
        # http://www.aclweb.org/anthology/P13-2017
        dependency_edge = token.dependency_edge
        print(u"Head token index: {}".format(dependency_edge.head_token_index))
        print(
            u"Label: {}".format(enums.DependencyEdge.Label(dependency_edge.label).name)
        )

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(u"Language of the text: {}".format(response.language))

def sample_analyze_entity_sentiment(text_content):
    keyDIR = "/Users/kunal/Documents/ResumeNLPVdart/APIKEYSGOOGLE/resumeMatcher-NLP_create_data.json"
    credentials = service_account.Credentials.from_service_account_file(keyDIR)
    client = language_v1.LanguageServiceClient(credentials=credentials)
    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}
    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_entity_sentiment(document, encoding_type=encoding_type)
    # Loop through entitites returned from the API
    for entity in response.entities:
        print(u"Representative name for the entity: {}".format(entity.name))
        # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
        print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))
        # Get the salience score associated with the entity in the [0, 1.0] range
        print(u"Salience score: {}".format(entity.salience))
        # Get the aggregate sentiment expressed for this entity in the provided document.
        sentiment = entity.sentiment
        print(u"Entity sentiment score: {}".format(sentiment.score))
        print(u"Entity sentiment magnitude: {}".format(sentiment.magnitude))
        # Loop over the metadata associated with entity. For many known entities,
        # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
        # Some entity types may have additional metadata, e.g. ADDRESS entities
        # may have metadata for the address street_name, postal_code, et al.
        for metadata_name, metadata_value in entity.metadata.items():
            print(u"{} = {}".format(metadata_name, metadata_value))

        # Loop over the mentions of this entity in the input document.
        # The API currently supports proper noun mentions.
        for mention in entity.mentions:
            print(u"Mention text: {}".format(mention.text.content))
            # Get the mention type, e.g. PROPER for proper noun
            print(
                u"Mention type: {}".format(enums.EntityMention.Type(mention.type).name)
            )

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(u"Language of the text: {}".format(response.language))

def sample_classify_text(text_content):
    keyDIR = "/Users/kunal/Documents/ResumeNLPVdart/APIKEYSGOOGLE/resumeMatcher-NLP_create_data.json"
    credentials = service_account.Credentials.from_service_account_file(keyDIR)
    client = language_v1.LanguageServiceClient(credentials=credentials)
    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}
    response = client.classify_text(document)
    # Loop through classified categories returned from the API
    for category in response.categories:
        # Get the name of the category representing the document.
        # See the predefined taxonomy of categories:
        # https://cloud.google.com/natural-language/docs/categories
        print(u"Category name: {}".format(category.name))
        # Get the confidence. Number representing how certain the classifier
        # is that this category represents the provided text.
        print(u"Confidence: {}".format(category.confidence))
sentenceList = ['Oleg Kotliarsky',
 '(720) 987-8054',
 'olegkot@gmail.com',
 'Profile highlights:',
 'Web Development Engineer',
 'Vast experience designing, programming and leading enterprise web applications development',
 'Proficient in optimal UX solutions',
 'Great experience in developing reusable components to optimize development time and maintenance',
 'Ability to provide technical leadership and clear guidance to development team',
 'High skills to research, evaluate and implement right technical solution for the enterprise application',
 'Technical Knowledge:',
 'JavaScript, TypeScript, ReactJS, Action Script 3.0, Java, PHP',
 'Angular, AngularJS, RXJS, Karma, Java Spring, İBATIS, Apache Struts',
 'Oracle, MongoDB, SQL Server, MYSQL',
 'angular-cli, npm, bower, gulp, GIT',
 'Languages:',
 'Frameworks:',
 'Databases:',
 'Tools:',
 'Professional Experience: Aug. 2017 - April 2020 Senior Web Developer, Comcast, CO',
 'Designed and developed new app features (Columbo - ESL). (Angular6/Angular UI, Remedy, JAVA, Oracle DB):',
 'data driven "case create wizard" with back-end precheck and dynamic restructure of the steps',
 '- case resolve "stepper" with variable number of corresponding relative issues',
 '- reusable components - "keyword" search, attachments list, "add attachments", PDF viewer, util service with multitude of helper functions.',
 '- HTTP request wrappers, HTTP response interceptor for unified error handling',
 'Developed a web app (Columbo - Executive Support Line). (Hybrid AngularJS/Angular UI, Remedy, JAVA, Oracle DB); Maintain and support GIT Hub of the project',
 'Dec. 2013 – June 2017 Senior UI Developer / Team Lead / Scrum Master, DN2K, CO',
 'Developed customers, search, navigation modules for "MyDairyCentral" web app portal, sensors tiles carousel, responsive design, etc. (Angular4, angular-cli, Jasmine/Karma)',
 'Developed sensors tiles carousel, set karma unit tests framework for "MyGrowCentral" web app portal (AngularJS, Node, responsive design, JHipster, Jasmine/Karma)',
 'Developed different features of the "MyAGCentral" web app portal, including navigation tree, work orders flow, etc. (AngularJS, Node, Mongo) - client Sagelnsights: https://www.sageinsights.com/',
 'Transitioned from Backbone to Angular framework (team effort) of the "MyAGCentral" web app portal',
 'October 2011 - Dec. 2013 Web Developer Expert, Amdocs Inc., CO',
 'Developed "Order Entry" web application for entering order to the Amdocs Enterprise order management system (HTML5/CSS3, JavaScript/jQuery, AJAX/DWR, JSP/Java 7, Oracle, Java Spring, iBatis)',
 'Developed e-signature web app using previously developed JavaScript/jQuery/JSP/Java6/Spring2 framework for sending client\'s contract to "on-the-fly" signature creation (integration with docusign.com service).',
 'Developed part of the real time payment integration flow utilizing Amdocs EAI framework called JESI. (Java, JSP, SOAP, Oracle, JavaScript, jQuery)',
 'Developed Flex "Executive Advisor" report tool for serving different types of client statistics presented in a rich graphic interactive way (Flex 4.6, Blaze DS, Java, Oracle, Action Script 3)',
 'October 2010 – Oct. 2011 Web Developer Contractor, Rose International (for Amdocs Inc.), CO',
 'Developed iLink Mobile app (running on iPad Safari – used home developed framework) for sales representatives [client: DexOne]. (JavaScript, jQuery, jQTouch, AJAX, HTML5/webkit, Java, Spring, iBatis, Oracle, JSP);',
 'Developed an iPad web application framework for rapid development of iOS apps that look like',
 'March 2009 - October 2010 GSET Engineer, Wall Street on Demand (now Markit on Demand), Boulder, CO',
 'Developed Entitlements management intranet tool [client: Goldman Sachs]. (Java, Struts, Sybase, JSP, JavaScript, jQuery, AJAX);',
 'March 2008 – March 2009 Team Lead Developer, Wall Street on Demand (now Markit on Demand), Boulder, CO',
 'Leaded team of web developers, working on line of Stocks Research Websites [client: Schwab Institutional] (ASP, JavaScript, AJAX);',
 'August 2005 – March 2008 Senior Web Developer, Wall Street on Demand (now Markit on Demand), Boulder, CO',
 'Developed Web site architecture and determine software requirements.',
 'Created and optimized content for the Web site, including planning, design, integration and testing of Web-site related code.',
 'Planned and designed new featured web sites according to client requirements. Close interaction with graphic designers, project managers and QA members of our group;',
 'Developed Real Time DB driven web sites with Stocks market content, including price quotes graphics, charts, news, alerts etc. Schwab group projects (ASP, JScript, JavaScript, AJAX);',
 'April 2004 – August 2005 Freelancer Web Developer, Denver, CO',
 'Developed full code circle from templates to launch (PHP/MySql, JavaScript, HTML, CSS);',
 'Created Graphics: logos, bullets, complete design (Photoshop, Flash MX);',
 'Promoted web sites in search engines positioning (1st page positions in Google, Yahoo on several key words).',
 'April 2003 – April 2004',
 'Web developer, Gteko (purchased by Microsoft), Raanana, Israel',
 '- Developed JavaScript/VBScript active client side (ActiveX event\'s handling flow: version checking, upgrading, downloading and installation) of different "e-support" accounts (HP, Canon, AOL, Dell, NEC, Lenovo, etc)',
 'Developed JavaScript classes reflecting graphic presentation of ActiveX control downloading and installation processes;',
 'Developed a full JavaScript based interface for ActiveX control data processing - JavaScript/DOM/DHTML based model for PC scanned data show. Was a leading developer for GTWebCheck product part called "Upgrade Advisor" or "Summary Report".',
 'June 2002 – April 2003 Freelancer Web developer, Tel-Aviv , Israel',
 'Complete web sites production (Programming development, PHP/MYSQL/JavaScript/HTML/CSS index + forum (OOP);',
 "Created graphic design according to Client's requirements (logo, bullets, layout – Photoshop, Flash); Made domain name registration; Assisted in identity development, marketing, online promotion and launch;",
 'Maintained web mastering; Promoted web sites for search engines positioning August 1999 - May 2002',
 'Web Developer, Snapshield Ltd, Tel Aviv, Israel',
 "Created Web design (Photoshop, Flash) for Web based application for remote data management for tens of thousands of clients of the leading Snapshield's Telecom Encryption Service (SNAP);",
 'Programmed part of the SNAP application (Customer Care) using ASP, JavaScript, VBScript, CSS, IIS 4;',
 'Set required configuration for SSL on MS IIS4.',
 'Created web based client-side application "Snapshield\'s Security Algorithm Benchmark" for dynamic online calculating and show for different TI DSP platforms and Snapshield algorithms. (ASP, CSS, DHTML)',
 'Created Flash Animated Company Business and Technical Presentations (online, cds) in Macromedia',
 'Flash 5; Integrated video streaming to companies web site (JavaScript, DHTML)',
 'Created graphic and technical design, developed, published and web mastered three generations of the\ncompany\'s web site. (HTML/DHTML, JavaScript, CSS, Macromedia Flash 5, Adobe Photoshop 5.5;',
 'Assisted in new branding process (migrating from Microlink to Snapshield)',
 'Education:',
 'BS and MS in Mathematics and Mechanics',
 'St. Petersburg State University',
 'Courses:',
 '"Oracle Certified Associate", iTerra Consulting, Ic., Denver, USA.',
 '"Design for Multimedia", ORT Syngalovsky College, Tel Aviv. (800 hours)',
 '"JavaScript - DHTML – DOM", Sela group, Tel Aviv (30 hours)',
 '"OOD/OOP for C++ and Java", "Network TCP/IP", Tel-Ran, Rishon-Lezion (1000 hours)']



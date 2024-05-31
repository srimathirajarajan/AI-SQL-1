from langchain_core.prompts.prompt import PromptTemplate

template1 =  """You work normal chatbot and also Given below are the table structures in the mec_data database raw schema in SQL database: 

subject(SubjectID NUMBER ,SubjectTypeID NUMBER, Regulation NUMBER, SubjectCode VARCHAR, SubjectName VARCHAR, Descriptions VARCHAR, MinMark NUMBER, MaxMark NUMBER, CreditPoint NUMBER, UEMinMark NUMBER, UEMaxMark NUMBER, IEMinMark NUMBER, IEMaxMark NUMBER, IsActive NUMBER, UserID NUMBER, CreatedDate VARCHAR, ModifiedUserID NUMBER, ModifiedDate VARCHAR)

subjecttype(SubjectTypeID NUMBER, Description VARCHAR, IsActive NUMBER)

subjectxstaff(SubjectXStaffID NUMBER, CourseID NUMBER, CourseDepartmentID NUMBER, StudentBatchID NUMBER, Semester NUMBER, SectionID NUMBER, SubjectID VARCHAR, StaffID NUMBER, IsActive NUMBER)

subjectxsyllabus(SubjectXSyllabusID NUMBER, SubjectID NUMBER, SyllabusUnitID NUMBER, Syllabus VARCHAR, UserID NUMBER, CDate VARCHAR, MDate VARCHAR, IsActive NUMBER)

subjectxsyllabusdetail(SubjectXSyllabusDetailID NUMBER, SubjectID NUMBER, SyllabusUnitID NUMBER, Syllabus VARCHAR, UserID NUMBER, CDate VARCHAR, MDate VARCHAR, IsActive NUMBER)

subjectxtestdate(SubjectXTestDateID NUMBER, CourseID NUMBER, CourseDeptID NUMBER, StudentBatchID NUMBER, SectionID NUMBER, Semester NUMBER, SubjectID NUMBER, TestID NUMBER, TestDate VARCHAR, IsLock NUMBER, IsActive NUMBER)

dont use LIKE %  when you use SubjectName in query generation
 
Take user questions and respond back with SQL queries.

a potential for column name conflicts due to joining tables with common column names. Let's use aliases to distinguish between the columns

Example: 
user question : display the subject details.

your generated query : SELECT * from subject;

user question : show me all subjects taught by a staff whose staff id is 211

your generated query : SELECT sx.SubjectID, s.SubjectCode, s.SubjectName
FROM subjectxstaff sx
INNER JOIN subject s ON sx.SubjectID = s.SubjectID
WHERE sx.StaffID = 211;

user question : list the tables in our database
your generated query : Show tables;

user question : Provide me the columns present in subject table
your generated query : SELECT COLUMN_NAME
FROM mec_data.COLUMNS
WHERE TABLE_NAME = 'subject';

user question : retrieve the syllabus for a Service Oriented Architecture - E3 --> IT2401 - 08.

your generated query : SELECT s.SubjectName, ss.Syllabus
FROM subjectxsyllabus ss
INNER JOIN subject s ON ss.SubjectID = s.SubjectID
WHERE s.SubjectName = 'Service Oriented Architecture - E3 --> IT2401 - 08';

user question : can you retrive the  test dates whose subjectid is 7 and courseid is 3

your generated query : SELECT TestDate FROM subjectxtestdate WHERE SubjectID = 7 AND CourseID = 3;

user question : what subject type belongs to java programming 

your generated query : SELECT s.SubjectName, st.Description AS SubjectType FROM subject s
JOIN subjecttype st ON s.SubjectTypeID = st.SubjectTypeID
WHERE s.SubjectName  LIKE 'Java Programming%';

user question : give me details subject and subject staff id whose staff id is 3 and 4.
your generated query : SELECT 
    s.SubjectID AS SubjectID_subject,
    s.SubjectName AS SubjectName_subject,
    sx.StaffID AS StaffID_subjectxstaff
FROM 
    subject s
JOIN 
    subjectxstaff sx ON s.SubjectID = sx.SubjectID
WHERE 
    sx.StaffID IN (3, 4);



user question : give me details subject and subject staff id whose staff id is 4 and 6.
your generated query : SELECT 
    s.SubjectID AS SubjectID_subject,
    s.SubjectName AS SubjectName_subject,
    sx.StaffID AS StaffID_subjectxstaff
FROM 
    subject s
JOIN 
    subjectxstaff sx ON s.SubjectID = sx.SubjectID
WHERE 
    sx.StaffID IN (4, 6);

    
user question :display the only subject name   available in department 3
your generated query : SELECT DISTINCT s.SubjectName
FROM subject s
JOIN subjectxstaff sx ON s.SubjectID = sx.SubjectID
WHERE sx.CourseDepartmentID = 3;


user question : Display the tables in our database
your generated query : Show tables;

user question : Provide me the columns present in subject table
your generated query : SHOW COLUMNS IN TABLE MEC.subject;

User question: {input}
Your generated SQL query: """

ENTITY_MEMORY_CONVERSATION_TEMPLATE = PromptTemplate(
    input_variables=["input"],
    template=template1,
)

_DEFAULT_ENTITY_MEMORY_CONVERSATION_TEMPLATE = """You work normal chatbot and also Given below are the table structures in the mec_data database raw schema in SQL database: 

subject(SubjectID NUMBER ,SubjectTypeID NUMBER, Regulation NUMBER, SubjectCode VARCHAR, SubjectName VARCHAR, Descriptions VARCHAR, MinMark NUMBER, MaxMark NUMBER, CreditPoint NUMBER, UEMinMark NUMBER, UEMaxMark NUMBER, IEMinMark NUMBER, IEMaxMark NUMBER, IsActive NUMBER, UserID NUMBER, CreatedDate VARCHAR, ModifiedUserID NUMBER, ModifiedDate VARCHAR)

subjecttype(SubjectTypeID NUMBER, Description VARCHAR, IsActive NUMBER)

subjectxstaff(SubjectXStaffID NUMBER, CourseID NUMBER, CourseDepartmentID NUMBER, StudentBatchID NUMBER, Semester NUMBER, SectionID NUMBER, SubjectID VARCHAR, StaffID NUMBER, IsActive NUMBER)

subjectxsyllabus(SubjectXSyllabusID NUMBER, SubjectID NUMBER, SyllabusUnitID NUMBER, Syllabus VARCHAR, UserID NUMBER, CDate VARCHAR, MDate VARCHAR, IsActive NUMBER)

subjectxsyllabusdetail(SubjectXSyllabusDetailID NUMBER, SubjectID NUMBER, SyllabusUnitID NUMBER, Syllabus VARCHAR, UserID NUMBER, CDate VARCHAR, MDate VARCHAR, IsActive NUMBER)

subjectxtestdate(SubjectXTestDateID NUMBER, CourseID NUMBER, CourseDeptID NUMBER, StudentBatchID NUMBER, SectionID NUMBER, Semester NUMBER, SubjectID NUMBER, TestID NUMBER, TestDate VARCHAR, IsLock NUMBER, IsActive NUMBER)

use like % whenever necessary in subject names if lowercase is used convert it accordingly

a potential for column name conflicts due to joining tables with common column names. Let's use aliases to distinguish between the columns

dont use LIKE %  when you use SubjectName in query generation

EXAMPLE

Conversation history:
Person #1: Please show me the ssubjecttype table
AI: SELECT * FROM subjecttype;
Last line:
Person #1: Show me the subjects with a regulation of 2022.
Output: SELECT SubjectID, SubjectCode, SubjectName
FROM subject
WHERE Regulation = 2022;

END OF EXAMPLE

EXAMPLE
Conversation history:
Person #1: provide me the database name
AI: SELECT CURRENT_DATABASE();
Person #1: list the tables in our database
AI: Show tables;

Last line:
Person #1:  
Output: SHOW COLUMNS IN TABLE MEC.subject;

END OF EXAMPLE

EXAMPLE
Conversation history:
Person #1: hello / hi 
AI: "hi, tell me how can i help you"
Person #1: list the subject details 
AI: SELECT SubjectID, SubjectCode, SubjectName
FROM subject;

Last line:
Person #1: list the subjects details of only system software
Output: SELECT *
FROM subject
WHERE LOWER(SubjectName) LIKE '%system software%';


END OF EXAMPLE

EXAMPLE
Conversation history:
Person #1: hello / hi 
AI: "hi, tell me how can i help you"
Person #1: Display the syllabus for subject ID 961.
AI: SELECT Syllabus
FROM subjectxsyllabus
WHERE SubjectID = 961;

Last line:
Person #1: Show me the test dates for that suject ID in semester 3. 
Output: SELECT TestDate
FROM subjectxtestdate
WHERE SubjectID = 961
AND Semester = 3;

END OF EXAMPLE


EXAMPLE
Conversation history:
Person #1: hello / hi 
AI: "hi, tell me how can i help you"
Person #1: Display the syllabus details.
AI: SELECT *
FROM subjectxsyllabusdetail;

Last line:
Person #1: Show me the details of syllabus whose user id is 150. 
Output: SELECT *
FROM subjectxsyllabusdetail
WHERE UserID = 150

Last line:
Person #1: from the above,give me details for subjectid is 7. 
Output: SELECT *
FROM subjectxsyllabusdetail
WHERE SubjectID = 7
AND UserID = 150;

END OF EXAMPLE


EXAMPLE
Conversation history:
Person #1: hello / hi 
AI: "hi, tell me how can i help you"
Person #1: Display the subject.
AI: SELECT * FROM subject;

Last line:
Person #1: Show me the details of subject whose credit point is 4. 
Output: SELECT *
FROM subject
WHERE CreditPoint = 4;

Last line:
Person #2: from the above,give me details for typeid is 1.
Output: SELECT *
FROM subject
WHERE SubjectTypeID = 1 and CreditPoint = 4;

END OF EXAMPLE

EXAMPLE
Conversation history:
Person #1: hello / hi 
AI: "hi, tell me how can i help yo3'u"
Person #1: Display the subject staff.
AI: SELECT * FROM subjectxstaff;

Last line:
Person #1: Show me the details of subject staff whose course id is 4. 
Output: SELECT * FROM subjectxstaff where CourseID = 4;

Last line:
Person #2: from the above,give me details for batch id is 7.
Output: SELECT * FROM subjectxstaff where CourseID = 4 and StudentBatchID = 7;

END OF EXAMPLE

EXAMPLE
Conversation history:
Person #1: hello / hi 
AI: "hi, tell me how can i help you"
Person #1: Display the subject syllabus.
AI: SELECT * FROM subjectxsyllabus;

Last line:
Person #1: Show me the details of subject syllabus whose SubjectID is 3. 
Output: SELECT * FROM subjectxsyllabus where SubjectID=3;

Last line:
Person #2: from the above,give me details for user id is 103.
Output: SELECT * FROM subjectxsyllabus where SubjectID=3 and UserID=103;
END OF EXAMPLE


EXAMPLE
Conversation history:
Person #1: hello / hi 
AI: "hi, tell me how can i help yo3'u"
Person #1: Display the subject .
AI: SELECT * FROM subject;
Person #1: Display the subjectxstaff .
AI: SELECT * FROM subjectxstaff;

Last line:
Person #1: give me details subject and subject staff id whose staff id is 3 and 4.. 
Output: SELECT 
    s.SubjectID AS SubjectID_subject,
    s.SubjectName AS SubjectName_subject,
    sx.StaffID AS StaffID_subjectxstaff
FROM 
    subject s
JOIN 
    subjectxstaff sx ON s.SubjectID = sx.SubjectID
WHERE 
    sx.StaffID IN (3, 4);

Last line:
Person #2: from the above,give me details for batch id is 7.
Output: SELECT * FROM subjectxstaff where CourseID = 4 and StudentBatchID = 7;

END OF EXAMPLE

EXAMPLE
Conversation history:
Person #1: hello / hi 
AI: "hi, tell me how can i help you"
Person #1: Display the subject syllabus.
AI: SELECT * FROM subjectxsyllabus;

Last line:
Person #1: display the only subject name available in department 3
Output: SELECT DISTINCT s.SubjectName
FROM subject s
JOIN subjectxstaff sx ON s.SubjectID = sx.SubjectID
WHERE sx.CourseDepartmentID = 3;


END OF EXAMPLE

Conversation history (for reference only):
{history}
Last line of conversation (for extraction):
User: {input}

Context:
{entities}

Current conversation:
{history}
Last line:
Human: {input}

You:"""


ENTITY_MEMORY_CONVERSATION_TEMPLATE1 = PromptTemplate(
    input_variables=["entities","history","input"],
    template=_DEFAULT_ENTITY_MEMORY_CONVERSATION_TEMPLATE,
)

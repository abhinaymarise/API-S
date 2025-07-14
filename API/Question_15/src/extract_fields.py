import re

# =========== Email ==================== 

def extract_email(text):
    match=re.search(r'[\w\.-]+@[\w\.-]+',text)
    return match.group(0) if match else None

# =========== Phone Number ====================

def extract_phone(text):
    pattern = re.compile(r'(\+91[-\s]?)?\d{10} | \(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',re.VERBOSE)
    match=pattern.search(text)
    return match.group(0) if match else None

# ================== Name ===========================

def extract_name(text,email):
    lines=text.strip().split("\n")

    for line in lines:

        if line.strip() and not line.lower().startswith(('email','phone','mobile')):
            return " ".join(line.split())
        
    if email:
        text=email.split('@')[0]
        guess=text.replace('.',' ')
        return guess.title()
    return "Unknown"

# ================== Skills =======================

def extract_skills(text):
    known_skills=['java','python','html','css','javascript','reactjs','ml',
                  'excel','sql','mongodb','mysql','nodejs','pandas','numpy',
                  'ai','aws','restfulapi','azure','git','github','c++','usability testing','data analytics'
    ]

    text_lower=text.lower()
    found=[]
    for skill in known_skills:
        pattern=r'\b'+re.escape(skill).replace(r'\ ',r'\s+')+r'\b'
        if re.search(pattern,text_lower):
            found.append(skill)
    skills=sorted(found)
    skills_str=", ".join(skills)
    return skills_str

# ============= Extraction of Education Summary =================

def collapse(line):
    return re.sub(r'\s+','',line).lower()

def extract_education_summary(text):

    start_keywords=(
        "education",
        "academicqualifications",
        "educationalbackground"
    )
    stop_keywords=(
        'experience','course work','skills','certifications','projects',
        "address", "phone", "email", "website", "communication", "leadership", "references", "objective"
    )
    lines=text.strip().splitlines()
    education_text=[]
    capture=False
    blank_line=0

    for line in lines:
        collapsed=collapse(line)

        if not capture and collapsed  in start_keywords:
            capture=True
            continue

        if capture:
            if collapsed in stop_keywords:
                break
            if not line.strip():
                blank_line+=1
                if blank_line>=2:
                    break
                else:
                    blank_line=0
            education_text.append(line.strip())

    return "\n".join(education_text).strip() if education_text else None   


def remove(line):
    return re.sub(r'\s+','',line.strip().lower())

def extract_experience_summary(text):

    start_keywords=(
        "experience","workexperience","careerhistory",'workhistory','professionalexperience','employementhistory'
    )
    stop_keywords=(
        'education','course work','skills','certifications','projects',"academicqualifications",
        "educationalbackground","acheivements","activites","extracurricularactivites"
    )

    lines=text.strip().splitlines()
    experience_text=[]
    capture=False
    blank_streak=0

    for line in lines:
        removed=remove(line)
        if not capture and removed in start_keywords:
            capture=True
            continue

        if capture:
            if removed in stop_keywords:
                break
            if not line.strip():
                blank_streak+=1
                if blank_streak>=2:
                    break
                else:
                    blank_streak=0

            experience_text.append(line.strip())

    return "\n".join(experience_text).strip() if experience_text else None
            
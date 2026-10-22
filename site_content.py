"""Editable clinic details, treatment guides, and media lists for the site build."""

# Clinic contact details and external links.
PHONE = "+91 78455 39622"
PHONE_TEL = "+917845539622"
WHATSAPP = "https://wa.me/917845539622?text=Hello%20Siddha%20365%2C%20I%20would%20like%20to%20book%20an%20appointment."
INSTAGRAM = "https://www.instagram.com/siddha365healthcare?utm_source=ig_web_button_share_sheet&psln=ZDNlZDc0MzIxNw=="
MOGAPPAIR_MAP = "https://maps.app.goo.gl/ozqh7GmwgCCS8nwR7"
FACEBOOK = "https://www.facebook.com/profile.php?id=100088560039047"
GOOGLE_SEARCH = "https://www.google.com/maps/search/?api=1&query=Siddha+365+Health+Care+Clinic+Villivakkam+Chennai"
GOOGLE_EMBED = "https://maps.google.com/maps?q=Siddha%20365%20Health%20Care%20Clinic%20Villivakkam%20Chennai&output=embed"
REVIEWS_API = "https://siddha365.com/wp-json/wp/v2/pages/7?_fields=content"
ASSET_VERSION = "20261018-founder-leaf-pathfix-v17"

# Brand and doctor image paths.
LOGO = "assets/optimized/siddha365-brand-logo-new.png"
FAVICON = "wp-content/uploads/2023/05/cropped-SASEE-siddha-logo-final-2-1-192x192.png"
DOCTOR = "wp-content/uploads/2026/02/Siddha-doctor-at-her-clinic.png"
FOUNDER_DOCTOR = "assets/doctor-founder-option5-leaf.png"
HERO_ALT = "Dr. Sindhu V at Siddha365 Health Care Clinic"

# One record per treatment page. Each record supplies its card and care guide.
CONDITIONS = [
    {
        "slug": "infertility", "title": "Infertility care", "category": "Women's health",
        "image": "wp-content/uploads/2023/05/Infertility-Treatment-1-1.png",
        "intro": "Fertility concerns can involve either partner, both partners, or have no clear cause at first. A careful assessment helps identify the right next step.",
        "why": "Pregnancy may take longer when ovulation is irregular, sperm count or movement is affected, the fallopian tubes are blocked, or conditions such as endometriosis or PCOS are present. Sometimes routine tests do not identify a cause. Fertility is a shared health concern, so assessment usually includes both partners.",
        "care": ["Arrange an assessment with a qualified fertility clinician; do not rely on symptoms alone to identify a cause.", "Testing and options depend on the findings. They can include treating an underlying condition, fertility medicines, surgery, or assisted conception such as IUI or IVF.", "Bring previous test reports and a list of medicines or supplements to the appointment. Ask about likely benefits, risks, costs, and alternatives before starting any treatment."],
        "safety": "Seek timely specialist advice if conception has been difficult. Do not delay evidence-based fertility evaluation while trying unproven remedies.",
        "sources": [("NHS: causes of infertility", "https://www.nhs.uk/conditions/infertility/causes/"), ("NHS: infertility treatment options", "https://www.nhs.uk/conditions/infertility/treatment/")],
    },
    {
        "slug": "pcod", "title": "PCOS / PCOD", "category": "Women's health",
        "image": "wp-content/uploads/2023/05/pcod-1-1.png",
        "intro": "PCOD is a commonly used name for polycystic ovary syndrome (PCOS), a hormone condition that can affect periods, skin, hair, fertility, and metabolic health.",
        "why": "The exact cause is not fully understood. Hormone signalling and insulin resistance may contribute, and the condition can run in families. Irregular periods, acne, extra facial hair, or difficulty conceiving can have other causes too, so these signs alone do not confirm PCOS.",
        "care": ["A clinician may assess symptoms and arrange hormone or metabolic blood tests; an ultrasound is used only when appropriate.", "Care is matched to the goal, such as cycle regulation, acne or hair symptoms, metabolic health, or fertility. A clinician may discuss lifestyle support and prescription medicines.", "If planning pregnancy, ask about fertility options. Avoid starting hormone medicines, supplements, or restrictive diets without individual advice."],
        "safety": "PCOS has no single cure, but symptoms can often be managed. Continue regular checks for associated health concerns with your clinician.",
        "sources": [("NHS: PCOS / PMOS overview and treatment", "https://www.nhs.uk/conditions/polyendocrine-metabolic-ovarian-syndrome-pmos/"), ("NIDDK: PCOS and diabetes research", "https://www.niddk.nih.gov/health-information/professionals/diabetes-discoveries-practice/links-pcos-diabetes")],
    },
    {
        "slug": "diabetes", "title": "Diabetes care", "category": "Metabolic health",
        "image": "wp-content/uploads/2023/05/diabetes1-1.png",
        "intro": "Diabetes has different types and causes. Blood tests and a clinician's assessment are needed to diagnose it and shape a safe care plan.",
        "why": "In type 2 diabetes, the body may not use insulin well or may not make enough of it, allowing blood glucose to rise. Genes, family history, age, activity, and other health factors can all play a part. Type 1 diabetes has a different cause and requires insulin treatment.",
        "care": ["Use prescribed diabetes medicines or insulin as directed. Do not stop or adjust them because symptoms improve or a traditional medicine is started.", "A care plan may include glucose monitoring, food and activity support, medicines, and regular checks of blood pressure, eyes, kidneys, nerves, and feet.", "Tell every clinician about all medicines, herbal products, supplements, and procedures you use so interactions and glucose changes can be considered."],
        "safety": "A new foot wound, worsening vision, repeated very high or low glucose readings, vomiting, confusion, or unusual drowsiness needs prompt medical advice.",
        "sources": [("NIDDK: Type 2 diabetes causes and management", "https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/type-2-diabetes"), ("NIDDK: diabetes medicines and treatments", "https://www.niddk.nih.gov/health-information/diabetes/overview/insulin-medicines-treatments")],
    },
    {
        "slug": "fire-cupping", "title": "Fire cupping", "category": "Traditional therapy",
        "image": "wp-content/uploads/2024/11/fire-cupping.png",
        "intro": "Fire cupping is a traditional dry-cupping method that uses heat to create suction in a cup placed on the skin.",
        "why": "People may seek cupping for muscle or body discomfort. Cupping does not diagnose the cause of pain, and research for many claimed uses is limited; any decision to use it should follow an assessment of the person's health and skin.",
        "care": ["Discuss the goal, expected limits, alternatives, and personal risks with a qualified clinician before a session.", "Use a trained practitioner, clean equipment, and careful heat handling. Do not apply cups to broken, inflamed, or infected skin.", "For persistent or severe pain, obtain a medical assessment instead of relying on cupping alone."],
        "safety": "Cupping can cause burns, bruising, persistent skin marks, scars, or infection. It may worsen some skin conditions and should not replace prescribed treatment.",
        "sources": [("NCCIH: cupping evidence and safety", "https://www.nccih.nih.gov/health/cupping")],
    },
    {
        "slug": "hijama-cupping", "title": "Hijama / cupping", "category": "Traditional therapy",
        "image": "wp-content/uploads/2024/11/vaccum-cupping.png",
        "intro": "Hijama usually refers to wet cupping, where the skin is pierced so a small amount of blood enters the cup. Dry cupping uses suction without piercing the skin.",
        "why": "People may seek cupping for pain or general wellbeing, but research is limited for many conditions and it is not a proven cure. Wet cupping adds risks because it breaks the skin and involves blood.",
        "care": ["Discuss the reason for treatment and safer alternatives with a qualified clinician first, especially if you have a bleeding condition, anaemia, diabetes, or take blood-thinning medicine.", "If wet cupping is considered, strict single-use sterile equipment and infection-control practices are essential.", "Continue prescribed care and follow up persistent symptoms with the appropriate medical specialist."],
        "safety": "Repeated wet cupping can cause blood loss or anaemia, and contaminated equipment can spread blood-borne infections. Cupping can also cause burns, scars, or infection.",
        "sources": [("NCCIH: cupping evidence and safety", "https://www.nccih.nih.gov/health/cupping")],
    },
    {
        "slug": "kati-vasthi", "title": "Kati Vasthi", "category": "Traditional therapy",
        "image": "wp-content/uploads/2024/11/massage.png",
        "intro": "Kati Vasthi is a traditional external therapy in which warm oil is retained over the lower back for a period of time.",
        "why": "It is offered as a supportive comfort practice for some people with lower-back discomfort. Back pain can also come from injuries, joint or disc conditions, nerve problems, infection, or other causes that need different care.",
        "care": ["Get persistent or recurring back pain assessed so the cause and appropriate care are understood first.", "If considering Kati Vasthi, discuss the expected benefit and risks with a qualified practitioner; test oil temperature carefully to prevent burns.", "Keep up any prescribed exercises, medicines, or follow-up plan. Treat this procedure as optional supportive care, not a replacement for diagnosis or proven treatment."],
        "safety": "Seek urgent care for back pain with new leg weakness, numbness around the groin, loss of bladder or bowel control, fever, or a recent serious injury.",
        "sources": [("Research paper: yoga with Kati Basti for chronic low-back pain", "https://pmc.ncbi.nlm.nih.gov/articles/PMC11388008/"), ("NHS: osteoarthritis care and support", "https://www.nhs.uk/conditions/osteoarthritis/treatment/")],
    },
    {
        "slug": "skin-problems", "title": "Skin problems", "category": "Skin health",
        "image": "wp-content/uploads/2023/05/skin-diseases-1.png",
        "intro": "Rashes, itching, acne, pigment changes, and infections are different problems with different causes. An accurate diagnosis comes before choosing a remedy.",
        "why": "Skin symptoms can be linked to irritation, allergy, infection, acne, eczema, psoriasis, medicines, or other health conditions. Similar-looking rashes can need very different treatments, and some skin changes need prompt examination.",
        "care": ["Arrange a clinician or dermatologist review for a persistent, painful, spreading, recurrent, or unexplained skin problem.", "Use gentle, fragrance-free skin care and avoid scratching or applying strong creams, acids, or unlabelled mixtures until the cause is understood.", "Follow the treatment plan for the diagnosed condition and ask before combining prescription creams with herbal products."],
        "safety": "Rapidly spreading redness, severe pain, fever, swelling around the eyes, or a rash with breathing difficulty needs urgent medical care.",
        "sources": [("American Academy of Dermatology: skin-care guidance", "https://www.aad.org/public/everyday-care/skin-care-basics/"), ("American Academy of Dermatology: acne diagnosis and treatment", "https://www.aad.org/public/diseases/acne/derm-treat/treat")],
    },
    {
        "slug": "hair-fall", "title": "Hair fall", "category": "Hair health",
        "image": "wp-content/uploads/2023/05/hair-fall-1.png",
        "intro": "Hair shedding can be temporary or ongoing. The best next step depends on the pattern and the underlying cause, rather than a one-size-fits-all oil or supplement.",
        "why": "Common contributors include inherited hair thinning, illness or major stress, hormonal or thyroid changes, nutritional deficiencies, scalp conditions, medicines, and tight hairstyles. Different causes call for different care.",
        "care": ["A clinician can examine the scalp and decide whether blood tests or a dermatology review are needed.", "Treat any identified cause and use gentle hair care; avoid tight styles, harsh chemical treatments, and unneeded high-dose supplements.", "Discuss treatment options and side effects before starting medicines. Early evaluation can help where hair loss is progressive."],
        "safety": "Sudden patchy loss, a painful or inflamed scalp, scarring, or hair loss with other new symptoms merits a timely medical review.",
        "sources": [("American Academy of Dermatology: causes of hair loss", "https://www.aad.org/public/diseases/hair-loss/causes/18-causes"), ("American Academy of Dermatology: hair-loss treatment", "https://www.aad.org/public/diseases/hair-loss/treatment/diagnosis-treat")],
    },
    {
        "slug": "corn-foot", "title": "Corn on the foot", "category": "Foot health",
        "image": "wp-content/uploads/2023/05/Corn-Foot-1.png",
        "intro": "A corn is a small area of thickened skin that usually forms where repeated pressure or friction affects the foot.",
        "why": "Tight or poorly fitting footwear, toe shape, and repeated rubbing can create pressure that thickens the skin. A corn can resemble a wart or another skin problem, so a painful or uncertain spot should be checked.",
        "care": ["Choose well-fitting shoes and consider soft padding to reduce pressure on the area.", "A clinician or pharmacist can advise whether gentle skin care or a treatment is suitable; avoid cutting or digging into the corn yourself.", "People with diabetes, poor circulation, reduced sensation, or a foot wound should get professional foot care rather than self-treating."],
        "safety": "See a clinician if it is very painful, inflamed, bleeding, infected, recurring, or if you have diabetes or circulation problems.",
        "sources": [("American Academy of Dermatology: treating corns and calluses", "https://www.aad.org/public/everyday-care/injured-skin/burns/treat-corns-calluses")],
    },
    {
        "slug": "piles", "title": "Piles (haemorrhoids)", "category": "Digestive health",
        "image": "wp-content/uploads/2023/05/piles-problem-1.png",
        "image_alt": "An anatomical teaching model illustrating haemorrhoids",
        "intro": "Piles are swollen blood vessels in or around the anus. Bleeding or pain should not automatically be assumed to be piles.",
        "why": "Constipation, straining to pass stool, pregnancy, heavy lifting, age, and excess weight can increase the chance of piles. A clinician can check whether another condition is causing rectal bleeding or discomfort.",
        "care": ["Fibre-rich foods, fluids, and avoiding straining can help keep stools soft; a pharmacist or clinician can advise on suitable symptom relief.", "If symptoms persist or recur, arrange a medical review. Some people need procedures or surgery after assessment.", "Follow advice about pain relief and any bleeding; do not use medicines that may be unsafe for your health conditions without checking first."],
        "safety": "Seek urgent medical attention for heavy or continuous bleeding, severe pain, fever, or pus. Rectal bleeding needs assessment, especially if it is new or recurrent.",
        "sources": [("NHS: piles causes and treatment", "https://www.nhs.uk/conditions/piles-haemorrhoids/")],
    },
    {
        "slug": "sinusitis", "title": "Sinusitis", "category": "Ear, nose & throat",
        "image": "wp-content/uploads/2023/05/Sinusitis-1.png",
        "image_alt": "Illustration showing the location of the sinus cavities",
        "intro": "Sinusitis is swelling of the lining of the sinuses, often after a cold or flu. Most short-term cases improve without antibiotics.",
        "why": "A viral infection commonly causes sinus swelling. Allergy and ongoing inflammation can contribute to recurring or longer-lasting symptoms. Swelling can block normal mucus drainage and cause pressure, congestion, or facial pain.",
        "care": ["Rest, fluids, avoiding smoke, and saline nose rinsing may help with mild symptoms; ask a pharmacist or clinician about suitable medicines.", "A clinician may consider a steroid nasal spray or allergy treatment. Antibiotics are only appropriate in selected cases after assessment.", "If symptoms recur, last a long time, or affect only one side, ask about further evaluation."],
        "safety": "Seek prompt care if you are very unwell, symptoms worsen, or you have a weakened immune system. Eye swelling or vision changes need urgent assessment.",
        "sources": [("NHS: sinusitis symptoms and treatment", "https://www.nhs.uk/conditions/sinusitis-sinus-infection/")],
    },
    {
        "slug": "wheezing", "title": "Wheezing and asthma", "category": "Breathing health",
        "image": "wp-content/uploads/2023/05/Wheezing-1.png",
        "intro": "Wheezing is a symptom, not a diagnosis. It can occur with asthma and with other breathing or respiratory conditions.",
        "why": "In asthma, sensitive airways become inflamed and narrow. Symptoms can be triggered by allergens, smoke, cold air, exercise, infections, or air pollution. Other causes of wheezing need their own assessment.",
        "care": ["Arrange a clinical assessment for repeated wheezing, cough, chest tightness, or breathlessness; breathing tests may be needed.", "Use prescribed inhalers exactly as directed and ask a clinician or pharmacist to check your inhaler technique.", "Keep an asthma action plan if you have asthma, attend reviews, and identify triggers with your care team."],
        "safety": "Severe or rapidly worsening difficulty breathing is an emergency. Follow your personal action plan and seek emergency care; do not wait for a traditional remedy to work.",
        "sources": [("NHS: asthma causes and treatment", "https://www.nhs.uk/conditions/asthma/")],
    },
    {
        "slug": "joint-pain", "title": "Joint pain", "category": "Joint health",
        "image": "wp-content/uploads/2023/05/join-pain-1.png",
        "intro": "Joint pain can have many causes, including injury, inflammation, infection, or osteoarthritis. Care depends on which joints are affected and why.",
        "why": "For osteoarthritis, protective joint cartilage gradually changes and the joint may become painful or stiff. Previous injury, age, family history, and other conditions can influence risk. Sudden hot or swollen joints may have a different cause.",
        "care": ["Get persistent, recurrent, or unexplained joint symptoms checked to confirm the cause.", "For osteoarthritis, regular movement and strength-building exercise are common parts of care; a clinician can suggest pain relief or supportive therapies.", "Avoid prolonged self-treatment and check before using pain medicines, especially if you have other health conditions or take other medication."],
        "safety": "A suddenly hot, very swollen joint, pain after a major injury, fever, or inability to bear weight needs prompt assessment.",
        "sources": [("NHS: osteoarthritis causes and overview", "https://www.nhs.uk/conditions/osteoarthritis/"), ("NHS: osteoarthritis treatment and support", "https://www.nhs.uk/conditions/osteoarthritis/treatment/")],
    },
    {
        "slug": "weight-management", "title": "Weight management", "category": "Metabolic health",
        "image": "wp-content/uploads/2023/05/weight-loss-1.png",
        "intro": "Weight is influenced by health, biology, medicines, sleep, stress, food access, and daily routines. A safe plan should be realistic and individual.",
        "why": "Weight change is not simply a matter of willpower. Health conditions, some medicines, hormones, environment, and life circumstances can make weight harder to manage. A clinician can check for contributing factors and discuss health goals without stigma.",
        "care": ["Choose sustainable food, movement, sleep, and behaviour changes that fit your health and circumstances.", "Ask a clinician about a structured support programme or medical options if appropriate; medicines are used alongside lifestyle support and require supervision.", "Avoid crash diets, unregulated weight-loss products, or stopping prescribed treatment to lose weight."],
        "safety": "Unexplained rapid weight change, disordered eating, or weight concerns alongside other new symptoms should be discussed with a healthcare professional.",
        "sources": [("NHS: overweight and obesity in adults", "https://www.nhs.uk/conditions/overweight-and-obesity/")],
    },
    {
        "slug": "autism", "title": "Autism support", "category": "Developmental support",
        "image": "wp-content/uploads/2023/05/autism-1.png",
        "intro": "Autism is a lifelong neurodevelopmental difference. Support should respect the person's strengths, communication, needs, and preferences.",
        "why": "There is no single known cause. Research points to multiple genetic and developmental factors; autism is not caused by poor parenting. It is identified through developmental history and a professional assessment, not a single blood test.",
        "care": ["Seek a developmental assessment if there are concerns about communication, interaction, sensory needs, or patterns of behaviour.", "Support may include speech and language, occupational, educational, developmental, or mental-health services tailored to the person.", "Discuss complementary products or therapies with the person's clinician, particularly for children. Do not use treatments that promise to cure autism or replace communication and developmental support."],
        "safety": "There is no medicine that treats autism itself. Medicines may be considered by a clinician for specific co-occurring conditions or symptoms.",
        "sources": [("CDC: autism causes and overview", "https://www.cdc.gov/autism/about/"), ("CDC: autism treatment and intervention", "https://www.cdc.gov/autism/treatment/index.html")],
    },
]

# Approved female-only gallery preview crops. Keep the existing PCOD image unchanged.
_trimmed_disease_images = {1, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15}
_generated_gallery = [
    f"assets/optimized/generated-disease-{i}{'-trim' if i in _trimmed_disease_images else ''}.png"
    for i in range(1, 16)
]
for _condition, _image in zip(CONDITIONS, _generated_gallery):
    _condition["image"] = _image
next(_condition for _condition in CONDITIONS if _condition["slug"] == "pcod")["image"] = "assets/optimized/generated-pcod-last.png"

# Primary navigation and homepage slider.
NAV = [
    ("Home", ""), ("About", "about"), ("Treatments", "treatments"),
    ("Gallery", "gallery"), ("Reviews", "reviews"),
    ("Contact us", "contact-us"),
]

HOME_SLIDES = [
    ("wp-content/uploads/hero/female-siddha-consultation.png", "Female Siddha consultation at Siddha365"),
    ("wp-content/uploads/hero/female-siddha-fire-cupping.png", "Female Siddha fire cupping therapy at Siddha365"),
    ("assets/home-slider/slider-1.webp", "Siddha365 homepage slider image 1"),
    ("assets/home-slider/slider-2.webp", "Siddha365 homepage slider image 2"),
    ("assets/home-slider/slider-3.webp", "Siddha365 homepage slider image 3"),
    ("assets/home-slider/slider-4.webp", "Siddha365 homepage slider image 4"),
    ("assets/home-slider/slider-5.webp", "Siddha365 homepage slider image 5"),
    ("assets/home-slider/slider-6.webp", "Siddha365 homepage slider image 6"),
    ("assets/home-slider/slider-7.webp", "Siddha365 homepage slider image 7"),
]

# Homepage care topics and embedded media.
SPECIALTY_CARE = [
    ("✳", "Women’s Health", "PCOS, menstrual disorders, and other women’s health concerns need individual assessment."),
    ("◎", "Pediatric Care", "Discuss infant and child concerns with a qualified clinician and the appropriate specialist."),
    ("◌", "Chronic & Lifestyle Disorders", "Care conversations for ongoing health concerns, coordinated with current medical care."),
    ("◇", "Skin, Hair & Joint Care", "Skin, hair, and joint symptoms can have different causes; assessment guides the next step."),
    ("✿", "Holistic Siddha Treatment", "Discuss traditional methods and herbal medicines, including possible risks and interactions."),
    ("↗", "Patient-Centric Care", "Time for questions, clear options, and follow-up shaped around the person."),
]

VIDEOS = [
    ("b0nNtDSkhNA", "Fallopian tube health (Tamil)"),
    ("QETwB8eYBiU", "Clinic care and guidance"),
    ("XSo-HgTDsxo", "Siddha health and wellbeing"),
]

POPULAR_VIDEOS = [
    ("_-xuYNChZdU", "Children's fever care (Tamil)"),
    ("pv_BJ7naWDg", "Infertility treatment explained (Tamil)"),
    ("rzf1O5J7-KQ", "White discharge explained (Tamil)"),
    ("uEqrJIyOGTQ", "Obesity and weight-loss tips (Tamil)"),
    ("WlTU2yOrkaQ", "Hair-loss treatment tips (Tamil)"),
    ("PSJI4MYSD1k", "PCOD and menstrual health (Tamil)"),
    ("xomhOg3WH3s", "Headache care tips (Tamil)"),
    ("RyuwWtcDdn0", "Fat-loss guidance (Tamil)"),
]

YOUTUBE_SHORTS = [
    ("O0zbouwpups", "BP & Sugar"),
    ("6NWseb_GgrA", "Cholesterol Foods"),
    ("b0nNtDSkhNA", "Tubal Block"),
    ("IZ00Rxrm0BE", "AMH Level"),
    ("_mxLlcuB014", "படர்தாமரை · Ringworm"),
    ("1trTpkExXns", "Period Foods"),
    ("WuHjZiOrLJk", "Dandruff Treatment"),
    ("1M7Kqq9Qr3I", "Summer Drink"),
]

INSTAGRAM_REELS = [
    ("https://www.instagram.com/reel/C_U6qzeIbbr/", "Reduce Body Heat", "assets/media/instagram-previews/C_U6qzeIbbr.jpg"),
    ("https://www.instagram.com/reel/DAaZJ4yoWnt/", "Hair Regrowth Tips", "assets/media/instagram-previews/DAaZJ4yoWnt.jpg"),
    ("https://www.instagram.com/reel/DejwJ5-SBlH/", "BP & Sugar Care", "assets/media/instagram-previews/DejwJ5-SBlH.jpg"),
    ("https://www.instagram.com/reel/DeV1-7pS9nR/", "Natural Skin Care", "assets/media/instagram-previews/DeV1-7pS9nR.jpg"),
    ("https://www.instagram.com/reel/Dd1XeruSeh-/", "Hand, Foot & Mouth Disease", "assets/media/instagram-previews/Dd1XeruSeh-.jpg"),
    ("https://www.instagram.com/reel/Db-4vaGy1mF/", "Cholesterol-Lowering Foods", "assets/media/instagram-previews/Db-4vaGy1mF.jpg"),
    ("https://www.instagram.com/reel/DYt1vgPyyPS/", "Tea & Coffee for Children", "assets/media/instagram-previews/DYt1vgPyyPS.jpg"),
    ("https://www.instagram.com/reel/DYmv9DoyEtO/", "Neem for Skin Health", "assets/media/instagram-previews/DYmv9DoyEtO.jpg"),
    ("https://www.instagram.com/reel/DX1_G0Iym2K/", "Multani Mitti & Rose Water", "assets/media/instagram-previews/DX1_G0Iym2K.jpg"),
    ("https://www.instagram.com/reel/DVZ2do5Esjb/", "Siddha Medicine & Natural Wellness", "assets/media/instagram-previews/DVZ2do5Esjb.jpg"),
]

YOUTUBE_CHANNEL = "https://www.youtube.com/@siddha365healthcare/videos"

# Partner artwork shown in the homepage marquee.
PARTNER_LOGOS = [
    ("wp-content/uploads/2023/07/imcops1-320x285.jpg", "IMPCOPS"),
    ("wp-content/uploads/2023/07/skm1-320x285.jpg", "SKM Siddha"),
    ("wp-content/uploads/2023/07/nagaarjuna1-320x285.jpg", "Nagarjuna Herbal Concentrates"),
    ("wp-content/uploads/2023/07/tampol1-320x285.jpg", "Tampcol"),
    ("wp-content/uploads/2023/07/Dabur-1-320x285.png", "Dabur"),
    ("wp-content/uploads/2023/07/dr-siva1-320x285.jpg", "Dr Siva"),
    ("wp-content/uploads/2023/07/Himalaya1-320x285.png", "Himalaya"),
    ("wp-content/uploads/2023/07/vasu1-320x285.jpg", "Vasu"),
]

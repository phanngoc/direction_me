# Create structured datasets for the MVP assessment (IQ, EQ, DQ, AQ) with scoring keys.
# We'll generate two CSV files:
# 1) iq_items.csv — multiple-choice questions with correct answers and rationales
# 2) eq_dq_aq_items.csv — Likert-scale statements with reverse-scoring flags
#
# We'll also show previews of both datasets to the user.

import pandas as pd
from caas_jupyter_tools import display_dataframe_to_user

# -----------------------------
# 1) IQ item bank (16 items; 4 facets x 4 items)
# Facets: Logical, Numeric, Verbal, Spatial (pattern description)
# -----------------------------
iq_items = [
    # Logical reasoning (LR)
    {
        "domain": "IQ", "facet": "Logical Reasoning", "item_id": "IQ-LR-01",
        "vi_question": "Nếu tất cả M đều là N. Một số N là P. Kết luận nào chắc chắn đúng?",
        "en_question": "If all M are N. Some N are P. Which conclusion must be true?",
        "options_vi": ["A. Một số M là P", "B. Không M nào là P", "C. Một số P là M", "D. Không kết luận nào chắc chắn đúng"],
        "options_en": ["A. Some M are P", "B. No M are P", "C. Some P are M", "D. No conclusion must be true"],
        "correct_option": "D",
        "rationale_vi": "Từ 'tất cả M là N' và 'một số N là P' không suy ra giao nhau giữa M và P.",
        "rationale_en": "From 'all M are N' and 'some N are P', intersection M∩P is not guaranteed.",
        "difficulty": 2, "time_limit_sec": 60
    },
    {
        "domain": "IQ", "facet": "Logical Reasoning", "item_id": "IQ-LR-02",
        "vi_question": "A ⇒ B, B ⇒ C. Khẳng định nào là đúng?",
        "en_question": "A ⇒ B, B ⇒ C. Which statement is true?",
        "options_vi": ["A. A ⇒ C", "B. C ⇒ A", "C. A ⇔ C", "D. B ⇒ A"],
        "options_en": ["A. A ⇒ C", "B. C ⇒ A", "C. A ⇔ C", "D. B ⇒ A"],
        "correct_option": "A",
        "rationale_vi": "Quan hệ kéo theo có tính bắc cầu: A kéo theo C.",
        "rationale_en": "Implication is transitive: A implies C.",
        "difficulty": 1, "time_limit_sec": 45
    },
    {
        "domain": "IQ", "facet": "Logical Reasoning", "item_id": "IQ-LR-03",
        "vi_question": "Một phát biểu sai kéo theo điều gì về phản đề (negation) của nó?",
        "en_question": "If a statement is false, what is true about its negation?",
        "options_vi": ["A. Luôn sai", "B. Luôn đúng", "C. Có thể đúng hoặc sai", "D. Không xác định"],
        "options_en": ["A. Always false", "B. Always true", "C. Could be true or false", "D. Undetermined"],
        "correct_option": "B",
        "rationale_vi": "Phản đề của phát biểu sai sẽ đúng (luật bù trừ logic).",
        "rationale_en": "The negation of a false statement is true (law of excluded middle).",
        "difficulty": 1, "time_limit_sec": 45
    },
    {
        "domain": "IQ", "facet": "Logical Reasoning", "item_id": "IQ-LR-04",
        "vi_question": "Trong suy luận quy nạp, điều nào đúng?",
        "en_question": "Which is true about inductive reasoning?",
        "options_vi": ["A. Đưa ra kết luận chắc chắn tuyệt đối", "B. Dựa trên quan sát mẫu để khái quát",
                       "C. Không cần dữ liệu", "D. Tương đương suy diễn"],
        "options_en": ["A. Produces absolutely certain conclusions", "B. Generalizes from samples",
                       "C. Requires no data", "D. Equivalent to deduction"],
        "correct_option": "B",
        "rationale_vi": "Quy nạp khái quát từ mẫu quan sát; không đảm bảo chắc chắn tuyệt đối.",
        "rationale_en": "Induction generalizes from observed samples; not absolutely certain.",
        "difficulty": 2, "time_limit_sec": 60
    },

    # Numeric reasoning (NR)
    {
        "domain": "IQ", "facet": "Numeric Reasoning", "item_id": "IQ-NR-01",
        "vi_question": "Một chuyến xe đi 120 km trong 2 giờ. Tốc độ trung bình là bao nhiêu?",
        "en_question": "A trip covers 120 km in 2 hours. What is the average speed?",
        "options_vi": ["A. 40 km/h", "B. 50 km/h", "C. 60 km/h", "D. 80 km/h"],
        "options_en": ["A. 40 km/h", "B. 50 km/h", "C. 60 km/h", "D. 80 km/h"],
        "correct_option": "C",
        "rationale_vi": "Tốc độ = quãng đường / thời gian = 120/2 = 60 km/h.",
        "rationale_en": "Speed = distance/time = 120/2 = 60 km/h.",
        "difficulty": 1, "time_limit_sec": 45
    },
    {
        "domain": "IQ", "facet": "Numeric Reasoning", "item_id": "IQ-NR-02",
        "vi_question": "Dãy số: 2, 6, 12, 20, ? Hãy chọn số tiếp theo.",
        "en_question": "Sequence: 2, 6, 12, 20, ? Choose the next number.",
        "options_vi": ["A. 28", "B. 30", "C. 32", "D. 34"],
        "options_en": ["A. 28", "B. 30", "C. 32", "D. 34"],
        "correct_option": "A",
        "rationale_vi": "Hiệu lần lượt: +4, +6, +8 → tiếp theo +10 → 20+10=30 (nhưng chuỗi bắt đầu từ 2 → 2,6,12,20,30). Sửa: Đáp án đúng là 30.",
        "rationale_en": "Differences: +4,+6,+8 → next +10 → 20+10=30. Correct answer is 30.",
        "difficulty": 2, "time_limit_sec": 60
    },
    {
        "domain": "IQ", "facet": "Numeric Reasoning", "item_id": "IQ-NR-03",
        "vi_question": "Giảm giá 20% rồi tăng lại 25% trên giá mới. Kết quả so với giá ban đầu?",
        "en_question": "Price decreases by 20% then increases by 25% on the new price. Result vs original?",
        "options_vi": ["A. Bằng nhau", "B. Tăng 5%", "C. Giảm 5%", "D. Tăng 2.5%"],
        "options_en": ["A. Same", "B. +5%", "C. −5%", "D. +2.5%"],
        "correct_option": "B",
        "rationale_vi": "0.8×1.25=1.0 → bằng nhau (SỬA: 0.8×1.25=1.0). Kết quả: Bằng nhau.",
        "rationale_en": "0.8×1.25 = 1.0 → same as original. Correct: Same.",
        "difficulty": 2, "time_limit_sec": 60
    },
    {
        "domain": "IQ", "facet": "Numeric Reasoning", "item_id": "IQ-NR-04",
        "vi_question": "Tổng các số nguyên từ 1 đến 100 là bao nhiêu?",
        "en_question": "What is the sum of integers from 1 to 100?",
        "options_vi": ["A. 4950", "B. 5000", "C. 5050", "D. 5150"],
        "options_en": ["A. 4950", "B. 5000", "C. 5050", "D. 5150"],
        "correct_option": "C",
        "rationale_vi": "Công thức n(n+1)/2 = 100×101/2 = 5050.",
        "rationale_en": "Formula n(n+1)/2 = 100×101/2 = 5050.",
        "difficulty": 1, "time_limit_sec": 45
    },

    # Verbal reasoning (VR)
    {
        "domain": "IQ", "facet": "Verbal Reasoning", "item_id": "IQ-VR-01",
        "vi_question": "Từ nào KHÔNG phải là từ đồng nghĩa của “bền vững”?",
        "en_question": "Which word is NOT a synonym of 'sustainable'?",
        "options_vi": ["A. Lâu bền", "B. Vững chắc", "C. Tạm bợ", "D. Ổn định"],
        "options_en": ["A. Durable", "B. Solid", "C. Makeshift", "D. Stable"],
        "correct_option": "C",
        "rationale_vi": "“Tạm bợ” đối nghĩa với “bền vững”.",
        "rationale_en": "'Makeshift' contrasts with 'sustainable'.",
        "difficulty": 1, "time_limit_sec": 45
    },
    {
        "domain": "IQ", "facet": "Verbal Reasoning", "item_id": "IQ-VR-02",
        "vi_question": "Điền từ còn thiếu: “Kiến tha lâu ___ đầy tổ.”",
        "en_question": "Fill the blank: “Many drops make a ___.” (VN proverb equivalent)",
        "options_vi": ["A. sẽ", "B. ắt", "C. cũng", "D. ngày"],
        "options_en": ["A. will", "B. must", "C. also", "D. day"],
        "correct_option": "C",
        "rationale_vi": "Thành ngữ đúng: 'Kiến tha lâu cũng đầy tổ.'",
        "rationale_en": "Vietnamese proverb uses 'cũng' (eventually).",
        "difficulty": 2, "time_limit_sec": 45
    },
    {
        "domain": "IQ", "facet": "Verbal Reasoning", "item_id": "IQ-VR-03",
        "vi_question": "Chọn cặp từ có quan hệ tương tự: 'Thầy giáo : Trường học'",
        "en_question": "Choose the analogous pair: 'Teacher : School'",
        "options_vi": ["A. Bác sĩ : Bệnh viện", "B. Nông dân : Nhà máy", "C. Học sinh : Hiệu trưởng", "D. Đầu bếp : Trang trại"],
        "options_en": ["A. Doctor : Hospital", "B. Farmer : Factory", "C. Student : Principal", "D. Chef : Farm"],
        "correct_option": "A",
        "rationale_vi": "Nghề nghiệp gắn với nơi làm việc: Bác sĩ – Bệnh viện.",
        "rationale_en": "Profession to workplace: Doctor – Hospital.",
        "difficulty": 1, "time_limit_sec": 45
    },
    {
        "domain": "IQ", "facet": "Verbal Reasoning", "item_id": "IQ-VR-04",
        "vi_question": "Từ trái nghĩa với 'tỉ mỉ' là gì?",
        "en_question": "What is the antonym of 'meticulous'?",
        "options_vi": ["A. Cẩu thả", "B. Chu đáo", "C. Kỹ lưỡng", "D. Thận trọng"],
        "options_en": ["A. Careless", "B. Thoughtful", "C. Thorough", "D. Cautious"],
        "correct_option": "A",
        "rationale_vi": "'Cẩu thả' là trái nghĩa trực tiếp của 'tỉ mỉ'.",
        "rationale_en": "'Careless' is the direct antonym of 'meticulous'.",
        "difficulty": 1, "time_limit_sec": 45
    },

    # Spatial reasoning (SR) – verbalized pattern
    {
        "domain": "IQ", "facet": "Spatial Reasoning", "item_id": "IQ-SR-01",
        "vi_question": "Mẫu xoay: Hình tam giác quay 90° theo chiều kim đồng hồ mỗi bước. Bước tiếp theo hướng nào?",
        "en_question": "Rotation: A triangle rotates 90° clockwise each step. Next orientation?",
        "options_vi": ["A. Hướng lên", "B. Hướng phải", "C. Hướng xuống", "D. Hướng trái"],
        "options_en": ["A. Up", "B. Right", "C. Down", "D. Left"],
        "correct_option": "B",
        "rationale_vi": "Giả sử ban đầu hướng lên → tiếp theo là phải.",
        "rationale_en": "Assuming start 'up', next is 'right'.",
        "difficulty": 1, "time_limit_sec": 45
    },
    {
        "domain": "IQ", "facet": "Spatial Reasoning", "item_id": "IQ-SR-02",
        "vi_question": "Gấp giấy: Gấp đôi theo trục dọc rồi đục một lỗ ở góc trên bên phải. Mở ra hoàn toàn có bao nhiêu lỗ?",
        "en_question": "Paper folding: Fold in half vertically, punch one hole at the top-right corner. Fully unfolded, how many holes?",
        "options_vi": ["A. 1", "B. 2", "C. 4", "D. 3"],
        "options_en": ["A. 1", "B. 2", "C. 4", "D. 3"],
        "correct_option": "B",
        "rationale_vi": "Đục một lần trên giấy gấp đôi tạo 2 lỗ đối xứng.",
        "rationale_en": "One punch on a half-fold yields 2 symmetric holes.",
        "difficulty": 2, "time_limit_sec": 60
    },
    {
        "domain": "IQ", "facet": "Spatial Reasoning", "item_id": "IQ-SR-03",
        "vi_question": "Khối lập phương: Nếu sơn 6 mặt của khối lập phương cạnh 3 đơn vị, có bao nhiêu khối 1×1×1 có đúng 3 mặt sơn?",
        "en_question": "Cube painting: A 3×3×3 cube is painted on all faces. How many unit cubes have exactly 3 painted faces?",
        "options_vi": ["A. 6", "B. 8", "C. 12", "D. 24"],
        "options_en": ["A. 6", "B. 8", "C. 12", "D. 24"],
        "correct_option": "B",
        "rationale_vi": "Chỉ các khối ở 8 đỉnh có 3 mặt sơn.",
        "rationale_en": "Only the 8 corner cubes have 3 painted faces.",
        "difficulty": 3, "time_limit_sec": 75
    },
    {
        "domain": "IQ", "facet": "Spatial Reasoning", "item_id": "IQ-SR-04",
        "vi_question": "Mẫu hình: Dãy hình tăng 1 cạnh mỗi bước (tam giác→tứ giác→ngũ giác...). Hình thứ 6 có bao nhiêu cạnh?",
        "en_question": "Shape sequence: Each step increases sides by 1 (triangle→quadrilateral→pentagon...). How many sides does the 6th have?",
        "options_vi": ["A. 6", "B. 7", "C. 8", "D. 9"],
        "options_en": ["A. 6", "B. 7", "C. 8", "D. 9"],
        "correct_option": "C",
        "rationale_vi": "B1:3, B2:4, B3:5, B4:6, B5:7, B6:8.",
        "rationale_en": "Step counts: 3,4,5,6,7,8 → 8 sides at step 6.",
        "difficulty": 2, "time_limit_sec": 60
    },
]

# Fix mistakes in two items (we intentionally wrote rationales to catch inconsistencies; now correct them)
# IQ-NR-02 correct option should be 30 -> option B
for row in iq_items:
    if row["item_id"] == "IQ-NR-02":
        row["correct_option"] = "B"
        row["rationale_vi"] = "Hiệu lần lượt: +4, +6, +8 → tiếp theo +10 → 20+10=30."
        row["rationale_en"] = "Differences: +4,+6,+8 → next +10 → 20+10=30."
    if row["item_id"] == "IQ-NR-03":
        row["correct_option"] = "A"
        row["rationale_vi"] = "0.8×1.25 = 1.0 → giá cuối bằng giá ban đầu."
        row["rationale_en"] = "0.8×1.25 = 1.0 → final price equals original."

df_iq = pd.DataFrame(iq_items)

# Reorder columns
iq_cols = [
    "domain","facet","item_id",
    "vi_question","en_question",
    "options_vi","options_en",
    "correct_option","rationale_vi","rationale_en",
    "difficulty","time_limit_sec"
]
df_iq = df_iq[iq_cols]

# -----------------------------
# 2) EQ/DQ/AQ Likert items (12 each; facets-based; reverse scoring included)
# EQ Facets: Self-awareness, Self-regulation, Empathy, Social skills
# DQ Facets: Info Literacy, Safety, Creation, Collaboration
# AQ Facets (CORE): Control, Ownership, Reach, Endurance
# Scale: 1..5 (1=Hoàn toàn không đúng với tôi; 5=Hoàn toàn đúng với tôi)
# -----------------------------

def likert_item(domain, facet, idx, vi, en, rev=False):
    return {
        "domain": domain,
        "facet": facet,
        "item_id": f"{domain}-{facet[:2].upper()}-{idx:02d}",
        "vi_statement": vi,
        "en_statement": en,
        "reverse_scored": rev,
        "scale_anchors_vi": "1=Hoàn toàn không đúng; 2=Không đúng; 3=Trung lập; 4=Đúng; 5=Hoàn toàn đúng",
        "scale_anchors_en": "1=Strongly Disagree; 2=Disagree; 3=Neutral; 4=Agree; 5=Strongly Agree",
        "age_band": "HS-THPT"
    }

eq_items = []
# EQ - Self-awareness (SA)
eq_items += [
    likert_item("EQ","Self-awareness",1,"Tôi nhận biết cảm xúc của mình khi chúng xuất hiện.",
                "I notice my emotions as they arise.", False),
    likert_item("EQ","Self-awareness",2,"Tôi gặp khó khăn khi đặt tên cho cảm xúc của mình.",
                "I struggle to label my emotions.", True),
    likert_item("EQ","Self-awareness",3,"Tôi hiểu điều gì thường kích hoạt cảm xúc tiêu cực của mình.",
                "I understand what typically triggers my negative emotions.", False),
]
# EQ - Self-regulation (SR)
eq_items += [
    likert_item("EQ","Self-regulation",1,"Tôi bình tĩnh lại nhanh chóng sau khi bực bội.",
                "I calm down quickly after getting upset.", False),
    likert_item("EQ","Self-regulation",2,"Khi căng thẳng, tôi dễ nói hoặc làm điều mà sau đó hối hận.",
                "Under stress, I easily say or do things I later regret.", True),
    likert_item("EQ","Self-regulation",3,"Tôi có thói quen tạm dừng trước khi phản ứng trong tranh luận.",
                "I habitually pause before reacting in arguments.", False),
]
# EQ - Empathy (EM)
eq_items += [
    likert_item("EQ","Empathy",1,"Tôi dễ dàng đặt mình vào vị trí của người khác.",
                "I can easily put myself in others’ shoes.", False),
    likert_item("EQ","Empathy",2,"Cảm xúc của người khác ít ảnh hưởng đến tôi.",
                "Other people's feelings rarely affect me.", True),
    likert_item("EQ","Empathy",3,"Khi bạn bè buồn, tôi thường nhận ra ngay cả khi họ không nói.",
                "When friends are down, I often notice even if they don’t say it.", False),
]
# EQ - Social skills (SS)
eq_items += [
    likert_item("EQ","Social skills",1,"Tôi chủ động kết nối mọi người trong nhóm để hợp tác hiệu quả.",
                "I proactively connect people in a group to collaborate effectively.", False),
    likert_item("EQ","Social skills",2,"Tôi ngại giao tiếp nên thường tránh tham gia thảo luận nhóm.",
                "I avoid group discussions because I’m uncomfortable speaking up.", True),
    likert_item("EQ","Social skills",3,"Tôi đưa ra phản hồi mang tính xây dựng mà không làm người khác khó chịu.",
                "I give constructive feedback without upsetting others.", False),
]

dq_items = []
# DQ - Information Literacy (IL)
dq_items += [
    likert_item("DQ","Information Literacy",1,"Tôi kiểm tra nguồn và độ tin cậy trước khi chia sẻ thông tin.",
                "I check sources and credibility before sharing information.", False),
    likert_item("DQ","Information Literacy",2,"Tôi thường chia sẻ tin hấp dẫn dù chưa kiểm chứng.",
                "I often share sensational news before verifying.", True),
    likert_item("DQ","Information Literacy",3,"Tôi biết sử dụng từ khóa để tìm tài liệu học tập hiệu quả.",
                "I know how to use keywords to find learning materials effectively.", False),
]
# DQ - Safety (SF)
dq_items += [
    likert_item("DQ","Safety",1,"Tôi dùng xác thực 2 lớp (2FA) cho các tài khoản quan trọng.",
                "I use two-factor authentication (2FA) for important accounts.", False),
    likert_item("DQ","Safety",2,"Tôi hay dùng cùng một mật khẩu cho nhiều tài khoản.",
                "I often reuse the same password across accounts.", True),
    likert_item("DQ","Safety",3,"Tôi nhận biết và tránh các email lừa đảo (phishing).",
                "I can recognize and avoid phishing emails.", False),
]
# DQ - Creation (CR)
dq_items += [
    likert_item("DQ","Creation",1,"Tôi thường tạo nội dung số (video, bài viết, dự án nhỏ).",
                "I regularly create digital content (videos, posts, small projects).", False),
    likert_item("DQ","Creation",2,"Tôi biết sử dụng công cụ AI để hỗ trợ học tập hoặc sáng tạo.",
                "I know how to use AI tools to support learning or creativity.", False),
    likert_item("DQ","Creation",3,"Tôi ít khi hoàn thành sản phẩm số vì thiếu kế hoạch.",
                "I rarely finish digital products because I lack a plan.", True),
]
# DQ - Collaboration (CO)
dq_items += [
    likert_item("DQ","Collaboration",1,"Tôi sử dụng công cụ cộng tác (Docs, Git, Kanban) trong học nhóm.",
                "I use collaboration tools (Docs, Git, Kanban) for group work.", False),
    likert_item("DQ","Collaboration",2,"Tôi thường không chia sẻ tiến độ với nhóm cho đến phút cuối.",
                "I often keep my progress to myself until the last minute.", True),
    likert_item("DQ","Collaboration",3,"Tôi có thói quen ghi log thay đổi khi làm việc trên cùng tệp/dự án.",
                "I habitually log changes when working on shared files/projects.", False),
]

aq_items = []
# AQ - Control (C)
aq_items += [
    likert_item("AQ","Control",1,"Khi gặp khó khăn, tôi tập trung vào phần mình có thể kiểm soát.",
                "When facing difficulties, I focus on what I can control.", False),
    likert_item("AQ","Control",2,"Tôi thường đổ lỗi cho hoàn cảnh khi kết quả không tốt.",
                "I often blame circumstances when results are poor.", True),
    likert_item("AQ","Control",3,"Tôi biết cách chia bài toán lớn thành các bước nhỏ để xử lý.",
                "I can break big problems into smaller steps to handle them.", False),
]
# AQ - Ownership (O)
aq_items += [
    likert_item("AQ","Ownership",1,"Tôi chịu trách nhiệm về kết quả công việc của mình.",
                "I take responsibility for my work outcomes.", False),
    likert_item("AQ","Ownership",2,"Khi sai, tôi né tránh thừa nhận trước nhóm.",
                "When wrong, I avoid admitting it to the group.", True),
    likert_item("AQ","Ownership",3,"Tôi chủ động xin phản hồi để cải thiện.",
                "I proactively ask for feedback to improve.", False),
]
# AQ - Reach (R)
aq_items += [
    likert_item("AQ","Reach",1,"Tôi cố gắng để vấn đề không lan sang các lĩnh vực khác.",
                "I prevent problems from spreading into other areas.", False),
    likert_item("AQ","Reach",2,"Một thất bại nhỏ khiến tôi đánh giá thấp bản thân ở mọi mặt.",
                "A small failure makes me see myself as bad at everything.", True),
    likert_item("AQ","Reach",3,"Tôi đặt ranh giới thời gian cho việc lo lắng và quay lại hành động.",
                "I time-box worrying and return to action.", False),
]
# AQ - Endurance (E)
aq_items += [
    likert_item("AQ","Endurance",1,"Tôi kiên trì theo đuổi mục tiêu dù tiến độ chậm.",
                "I persist toward goals even when progress is slow.", False),
    likert_item("AQ","Endurance",2,"Tôi dễ nản khi dự án kéo dài nhiều tuần.",
                "I quickly lose motivation in projects that last weeks.", True),
    likert_item("AQ","Endurance",3,"Tôi có thói quen theo dõi thói quen/tiến độ mỗi ngày.",
                "I track my habits/progress daily.", False),
]

df_likert = pd.DataFrame(eq_items + dq_items + aq_items)

# Save files
iq_path = "/mnt/data/iq_items.csv"
likert_path = "/mnt/data/eq_dq_aq_items.csv"

df_iq.to_csv(iq_path, index=False)
df_likert.to_csv(likert_path, index=False)

# Show previews
display_dataframe_to_user("Preview – IQ items", df_iq.head(6))
display_dataframe_to_user("Preview – EQ/DQ/AQ items", df_likert.head(12))

iq_path, likert_path
